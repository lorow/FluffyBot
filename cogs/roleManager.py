
from discord.ext import commands


class RoleManager(object):

    """
        Help:

        Brief:
        nothing for now

        Usage:
        command //test

        End_help:
        """

    def __init__(self, bot):
        print("role manager ready to give roles!")
        self.bot = bot


def setup(bot):
    bot.add_cog(RoleManager(bot))
