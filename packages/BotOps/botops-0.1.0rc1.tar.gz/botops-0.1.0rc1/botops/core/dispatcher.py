from __future__ import annotations

import asyncio
import typing
from logging import getLogger

from botops import Handler
from botops.telegram import Update

if typing.TYPE_CHECKING:
    from botops.bot import Bot


class Dispatcher:
    def __init__(self) -> None:
        self.handlers: list[Handler] = []
        self.logger = getLogger(__name__)

    def register(self, *handlers: type[Handler]) -> None:
        self.handlers.extend(handler() for handler in handlers)

    async def dispatch(self, bot: Bot, update: Update, done_callback: typing.Callable) -> None:
        for handler in reversed(self.handlers):
            concrete_update = getattr(update, handler.__update_type__)
            if concrete_update is None:
                continue

            task = asyncio.create_task(
                handler(bot, concrete_update), name=handler.__class__.__name__
            )
            task.add_done_callback(done_callback)

            if handler.Meta.propagation:
                continue

            return

        self.logger.info(f"Alone update:\n\t{update}")
