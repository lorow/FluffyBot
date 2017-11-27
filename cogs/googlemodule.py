from discord.ext import commands
import google as gl


class GoogleModule(object):
    """This plugin searches through the deepest depths of google for you. It has see what it didn't want to see. So please, be gentle.
      \n usage: \n
       [prefix]google the things you want to search for \n
       NOTE: checking if results or query is NSFW is extremely hard or/and impossible. Search wisely!"""

    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command()
    async def google(self, ctx, *, args=''):
        urls = gl.search(args, stop=1)
        i = 0
        for url in urls:
                if i == 0:
                    await ctx.send(url)
                    i = i + 1
                else:
                    break


def setup(bot):
    print("added Google Module")
    bot.add_cog(GoogleModule(bot))
