# from discord.ext import commands
#
#
# class TestModule(object):
#
#     def __init__(self, bot, event_manager, config_manager):
#         self.bot = bot
#         self.configManager = config_manager
#         self.eventManager = event_manager
#
#     @commands.command()
#     async def test(self, ctx):
#         for i in range(2):
#             await ctx.send("`test` \n  test \n")
#
#     @commands.command()
#     async def update(self, ctx):
#         await ctx.send("updating!")
#         for cog in self.configManager.extensions:
#             self.bot.unload_extension(cog)
#         self.bot._load_cogs()
#         await ctx.send("updated!")
#
#
# def setup(bot, event_manager, config_manager):
#     print("added test")
#     bot.add_cog(TestModule(bot, event_manager, config_manager))

from operator import itemgetter

t = """
Help:

Test briefa

Usage:
jakiś jeszcze inny tekst


Brief:
command x:
    This does something

End_help:
"""

keywords = ("Brief:", "Usage:", "End_help:")
t = list(filter(None,t.split('\n')))
print(t)

y = [{"name":index, "index": t.index(index)} for index in keywords]
y.sort(key= itemgetter("index"))
print(y)