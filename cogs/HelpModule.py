import ujson
from cogs.core.utils import ErrorCodes
import discord
from discord.ext import commands
import difflib

class HelpModule(object):

    __json_doc__ = """
     {
        "ignore": true,
        "brief":"just a brief message",

        "commands":{
            "command":{
                "desc": "short desc",

                "args":{
                    "arg-name": "desc"
                }
            }
          }
        } 
        """

    def __init__(self, bot, cogs, config_manager):
        self.bot = bot

        self.config_manager = config_manager
        self.doc_keys = list(config_manager.get_field("extensions").keys())
        self.docs = {}

        self.collect_doc(cogs)
        self.filter_docs()

    def collect_doc(self, cogs):
        self.docs["HelpModule"] = ujson.loads(self.__json_doc__)

        for cog, instance in cogs.items():
            try:
                self.docs[cog] = ujson.loads(instance.__json_doc__)
            except AttributeError:
                print(ErrorCodes.bcolors.FAIL +
                      "The {cog} is missing __json_doc__ attribute".format(cog=cog)
                      + ErrorCodes.bcolors.ENDC)
            except ValueError:
                print(ErrorCodes.bcolors.FAIL +
                      "there was an problem with decoding {cog}'s __json_doc__, check it".format(cog=cog)
                      + ErrorCodes.bcolors.ENDC)

    def filter_docs(self):
        for cog, doc in list(self.docs.items()):
            if "ignore" in doc and doc['ignore'] is True:
                del self.docs[cog]

    async def prepare_module_names(self):
        return "\n".join(self.docs.keys())

    async def prepare_default_embed(self, embed, ctx):
        embed.title = ctx.bot.user.name
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        return embed

    async def prepare_embed_help(self, embed, ctx):

        embed.color = discord.Colour(0x8cff00)

        embed.add_field(
            name="@{author}".format(author=ctx.author.name),
            value="Here's some help for you!",
            inline=False
        )

        embed.add_field(
            name="Current prefixes",
            value= "```" + ', '.join(ctx.bot._opts['command_prefix']) + "```",
            inline=False
        )

        embed.add_field(
            name="How to use",
            value="Simply write //help *module* - this will show more info about given module \n",
            inline=False
        )

        embed.add_field(
            name="Active modules",
            value="```css\n{modules}```".format(modules=await self.prepare_module_names()),
            inline=False
        )

        embed.add_field(
            name="Useful links",
            value=":link: [Website](https://discord.com)\n"
                  ":bulb: [Github](https://github.com/lorow/fluffy)\n",
            inline=False
        )

        embed.add_field(
            name="Development",
            value=":clipboard:[On Trello!](https://trello.com/b/4WdID9tN/fluffybot)",
            inline=False
        )

        embed.add_field(
            name="Want me on your server?",
            value=":space_invader: [Invite me!](https://discord.com)"
        )

        embed.add_field(
            name="Bot version",
            value="Fluffy ``2.0``"
        )

        embed.set_footer(
            text="In case something goes wrong, send me a message -> #lorow6600"
        )

        return embed

    async def prepare_embed_module(self, embed, ctx, module):
        return embed


    @commands.command()
    async def help(self, ctx, *, module: str = ''):

        embed = await self.prepare_default_embed(discord.Embed(), ctx)

        if not module:
           await ctx.send(embed=await self.prepare_embed_help(embed, ctx))
        else:
            await ctx.send(embed=await self.prepare_embed_module(embed, ctx, module))


def setup(bot, config_manager):
    print("Added HelpModule")
    bot.remove_command("help")
    bot.add_cog(HelpModule(bot, bot.cogs, config_manager))
