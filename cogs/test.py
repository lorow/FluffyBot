from discord.ext import commands

class TestModule(object):

    def __init__(self, bot, eventManager, configManager):
        self.bot = bot
        self.configManager = configManager
        self.eventManager = eventManager

    @commands.command()
    async def test(self, ctx):
        await ctx.send()

def setup(bot, eventManager, configManager):
    print("added test")
    bot.add_cog(TestModule(bot, eventManager, configManager))