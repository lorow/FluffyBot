from discord.ext import commands


class TagModule(object):
    """Simple tag system, store your most valuable data here. But don't forget about a backup!

        Usage:
            [prefix]tag [name] - to get saved data under that tag
            [prefix]tag [name] [data] - to save some data under that tag
            [prefix]save - to save the data to a file
            [prefix]load - to load data from the backup file. Note, this happens automatically when the bot start"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tag(self, ctx, *, content=''):
        if content.count('"') % 2 == 0 and content.count('"') > 0:
            await ctx.send("yep, seems legit")
        else:
            await ctx.send("dunno")


def setup(bot):
    print("added tagSystem")
    bot.add_cog(TagModule(bot))
