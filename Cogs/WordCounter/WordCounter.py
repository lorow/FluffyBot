from discord.ext import commands

from Core.Events import FluffyEventSystem
from Core.Config.ConfigManager import ConfigManager
from Core.storage.repository.repositories.word_counter_repository import (
    WordCounterRepository,
)


class WordCounter(commands.Cog):

    __json_doc__ = """{}"""

    def __init__(self, bot, event_manager, config_manager, word_counter_repository):
        self.configManager = config_manager
        self.eventManager = event_manager
        self.bot = bot
        self.word_counter_repository = word_counter_repository


def setup(
    bot,
    event_manager: FluffyEventSystem,
    config_manager: ConfigManager,
    word_counter_repository: WordCounterRepository,
):
    print("Added word counter cog")
    bot.add_cog(
        WordCounter(bot, event_manager, config_manager, word_counter_repository)
    )
