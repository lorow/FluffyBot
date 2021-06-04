from discord.ext import commands


class UsefulCommand(object):

    __json_doc__ = """
         {
            "ignore": false,
            "brief": "Probably useful commands",
    
            "commands":{
                "invite":{
                    "desc": "Bot will send you an invite link so you can invite it to your own server",
    
                    "args":{}
                }
            }
        } 
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
