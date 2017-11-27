from discord.ext import commands

class testCog(object):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def present(self, ctx):
        await ctx.send("What? Nno... I'm not sleeping")

def setup(bot):
    print("Up and running!")
    bot.add_cog(testCog(bot))