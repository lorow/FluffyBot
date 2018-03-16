from collections import defaultdict

import aiohttp
from discord.ext import commands


class DerpiBooru(object):
    # """ Ponies, ponies, ponies
    #
    #     Usage:
    #         [prefix]dp [optional amount] query - bot will send some cute pony pictures from DerpiBooru"""

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

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.search_link = 'https://derpibooru.org/search.json?q='
        self.entries = defaultdict(list)
        self.keys = ['image']

    @commands.command()
    async def dp(self, ctx, *, args: str):
        split_message = args.split()

        amount = int(split_message[-1]) if split_message[-1].isdigit() and int(split_message[-1]) > 0 else 1
        query = '+'.join(split_message) if not split_message[-1].isdigit() else '+'.join(split_message[:-1])
        await self.make_req(query)

        for i in range(amount):
            await ctx.send(self.entries[self.keys[0]][i])

    async def make_req(self, query):
        async with aiohttp.ClientSession() as cs:
            req_mess = self.search_link + query
            async with cs.get(req_mess) as r:
                entries = await r.json()
                for entry, key in zip(entries['search'], self.keys):
                    self.entries[key].append("http:{s}".format(s=entry[key]) if key == "image" else entry[key])


def setup(bot):
    print("added DP module")
    bot.add_cog(DerpiBooru(bot))
