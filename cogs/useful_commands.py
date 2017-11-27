from discord.ext import commands
import cogs.utils.configJSON as configJson


class UsefulCommand(object):
    """Just some use(less)ful commands

        Usage:
            [prefix]invite - will send an invite link for you to let you invite this bot

    """

    def __init__(self, bot):
        self.bot = bot
        self.invite_link = "https://discordapp.com/oauth2/" \
                           "authorize?client_id=328174635965349888&scope=bot&permissions=305392711"

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(self.invite_link)

# unsafe, only for development purposes
    @commands.command()
    async def reload(self, ctx):
        await ctx.send("Hot reload started")
        await ctx.send("unloading cogs")
        for cog in configJson.extensions:
            self.bot.unload_extension(cog)
        await ctx.send("unloaded all cogs")
        await ctx.send("reading new config")
        new_conf = configJson.reload_config()

        await ctx.send("loading new config")
        for new_cog in new_conf['extensions']:
            self.bot.load_extension(new_cog)

        await ctx.send("successfully loaded new cogs. Now you can use your bot")

    @commands.command()
    async def blame(self, ctx, user):
        await ctx.send(user + " https://www.youtube.com/watch?v=R3ZEzG0r7Yc")

def setup(bot):
    print("useful commands added")
    bot.add_cog(UsefulCommand(bot))
