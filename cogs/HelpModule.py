import ujson
from cogs.core.utils import ErrorCodes
import discord
from discord.ext import commands


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


    @commands.command()
    async def help(self, ctx):
        await  ctx.send("help")

def setup(bot, config_manager):
    print("Added HelpModule")
    bot.remove_command("help")
    bot.add_cog(HelpModule(bot, bot.cogs, config_manager))
