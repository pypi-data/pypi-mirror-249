import asyncio
from asyncio import Queue
from collections.abc import AsyncIterator, Awaitable, Callable
from logging import getLogger
from typing import Any, Literal, TypeVar, Unpack

from botops import telegram
from botops.core import APIClient
from botops.utils import Cleanup, Loader

__all__ = ["BotEngine"]

_R = TypeVar("_R")


class BotEngine(Cleanup):
    def __init__(self, token: str) -> None:
        self._client = APIClient()
        self._lock = asyncio.Lock()
        self._is_running = False
        self._worker_task: Awaitable | None = None
        self._url = f"/bot{token}"
        self._id = int(token.split(":")[0])
        self._last_update_id: int | None = None
        self._updates: Queue[telegram.Update] = asyncio.Queue(maxsize=100)
        self._load = Loader()
        self._logger = getLogger(__name__)

    async def _on_startup(self) -> None:
        await self._client.setup()
        await self._start()

    async def _on_shutdown(self) -> None:
        await self._stop()
        await self._client.shutdown()

    async def _start(self) -> None:
        await self._lock.acquire()

        async def _worker() -> None:
            self._lock.release()
            while self._is_running:
                await self._get_updates(limit=1, timeout=3)

        self._is_running = True
        self._worker_task = asyncio.create_task(_worker())

        await self._lock.acquire()  # Wait task for start running at the event loop.

    async def _stop(self) -> None:
        if self._is_running:
            self._is_running = False

        if self._worker_task:
            await self._worker_task

    def _recalculate_last_update_id(self, update_id: int) -> None:
        self._last_update_id = update_id + 1

    async def _get_updates(self, **attrs: Unpack[telegram.GetUpdates]) -> None:
        updates = await self.execute(
            "GET",
            telegram.Method.get_updates,
            list[telegram.Update],
            offset=self._last_update_id,
            **attrs,
        )

        if updates:
            self._recalculate_last_update_id(updates[-1].update_id)

        for update in updates:
            await self._updates.put(update)

    def _get_path(self, method: telegram.Method) -> str:
        return f"{self._url}/{method}"

    @property
    def updates(self) -> AsyncIterator:
        def _done_callback(task: asyncio.Task | None = None) -> None:
            self._updates.task_done()

            if task is None:
                return

            if task.cancelled():
                self._logger.warning(f"Task {task.get_name()} is cancelled!")
            elif exc := task.exception():
                self._logger.exception(f"Task {task.get_name()} {task.get_stack()}!", exc_info=exc)
            else:
                self._logger.info(f"Task {task.get_name()} successfully finished!")

        async def _async_iter() -> (
            AsyncIterator[tuple[dict, Callable[[asyncio.Task | None], None]]]
        ):
            while update := await self._updates.get():
                yield update, _done_callback

            await self._updates.join()

        return _async_iter()

    async def execute(
        self,
        http_method: Literal["POST", "GET"],
        method: telegram.Method,
        result: type[_R],
        /,
        **attrs: Any,
    ) -> _R:
        response = await self._client.request(http_method, self._get_path(method), **attrs)

        if not response.ok:
            raise ValueError(
                f"Telegram response error code: {response.error_code}. {response.description}"
            )

        return self._load(result, response.result)
