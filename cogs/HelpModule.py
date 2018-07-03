import ujson
from cogs.core.utils import ErrorCodes
import pprint
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
                print(ErrorCodes.bcolors.FAIL+
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



    # def parse_doc(self, cogs):
    #     cogs['HelpModule'] = self
    #     for cog in enumerate(cogs):
    #         # cog is an tuple, so in the 1 place is what we really want, the actual object
    #         if cog[1] not in self.ignore:
    #             if cogs[cog[1]].__doc__ is not None:
    #                 spliced = list(filter(None, cogs[cog[1]].__doc__.split('\n')))
    #                 spliced = [' '.join(x.split()) for x in spliced]
    #                 try:
    #                     indexes = {index: spliced.index(index) for index in self.keywords}
    #                 except ValueError:
    #                     raise IncompleteHelp("{c} - Your documentation is incomplete".format(c=cog))
    #
    #                 if indexes["Help:"] < indexes["End_help:"] and indexes["Brief:"] < indexes["Usage:"]:
    #                     self.docs[self.doc_keys[cog[0]]] = {
    #                         "brief": spliced[indexes["Brief:"] + 1:indexes["Usage:"]],
    #                         "usage": spliced[indexes["Usage:"] + 1:indexes["End_help:"]]
    #                     }
    #                 else:
    #                     raise IncompleteHelp("{c} - Your documentation is incomplete".format(c=cog))
    #             else:
    #                 raise MissingDoc("{c} - missing doc".format(c=cog))
    #
    # @commands.command()
    # async def help(self, ctx, *, args=''):
    #     try:
    #         if len(args) <= 0:
    #             message = discord.Embed(
    #                 title="Here's the list of all active modules:",
    #                 description="\n".join(["`" + x + "`" + "\n    " +
    #                                        ' '.join(self.docs[x]["brief"]) for x in self.docs.keys()]))
    #             await ctx.send(embed=message)
    #         else:
    #             mess = discord.Embed(
    #                 title="Here's a list of commands for {c}".format(c=args),
    #                 description=''.join(["\n" + "`" + x[7: -1] + "`"
    #                                      if x.startswith("command") else "\n  " + x for x in self.docs[args]["usage"]]))
    #             await ctx.send(embed=mess)
    #     except Exception:
    #         await ctx.send("{arg} - probably doesn't exist, check your query".format(arg=args))


def setup(bot, config_manager):
    print("Added HelpModule")
    bot.remove_command("help")
    bot.add_cog(HelpModule(bot, bot.cogs, config_manager))
