from discord.ext import commands


class TagModule(object):

    __json_doc__ = \
        """
         {
            "ignore": false,
            "brief":"Simply tags",
    
            "commands":{
                "tag":{
                    "desc": "Bot will send you whatever was under given tag",
    
                    "args":{
                        "tag"  : "for example 'foobar'"
                    }
                }
            }
         } 
        """

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
