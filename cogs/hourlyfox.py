import discord
from discord.ext import commands


class HourlyFox(object):
    """
        Help:

        Brief:
        A new floof every hour!
        By default the bot won't send anything unless you tell it so. It also won't send anything if it was the last one
        to send a message.

        Usage:
        command //sendFluffs [optional ignore - if you want the bot to ignore the limit] :
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
        self.eventManager.append_listener("on_message", self.change_last_id)
        self.channels = []
        self.channels_type = {}
        self.last_id = None

    async def change_last_id(self, message):
        self.last_id = message.author.id

    @commands.command()
    async def sendFluffs(self, ctx, ignore="False"):

        if ctx.channel in self.channels:
            await ctx.send("This channel is already waiting for fluffs")
        else:
            self.channels.append(ctx.channel)
            self.channels_type[ctx.channel] = ignore
            await ctx.send("I'll be sending fluffs here from now on!")

    @commands.command()
    async def stopSendingFluffs(self, ctx):
        if ctx.channel in self.channels:
            self.channels.remove(ctx.channel)
            self.channels_type.pop(ctx.channel)
            await ctx.send("This channel will no longer receive any fluffs")
        else:
            await ctx.send("This channel was not receiving any fluffs at all")

    async def send_link(self, tweet):

        image = tweet['entities']['media'][0]['media_url_https']
        link = tweet['entities']['media'][0]['url']
        print(tweet)
        embed_tweet = discord.Embed(description="Here's a fox for ya!").set_image(url=image).set_footer(text=link)

        for channel in self.channels:
            if bool(self.channels_type[channel]):
                if self.last_id != self.bot.user.id:
                    await channel.send(embed=embed_tweet)
            else:
                await  channel.send(embed=embed_tweet)


def setup(bot, config_manager, event_manager):
    bot.add_cog(HourlyFox(bot, config_manager, event_manager))
