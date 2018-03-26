from discord.ext import commands


class TestModule(object):

    def __init__(self, bot, event_manager, config_manager):
        self.bot = bot
        self.configManager = config_manager
        self.eventManager = event_manager

    async def test(self, message):
        await message.channel.send(message.author.id)

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
