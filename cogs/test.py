from discord.ext import commands


class TestModule(object):

    def __init__(self, bot, eventManager):
        self.bot = bot
        self.eventManager = eventManager

        self.eventManager.append_event("test_event").append_listener("test_event", self.te)

    @staticmethod
    def te(text):
        print(text)

    @commands.command()
    async def test(self, ctx):
        self.eventManager.notify("test_event", "fuck")
        await ctx.send("event sent")

def setup(bot, eventManager, configManager):
    bot.add_cog(TestModule(bot, eventManager))