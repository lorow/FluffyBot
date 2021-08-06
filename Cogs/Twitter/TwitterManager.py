import peony
from discord.ext import commands

from Core import FluffyEventSystem
from Core.Config.ConfigManager import ConfigManager
from Core.storage.repository.repositories.twitter_repository import TwitterRepository


class FluffyTwitter(commands.Cog):

    __json_doc__ = """
         {
            "ignore": true,
         } 
        """

    def __init__(self, bot, event_manager, config_manager, twitter_repository):
        self.configManager = config_manager
        self.eventManager = event_manager
        self.bot = bot
        self.twitterRepository = twitter_repository

        self.client = peony.PeonyClient(
            **{
                "consumer_key": config_manager.get_field("consumer_key"),
                "consumer_secret": config_manager.get_field("consumer_secret"),
                "access_token": config_manager.get_field("access_token"),
                "access_token_secret": config_manager.get_field("access_token_secret"),
            }
        )

        self.prepare_events()
        self.bot.loop.create_task(self.track())

    def prepare_events(self):
        for key in self.configManager.get_field("birds_to_follow"):
            self.eventManager.append_event(key)

    async def track(self):
        await self.bot.wait_until_ready()
        req = self.client.stream.statuses.filter.post(
            follow=list(self.configManager.birds_to_follow.values())
        )
        async with req as stream:
            async for tweet in stream:
                if peony.events.tweet(tweet):
                    await self.eventManager.notify(tweet["user"]["screen_name"], tweet)


def setup(
    bot,
    event_manager: FluffyEventSystem,
    config_manager: ConfigManager,
    twitter_repository: TwitterRepository,
):
    bot.add_cog(FluffyTwitter(bot, event_manager, config_manager, twitter_repository))
