import importlib
import importlib.util
import inspect
import logging
import sys

import discord
from discord.ext import commands
from discord.ext.commands import errors, ExtensionFailed

from Core import configLoader
from Core.repository.repository import AbstractRepository
from Core.utils import ErrorCodes


class FluffyBot(commands.Bot):
    def __init__(self):
        self.configManager = configLoader.ConfigManager()

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
        # noinspection PyUnresolvedReferences
        await self.additional_dep["event_manager"].notify("on_message", message)
        await self.process_commands(message)

    def _get_storage_connector(self, storage_config: dict):
        path_split = storage_config.get("connector").split(".")
        path = ".".join(path_split[:-1])
        module = importlib.import_module(path)
        return getattr(module, path_split[-1])

    def _get_repository(self, repository_item):
        repository_name, repository_path = repository_item
        path_split = repository_path.split(".")
        path = ".".join(path_split[:-1])
        module = importlib.import_module(path)
        return repository_name, getattr(module, path_split[-1])

    def _prepare_storages(self):
        """ Prepares the repositories and connects them to the database by using Connector classes """
        declared_storages = self.configManager.get_field("storage")

        for storage_name, storage_config in declared_storages.items():
            connector = self._get_storage_connector(storage_config)
            connection = connector(connection_details=storage_config.get("connection_details")).connect()

            for repository_item in storage_config.get("repositories").items():
                repository_name, repository_class = self._get_repository(repository_item)
                repository_class = repository_class(session=connection)
                self.storages[repository_name] = {
                    "class": repository_class
                }

    def _collect_dependencies(self):
        """loads the dependencies listed in configuration file"""
        deps = self.configManager.get_field("dependencies")

        for dependency in deps:
            dep = importlib.import_module(deps[dependency])
            # the thing that importlib imports is a module, so we have to somehow initialize it, the best way is by a
            # global setup function. If the module has no such function, then it's not supposed to be auto-imported
            try:
                self.additional_dep[dependency] = dep.setup()
            except AttributeError:
                print(
                    ErrorCodes.bcolors.WARNING
                    + "WARNING: dependency {dep} has no setup function and thus can not be added automatically".format(
                        dep=dependency
                    )
                    + ErrorCodes.bcolors.ENDC
                )

    def _prepare_dependencies(self, cog):
        """populates deps dict containing all of the needed dependencies by cog"""
        deps = {}
        argspec = inspect.getfullargspec(cog.setup)
        for key in argspec[0]:
            if key in self.storages.keys():
                deps[key] = self.storages[key]["class"]
            elif key in self.additional_dep.keys():
                deps[key] = self.additional_dep[key]
            else:
                print(f"Could not find anything for {key}")
        return deps

    def _load_from_module_spec(self, spec, key):
        lib = importlib.util.module_from_spec(spec)
        sys.modules[key] = lib
        try:
            spec.loader.exec_module(lib)
        except Exception as e:
            del sys.modules[key]
            raise errors.ExtensionFailed(key, e) from e

        try:
            setup = getattr(lib, 'setup')
        except AttributeError:
            del sys.modules[key]
            raise errors.NoEntryPointError(key)

        try:
            setup(**self._prepare_dependencies(lib))
        except Exception as e:
            del sys.modules[key]
            self._remove_module_references(lib.__name__)
            self._call_module_finalizers(lib, key)
            raise errors.ExtensionFailed(key, e) from e
        else:
            self._BotBase__extensions[key] = lib

    def _load_cogs(self):
        for extension in self.configManager.get_field("extensions").values():
            try:
                self.load_extension(extension)
            except ExtensionFailed:
                print(f"{extension} - failed")

    def _prepare_logger(self, logger, handler):
        """prepares logger to let others log their info"""

        logger.setLevel(logging.DEBUG)
        handler.setFormatter(
            logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        )
        logger.addHandler(handler)

    def _run(self):

        self._prepare_logger(self.logger, self.handler)
        self._collect_dependencies()
        self._prepare_storages()
        self._load_cogs()
        # noinspection PyUnresolvedReferences
        self.additional_dep["event_manager"].append_event("on_message")
        self.run(self.configManager.get_field("bot_token"))
        return self


Fbot = FluffyBot()
