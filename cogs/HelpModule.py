from discord.ext import commands
import discord


class HelpModule(object):

    def __init__(self, bot, cogs):
        self.bot = bot
        self.cogs = cogs
 
    @commands.command()
    async def help(self, ctx, *, args=''):

        if len(args) <= 0:
            message = discord.Embed(
                title="Here's the list of all active plugins:",
                description='\n'.join(list(self.cogs)))
            message.set_footer(text="To see how to use the plugins type: help nameOfThePlugin")
            await ctx.send(embed=message)
        else:
            message = discord.Embed(
                title=args,
                description=self.cogs[args].__doc__)
            await ctx.send(embed=message)

        await ctx.send("empire did nothing wrong!")


def setup(bot):
    print("Added HelpModule")
    bot.remove_command("help")
    bot.add_cog(HelpModule(bot, bot.cogs))
