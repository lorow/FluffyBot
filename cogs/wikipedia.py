import discord
import wikipedia
from discord.ext import commands


class Wiki(object):

    __json_doc__ =\
        """
         {
            "ignore": false,
            "brief":"Plugin searching through wikipedia",
    
            "commands":{
                "wiki":{
                    "desc": "Returns one definition at a time",
    
                    "args":{
                        "lang"  : "The lang you want to use",
                        "query" : "Things you want to search for"
                    }
                }
              }
            } 
        """

    def __init__(self, bot):
        self.bot = bot
        self.lang = "en"
        self.query = "none"

    async def setup_query(self, args):
        query = args.split()
        self.lang = query[0]
        self.query = '_'.join(query[1:])

    @commands.command()
    async def wiki(self, ctx, *, args: str=''):
        if str == '':
            await ctx.send("here's how to use this commdand: \n "
                           "[pefix]wiki lang query - returns one definition at a time")
        else:  
            await self.setup_query(args)
            try:
                wikipedia.set_lang(self.lang)
                await ctx.send(embed=discord.Embed(title=' '.join(args.split()[1:]),
                                                   description=wikipedia.summary(self.query)))
            except Exception:
                await ctx.send("It seem that wikipedia does not support this language, try something else")


def setup(bot):
    print("added wiki module")
    bot.add_cog(Wiki(bot))
