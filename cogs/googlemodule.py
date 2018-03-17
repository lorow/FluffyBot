from discord.ext import commands
try:
    import googlesearch as gl
except ImportError:
    import google as gl


class GoogleModule(object):
    # """
    #    It has seen what it didn't want to see. So please, be gentle.
    #   \n usage: \n
    #    [prefix] the things you want to search for \n
    #    NOTE: """

    """
        Help:

        Brief:
        This plugin searches through the deepest depths of google for you. Search wisely!

        Usage:
        command //google [lang] [query]:
            This command will return whatever it finds first

        End_help:
        """

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
