from discord.ext import commands

from Cogs.WordCounter.models import WordsToTrackModel, WordCounterModel
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
        self.word_counter_repository: WordCounterRepository = word_counter_repository

    @commands.group()
    async def word(self, ctx):
        pass

    @word.command()
    async def track(self, ctx, *, word=""):
        if word:
            word_to_track = WordsToTrackModel()
            self.word_counter_repository.add(word_to_track)
            await ctx.send(f"I've started tracking '{word_to_track}' for ya")

    @word.command()
    async def count(self, ctx, *, word="", for_user=""):
        if word:
            counted_word: WordCounterModel = self.word_counter_repository.get(
                word, for_user
            )  # TODO move the repository implementation to the cog domain so that it can be typed
            if for_user:
                await ctx.send(
                    f"You've said '{counted_word.word}' exactly {counted_word.count}"
                )


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
