import importlib
import inspect
import logging
import sys

import discord
from discord.ext import commands

import cogs.core.configJSON as configJson
import cogs.core.utils.ErrorCodes as errorCodes


class FluffyBot(commands.Bot):

    def __init__(self):
        self.configManager = configJson.ConfigManager()

        self._opts = {'command_prefix': self.configManager.get_field('command_prefix'),
                      'description': self.configManager.get_field('description'),
                      'command_not_found': 'description'}

        # some starting deps are added at the very beginning, the rest will be loaded at runtime
        self.additional_dep = {
            'bot': self,
            'config_manager': self.configManager
        }

        self.logger = logging.getLogger('discord')
        self.handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        super().__init__(**self._opts)

        self._run()

    async def on_ready(self):
        print('Logged in as: {u}'.format(u=self.user.name))
        print('Bots ID is: {i}'.format(i=self.user.id))
        print('Current version is {v}'.format(v=discord.version_info))
        print('_ _ _ _ _ _ _ _ _ _')

    async def on_error(self, event_method, *args, **kwargs):
        print(event_method)

    async def on_message(self, message):
        await self.additional_dep['event_manager'].notify("on_message", message)

        await self.process_commands(message)

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
                print(errorCodes.bcolors.WARNING +
                      'WARNING: dependency {dep} has no setup function and thus can not be added automatically'
                      .format(dep=dependency)
                      + errorCodes.bcolors.ENDC)

    def _prepare_dependencies(self, cog):
        """populates 'dict' containing all of the needed dependencies by cog"""
        deps = {}
        for key in inspect.getfullargspec(cog.setup)[0]:
            try:
                deps[key] = self.additional_dep[key]
            except KeyError:
                pass
        return deps

    def _load_cogs(self):
        """overrides :discord.commands: load_cogs() function in order to let Fluffybot provide additional dependencies
           when the bot starts to load plugins
        """

        for extension in self.configManager.get_field('extensions').items():
            lib = importlib.import_module(extension[1])
            if not hasattr(lib, 'setup'):
                del lib
                del sys.modules[extension[1]]
                raise discord.ClientException('extension does not have a setup function')

            lib.setup(**self._prepare_dependencies(lib))
            self.extensions[extension[0]] = lib

    def _prepare_logger(self, logger, handler):
        """prepares logger to let others log their info"""

        logger.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)

    def _run(self):

        self._prepare_logger(self.logger, self.handler)
        self._collect_dependencies()
        self._load_cogs()
        self.additional_dep['event_manager'].append_event("on_message")
        self.run(self.configManager.get_field('testing_bot_token'))
        return self


Fbot = FluffyBot()
