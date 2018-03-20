from discord.ext import commands
from discord.ext.commands import Command


class TestModule(object):

    def __init__(self, bot, event_manager, config_manager):
        self.bot = bot
        self.configManager = config_manager
        self.eventManager = event_manager
        self.eventManager.append_listener("on_message", self.test)

    @commands.command()
    async def testT(self, ctx):
        await ctx.send("t")

    async def test(self, message):
        await Command.invoke(self.testT)

    @commands.command()
    async def update(self, ctx):
        await ctx.send("updating!")
        for cog in self.configManager.extensions:
            self.bot.unload_extension(cog)
        self.bot._load_cogs()
        await ctx.send("updated!")


def setup(bot, event_manager, config_manager):
    print("added test")
    bot.add_cog(TestModule(bot, event_manager, config_manager))
