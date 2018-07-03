from discord.ext import commands
try:
    import googlesearch as gl
except ImportError:
    import google as gl


class GoogleModule(object):


    __json_doc__ =\
    """
     {
        "ignore": false,
        "brief":"This command will return whatever it finds first",

        "commands":{
            "google":{
                "desc": "The bot will send an image from given subredit. Random also works!",

                "args":{
                    "lang"  : "lang-based version of google you'd like to use",
                    "query" : "things you'd like to search"
                }
            }
        }
    } 
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
