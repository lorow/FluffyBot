import hikari
import tanjun

from Core.Config.ConfigManager import ConfigManager


class FluffyBot(tanjun.Client):
    def __init__(self):
        self.config_manager = ConfigManager()
        hikari_bot = hikari.GatewayBot(token=self.config_manager.get_field("bot_token"))

        super(FluffyBot, self).__init__(
            rest=hikari_bot.rest,
            cache=hikari_bot.cache,
            events=hikari_bot.event_manager,
            shard=hikari_bot,
            event_managed=True,
            mention_prefix=False,
            set_global_commands=self.config_manager.get_field("guild", True),
        )

        self.set_human_only()
        self.set_hikari_trait_injectors(hikari_bot)
        hikari_bot.run()
