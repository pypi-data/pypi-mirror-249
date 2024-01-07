from __future__ import annotations

import asyncio
from collections.abc import Callable
from logging import getLogger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from botops.core import Bot, Handler
    from botops.telegram import Update


class Dispatcher:
    def __init__(self) -> None:
        self.handlers: list[Handler] = []
        self.logger = getLogger(__name__)

    def register(self, *handlers: type[Handler]) -> None:
        self.handlers.extend(handler() for handler in handlers)

    async def dispatch(self, bot: Bot, update: Update, done_callback: Callable) -> None:
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
