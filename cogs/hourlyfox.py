import discord
from discord.ext import commands


class HourlyFox(object):


    __json_doc__ =\
    """
     {
        "ignore": false,
        "brief":"
            A new floof every hour!
            By default the bot won't send anything unless you tell it so. It also won't send anything if it was the last one
            to send a message.
        ",

        "commands":{
            "sendFluffs":{
                "desc": "Adds the channel from which this was executed to the list of awaiting for foxxos",

                "args":{
                    "ignore_limit"  : "[Optional] if you want the bot to ignore the limit"
                }
            },
            
            "stopSending":{
                "desc": "Removes the channel from which this was executed from mentioned above list",
                "args":{}
            }
        }
     } 
    """

    def __init__(self, bot, config_manager, event_manager):
        self.bot = bot
        self.configManager = config_manager
        self.eventManager = event_manager

        self.default_title = "Here's a fox for ya!"

        self.last_id = {}

        self.channels = []
        self.channels_type = {}

        self.eventManager.append_listener("on_message", self.change_last_id)
        self.eventManager.append_listener('hourlyFox', self.send_link)
        self.eventManager.append_listener("lorow23", self.send_link)

    async def change_last_id(self, message):
        # update the last id only if the title of the embedded message is the same as the default title
        try:
            if message.embeds[0].title == self.default_title:
                self.last_id[message.channel.id] = message.author.id
            else:
                self.last_id[message.channel.id] = 0 # just nothing, so the bot can simply ignore it
        except Exception as e:
            print(e)

        print('{c} {i}}'.format(c = message.channel.id, i = self.last_id[message.channel.id]))

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
        embed_tweet = discord.Embed(title=self.default_title).set_image(url=image).set_footer(text=link)

        for channel in self.channels:
            if self.channels_type[channel] == "ignore_limit":
                await channel.send(embed=embed_tweet)
            else:
                if self.last_id[channel] != self.bot.user.id:
                    await channel.send(embed=embed_tweet)


def setup(bot, config_manager, event_manager):
    bot.add_cog(HourlyFox(bot, config_manager, event_manager))
