from discord.ext import commands
import google as gl


class GoogleModule(object):
    def __init__(self, bot: commands.bot):
        self.bot = bot

    @commands.command()
    async def google(self, ctx, *, args: str):
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

