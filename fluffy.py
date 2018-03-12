import importlib
import inspect
import logging
import sys

import discord
from discord.ext import commands

import cogs.utils.configJSON as configJson
from cogs.utils import FluffyEventSystem


class FluffyBot(commands.Bot):

    def __init__(self):
        self.configManager = configJson.configManager()

        self._opts = {'command_prefix': self.configManager.get_field('command_prefix'),
                      'description': self.configManager.get_field('description'),
                      'command_not_found': 'description'}

        self.additional_dep = {
            'bot': self,
            'config_manager': self.configManager,
            'event_manager': FluffyEventSystem.EventDispatcher().event_handler
        }

        self.logger = logging.getLogger('discord')
        self.handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
        super().__init__(**self._opts)

    async def on_ready(self):
        print('Logged in as: {u}'.format(u=self.user.name))
        print('Bots ID is: {i}'.format(i=self.user.id))
        print('Current version is {v}'.format(v=discord.version_info))
        print('_ _ _ _ _ _ _ _ _ _')

    async def on_error(self, event_method, *args, **kwargs):
        pass

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
        """overrides 'discord.commands' load_cogs() function in order to let Fluffybot provide additional dependencies
           when the bot starts to load plugins
        """
        for extension in self.configManager.get_field('extensions').values():
            lib = importlib.import_module(extension)
            if not hasattr(lib, 'setup'):
                del lib
                del sys.modules[extension]
                raise discord.ClientException('extension does not have a setup function')

            lib.setup(**self._prepare_dependencies(lib))
            self.extensions[extension] = lib

    def _prepare_logger(self, logger, handler):
        """prepares logger to let others log their info"""
        logger.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        logger.addHandler(handler)

    def _run(self):
        self._prepare_logger(self.logger, self.handler)
        self._load_cogs()
        self.run(self.configManager.get_field('bot_token'))
        return self


Fbot = FluffyBot()._run()
