from collections import defaultdict

import aiohttp
import discord
from discord.ext import commands


class E926(object):
    # """ Plugin searching through e926 image booru
    #
    #     Usage:
    #         [prefix]e9 image [optional amount] query - bot will send some furbals, just for you!
    #         [prefix]e9 link [optional amount] query - bot will send an link to the original post, instead of just image!
    # """

    """
    Help:

    Test briefa

    Brief:
    jakiś jeszcze inny tekst

    cawd

    Usage:
    command x:
        This does something
    command x:
        This does something
    command x:
        This does something

    End_help:

    bla blqa bla
    """

    def __init__(self, bot):
        self.bot = bot
        self.search_link = 'http://e926.net/post/index.json?tags='
        self.original_link = 'http://e926.net/post/show/'
        self.keys = ['file_url', 'author', 'score', 'id']
        self.entries = defaultdict(list)

    @commands.group()
    async def e9(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("in case you forgot: \n" +
                           "[prefix]e9 image [optional amount] query - bot will send some furbals, just for you! \n "
                           "[prefix]e9 link [optional amount] query - bot will send an link to the original post, instead of just image!")

    @e9.command()
    async def image(self, ctx, *, arg: str):
        split_message = arg.split()

        amount = int(split_message[-1]) if split_message[-1].isdigit() and int(split_message[-1]) > 0 else 1
        query = '+'.join(split_message) if not split_message[-1].isdigit() else '+'.join(split_message[:-1])

        self.entries.clear()
        await self.make_req(query, amount)

        for entry in self.entries["entries"][0]:
            await ctx.send(embed=discord.Embed(description='Author: {a}, Score: {s}'
                                               .format(a=entry[self.keys[1]], s=entry[self.keys[2]]))
                           .set_image(url=entry[self.keys[0]]))

    @e9.command()
    async def link(self, ctx, *, arg: str):
        await ctx.send("Not implemented yet!")

    async def make_req(self, query, amount):
        async with aiohttp.ClientSession() as cs:
            req_mess = '{l}{q}{li}{a}'.format(l=self.search_link, q=query, li='&limit=', a=str(amount))
            async with cs.get(req_mess) as r:
                self.entries["entries"].append(await r.json())


def setup(bot):
    print('added E9 module')
    bot.add_cog(E926(bot))
