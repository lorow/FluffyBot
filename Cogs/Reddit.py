import random
from collections import defaultdict

import aiohttp
from discord.ext import commands


class Reddit(commands.Cog):

    __json_doc__ = """
     {
        "ignore": false,
        "brief":"Just some basic Reddit commands. Use them to make your or someones day better",

        "commands":{
            "reddit image":{
                "desc": "The bot will send an image from given subredit. Random also works!",

                "args":{
                    "subreddit name": "A subreddit from which you want to get a random image"
                }
            }
        }
    } 
    """

    def __init__(self, bot, config_manager):
        self.bot = bot
        self.configManager = config_manager
        self.imgur_link = "https://api.imgur.com/3/gallery/r/"
        self.entries = defaultdict(list)
        self.keys = ["link"]

    @commands.group()
    async def reddit(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(self.__doc__)

    @reddit.command()
    async def image(self, ctx, *, subreddit=""):
        if subreddit == "":
            await ctx.send(
                "It seems like you forgot how to use it, so here you go: \n"
                " [prefix]reddit image [subreddit name]"
            )
        else:
            await self.make_req(self.imgur_link, subreddit)
            i = random.randint(0, len(self.entries["link"]))
            await ctx.send(self.entries["link"][i])

    @reddit.command()
    async def post(self, ctx, *, subreddit=""):
        await ctx.send("not implemented yet!")

    async def make_req(self, link, subreddit):
        async with aiohttp.ClientSession(
            headers={
                "Authorization": "Client-ID "
                + self.configManager.get_field("imgur_client_id")
            }
        ) as cs:

            async with cs.get("{l}{s}".format(l=link, s=subreddit)) as r:
                entries = await r.json()
                for entry, key in zip(entries["data"], self.keys):
                    self.entries[key].append(entry[key])


def setup(bot, config_manager):
    print("Added Reddit module")
    bot.add_cog(Reddit(bot, config_manager))
