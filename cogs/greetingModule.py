from discord.ext import commands

class greetingModule(object):

    def __init__(self, bot):
        self.bot = bot

        @self.bot.listen()
        async def on_member_join(member):
            await member.send("Hello there! {u}".format(u=member.mention))

        @self.bot.listen()
        async def on_member_remove(member):
            await member.send("Good bye old friend {u}".format(u=member.mention))

def setup(bot):
    print("Greeting module ready to greet!")
    bot.add_cog(greetingModule(bot))