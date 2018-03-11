from discord.ext import commands


class UsefulCommand(object):
    """Just some use(less)ful commands

        Usage:
            [prefix]invite - will send an invite link for you to let you invite this bot

    """

    def __init__(self, bot, config_manager):
        self.bot = bot
        self.configManager = config_manager
        self.invite_link = "none for now"

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(self.invite_link)

    @commands.command()
    async def blame(self, ctx, user):
        await ctx.send(user + " https://www.youtube.com/watch?v=R3ZEzG0r7Yc")


def setup(bot, config_manager):
    print("useful commands added")
    bot.add_cog(UsefulCommand(bot, config_manager))
