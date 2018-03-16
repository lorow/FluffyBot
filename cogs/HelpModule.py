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
        command x:
            This does something
        command x:
            This does something
        command x:
            This does something

        End_help:

        bla blqa bla
        """

    def __init__(self, bot, cogs):
        self.bot = bot
        self.keywords = ("Help:", "Brief:", "Usage:", "End_help:")
        self.ignore = ["FluffyTwitter", "TestModule"]
        self.docs = {}  # {name:{ brief:"awd", usage:["command", "use case", "command" ...]}, name: ...}
        self.parse_doc(cogs)

    def parse_doc(self, cogs):
        for cog in cogs:
            if cog not in self.ignore:
                if cogs[cog].__doc__ is not None:
                    spliced = list(filter(None, cogs[cog].__doc__.split('\n')))
                    spliced = [' '.join(x.split()) for x in spliced]
                    try:
                        indexes = {index: spliced.index(index) for index in self.keywords}
                    except ValueError:
                        raise IncompleteHelp("{c} - Your documentation is incomplete".format(c=cog))

                    if indexes["Help:"] < indexes["End_help:"] and indexes["Brief:"] < indexes["Usage:"]:
                        self.docs[cog] = {
                            "brief": spliced[indexes["Brief:"] + 1:indexes["Usage:"]],
                            "usage": spliced[indexes["Usage:"] + 1:indexes["End_help:"]]
                        }
                    else:
                        raise IncompleteHelp("{c} - Your documentation is incomplete".format(c=cog))
                else:
                    raise MissingDoc("{c} - missing doc".format(c=cog))

    @staticmethod
    async def prepare_entry(x):
        return "`" + x + "`"

    @commands.command()
    async def help(self, ctx, *, args=''):
        pass
        if len(args) <= 0:
            message = discord.Embed(
                title="Here's the list of all active modules:",
                description="\n".join([await self.prepare_entry(x)
                                       + "\n    " + ' '.join(self.docs[x]["brief"]) for x in self.docs.keys()])
            )
            message.set_footer(text="To see how to use the plugins type: help nameOfThePlugin")
            await ctx.send(embed=message)


def setup(bot):
    print("Added HelpModule")
    bot.remove_command("help")
    bot.add_cog(HelpModule(bot, bot.cogs))
