import discord
from discord.ext import commands


class TestModule(object):

    def __init__(self, bot, event_manager, config_manager):
        self.bot = bot
        self.configManager = config_manager
        self.eventManager = event_manager

    @commands.command()
    async def test(self, ctx):
        await ctx.send(embed=discord.Embed().add_field(name="Description",
                                                       value=str({'key': 'value', 'key1': 'value', 'key2': 'value'}
                                                                 .keys())).add_field(name="Commands", value="test2"))


def setup(bot, event_manager, config_manager):
    print("added test")
    bot.add_cog(TestModule(bot, event_manager, config_manager))
