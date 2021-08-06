import importlib
import logging
import sys

import discord
from discord.ext import commands
from discord.ext.commands import ExtensionFailed, NoEntryPointError

from Core.Bot.utils import (
    _setup_logger_handler,
    _collect_dependencies,
    _prepare_dependencies,
    _prepare_storages,
)
from Core.Config.ConfigManager import ConfigManager


class FluffyBot(commands.Bot):
    def __init__(self):
        self.configManager = ConfigManager()
        self._opts = {
            "command_prefix": self.configManager.get_field("command_prefix"),
            "description": self.configManager.get_field("description"),
            "command_not_found": "description",
        }

        # some starting deps are added at the very beginning, the rest will be loaded at runtime
        self.additional_dep = {"bot": self, "config_manager": self.configManager}
        self.storages = {}

        self.logger = logging.getLogger("discord")
        self.handler = logging.FileHandler(
            filename="discord.log", encoding="utf-8", mode="w"
        )
        super().__init__(**self._opts)

        self._run()

    async def on_ready(self):
        print("Logged in as: {u}".format(u=self.user.name))
        print("Bots ID is: {i}".format(i=self.user.id))
        print("Current version is {v}".format(v=discord.version_info))
        print("_ _ _ _ _ _ _ _ _ _")

    async def on_error(self, event_method, *args, **kwargs):
        print(event_method)

    async def on_message(self, message):
        event_manager = self.additional_dep.get("event_manager", None)
        if event_manager:
            # noinspection PyUnresolvedReferences
            await event_manager.notify("on_message", message)

        await self.process_commands(message)

    def _load_from_module_spec(self, spec, key):
        """overridden method for allowing injecting additional dependencies"""
        lib = importlib.util.module_from_spec(spec)
        sys.modules[key] = lib
        try:
            spec.loader.exec_module(lib)
        except Exception as e:
            del sys.modules[key]
            raise ExtensionFailed(key, e) from e

        try:
            setup = getattr(lib, "setup")
        except AttributeError:
            del sys.modules[key]
            raise NoEntryPointError(key)

        try:
            setup(**_prepare_dependencies(self.storages, self.additional_dep, lib))
        except Exception as e:
            del sys.modules[key]
            self._remove_module_references(lib.__name__)
            self._call_module_finalizers(lib, key)
            raise ExtensionFailed(key, e) from e
        else:
            self._BotBase__extensions[key] = lib

    def _load_cogs(self):
        for extension in self.configManager.get_field("extensions").values():
            try:
                self.load_extension(extension)
            except ExtensionFailed as e:
                print(f"{extension} - failed")
                print(e)

    def _run(self):

        self.logger = _setup_logger_handler(self.logger, self.handler)
        self.additional_dep.update(_collect_dependencies(self.configManager))
        self.storages = _prepare_storages(self.configManager)
        self._load_cogs()
        # noinspection PyUnresolvedReferences
        self.additional_dep["event_manager"].append_event("on_message")
        self.run(self.configManager.get_field("bot_token"))
        return self
