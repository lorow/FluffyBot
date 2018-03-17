import discord
from discord.ext import commands


class HourlyFox(object):
    """
        Help:

        Brief:
        A new floof every hour!

        Usage:
        command //sendFluffs:
            Adds the channel from which this was executed to the list of awaiting for foxxos
        command //stopSending:
            Removes the channel from which this was executed from mentioned above list

        End_help:
        """

    def __init__(self, bot, config_manager, event_manager):
        self.bot = bot
        self.configManager = config_manager
        self.eventManager = event_manager
        self.eventManager.append_listener('hourlyFox', self.send_link)
        self.channels = []

    @commands.command()
    async def sendFluffs(self, ctx):
        if ctx.channel in self.channels:
            await ctx.send("This channel is already waiting for fluffs")
        else:
            self.channels.append(ctx.channel)
            await ctx.send("I'll be sending fluffs here from now on!")

    @commands.command()
    async def stopSending(self, ctx):
        try:
            self.channels.remove(ctx.channel)
        except ValueError:
            pass

    async def send_link(self, tweet):

        image = tweet['entities']['media'][0]['media_url_https']
        link = tweet['entities']['media'][0]['url']
        print(tweet)
        embed_tweet = discord.Embed(description="Here's a fox for ya!").set_image(url=image).set_footer(text=link)

        for channel in self.channels:
            await channel.send(embed=embed_tweet)


def setup(bot, config_manager, event_manager):
    bot.add_cog(HourlyFox(bot, config_manager, event_manager))
