import peony


class FluffyTwitter(object):

    def __init__(self, bot, eventManager, configManager):
        self.configManager = configManager
        self.eventManager = eventManager
        self.bot = bot
        self.client = peony.PeonyClient(**{'consumer_key': configManager.get_field("consumer_key"),
                                           'consumer_secret': configManager.get_field("consumer_secret"),
                                           'access_token': configManager.get_field("access_token"),
                                           'access_token_secret': configManager.get_field("access_token_secret")})

        self.prepare_events()
        self.bot.loop.create_task(self.track())

    def prepare_events(self):
        for key in self.configManager.get_field("birds_to_follow"):
            self.eventManager.append_event(key)

    async def track(self):
        await self.bot.wait_until_ready()
        req = self.client.stream.statuses.filter.post(follow = list(
            self.configManager.get_field("birds_to_follow").values()
        ))
        async with req as stream:
            async for tweet in stream:
                if peony.events.tweet(tweet):
                    print("test2")
                    user_name = tweet['user']['screen_name']
                    link = tweet['entities']['media'][0]['media_url_https']
                    await self.eventManager.notify(user_name, link)


def setup(bot, eventManager, configManager):
    bot.add_cog(FluffyTwitter(bot, eventManager, configManager))













