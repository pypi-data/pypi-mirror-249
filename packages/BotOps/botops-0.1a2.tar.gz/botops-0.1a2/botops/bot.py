from typing import Unpack

from botops import telegram
from botops.core import BotEngine, Dispatcher
from botops.utils import Cleanup

__all__ = ["Bot"]


class Bot(Cleanup):
    def __init__(self, token: str, dispatcher: Dispatcher):
        self._engine = BotEngine(token)
        self._dispatcher = dispatcher

    async def run(self) -> None:
        async for update, done_callback in self._engine.updates:
            await self._dispatcher.dispatch(self, update, done_callback)

    async def _on_startup(self) -> None:
        await self._engine.startup()

    async def _on_shutdown(self) -> None:
        await self._engine.shutdown()

    async def get_me(self) -> telegram.User:
        return await self._engine.execute("GET", telegram.Method.get_me, telegram.User)

    async def log_out(self) -> bool:
        return await self._engine.execute("GET", telegram.Method.log_out, bool)

    async def close(self) -> bool:
        return await self._engine.execute("GET", telegram.Method.close, bool)

    async def send_message(self, **attrs: Unpack[telegram.SendMessage]) -> telegram.Message:
        return await self._engine.execute(
            "POST", telegram.Method.send_message, telegram.Message, **attrs
        )
