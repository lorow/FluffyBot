import discord
from discord.ext import commands


class MissingDoc(Exception):
    pass


class IncompleteHelp(Exception):
    pass


class HelpModule(object):
    """
        Help:

        Test briefa

        Brief:
        jakiś jeszcze inny tekst

        cawd

        Usage:
        command baawd:
            This does something
        command adw:
            This does something
        command awd:
            This does something

        End_help:

        bla blqa bla
        """

    def __init__(self, bot, cogs, config_manager):
        self.bot = bot
        self.config_manager = config_manager
        self.keywords = ("Help:", "Brief:", "Usage:", "End_help:")
        self.ignore = config_manager.get_field("ignore_plugins")
        self.doc_keys = list(config_manager.get_field("extensions").keys())
        self.docs = {}  # {name:{ brief:"awd", usage:["command", "use case", "command" ...]}, name: ...}
        self.parse_doc(cogs)

    def parse_doc(self, cogs):
        for cog in enumerate(cogs):
            if cog[1] not in self.ignore:
                if cogs[cog[1]].__doc__ is not None:
                    spliced = list(filter(None, cogs[cog[1]].__doc__.split('\n')))
                    spliced = [' '.join(x.split()) for x in spliced]
                    try:
                        indexes = {index: spliced.index(index) for index in self.keywords}
                    except ValueError:
                        raise IncompleteHelp("{c} - Your documentation is incomplete".format(c=cog))

                    if indexes["Help:"] < indexes["End_help:"] and indexes["Brief:"] < indexes["Usage:"]:
                        self.docs[self.doc_keys[cog[0]]] = {
                            "brief": spliced[indexes["Brief:"] + 1:indexes["Usage:"]],
                            "usage": spliced[indexes["Usage:"] + 1:indexes["End_help:"]]
                        }
                    else:
                        raise IncompleteHelp("{c} - Your documentation is incomplete".format(c=cog))
                else:
                    raise MissingDoc("{c} - missing doc".format(c=cog))

    @commands.command()
    async def help(self, ctx, *, args=''):
        try:
            if len(args) <= 0:
                message = discord.Embed(
                    title="Here's the list of all active modules:",
                    description="\n".join(["`" + x + "`"+ "\n    " +
                                           ' '.join(self.docs[x]["brief"]) for x in self.docs.keys()]))
                await ctx.send(embed=message)
            else:
                mess = discord.Embed(
                    title="Here's a list of commands for {c}".format(c=args),
                    description=''.join(["\n" + "`" + x[7: -1]+ "`"
                                         if x.startswith("command") else "\n  " + x for x in self.docs[args]["usage"]]))
                await ctx.send(embed=mess)
        except Exception:
            await ctx.send("{arg} - probably doesn't exists, check your query".format(arg=args))


def setup(bot, config_manager):
    print("Added HelpModule")
    bot.remove_command("help")
    bot.add_cog(HelpModule(bot, bot.cogs, config_manager))
