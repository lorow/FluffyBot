from discord.ext import commands


class HourlyFox():

    def __init__(self, bot, configManager, eventManager):
        self.bot = bot
        self.configManager = configManager
        self.eventManager = eventManager
        self.eventManager.append_listener('hourlyFox', self.send_link)
        self.channels = []

    @commands.command()
    async def sendFluffs(self,ctx):
        self.channels.append(ctx.channel) if not ctx.channel in self.channels else await \
            ctx.send("This channel is already waiting for fluffs")
        await ctx.send("I'll be sending fluffs here from now on!")

    async def send_link(self, tweet):
        for channel in self.channels:
            await channel.send(tweet['entities']['media'][0]['media_url_https'])


def setup(bot, configManager, eventManager):
    bot.add_cog(HourlyFox(bot, configManager, eventManager))
