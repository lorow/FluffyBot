class HourlyFox():
    def __init__(self, bot, configManager, eventManager):
        self.bot = bot
        self.configManager = configManager
        self.eventManager = eventManager
        self.eventManager.append_listener('lorow23', self.testLink)

    async def testLink(self,link):
        channel = self.bot.core.get_channel(328175388331081739)
        await channel.send(link)

def setup(bot, configManager, eventManager):
    print("Hourly fox ready to send fluffs!")
    bot.add_cog(HourlyFox(bot, configManager, eventManager))
