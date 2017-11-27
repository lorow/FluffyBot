import cogs.utils.configJSON as configJson
from discord.ext import commands
import discord
import logging

opts = {'command_prefix': configJson.default_prefix,
        'description': configJson.bot_description,
        'command_not_found': ''}

bot = commands.Bot(**opts)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(discord.version_info)
    print('------')


@bot.event
async def on_command_error(ctx, error):
    await ctx.send("I'm sorry, something went wrong. This command may not exist \n")
    print(error)

if __name__ == '__main__':
    for e in configJson.extensions:
        bot.load_extension(e)
    bot.run(configJson.bot_token)
