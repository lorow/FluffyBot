import os
from dotenv import load_dotenv

load_dotenv()

environment = os.environ.get("environment")
owner_id = os.environ.get("owner_id")
bot_token = os.environ.get("bot_token")

description = "This bot is full of fluff! It is literally made out of it! No but honestly if you are looking for the most retarded bot in the universe you have come to the right place."

default_status = "//help for a list of commands"
command_prefix = "//"
imgur_client_id = os.environ.get("imgur_token")
imgur_client_secret = os.environ.get("imgur_secret")
consumer_key = os.environ.get("twitter_consumer", None)
consumer_secret = os.environ.get("twitter_secret", None)
access_token = os.environ.get("twitter_access", None)
access_token_secret = os.environ.get("twitter_access_secret", None)
google_id = os.environ.get("google_id")

extensions = {
    "fun": "Cogs.Fun_commands",
    "derpiBooru": "Cogs.DerpiBooru",
    "e926": "Cogs.e926",
    "reddit": "Cogs.Reddit",
    "google": "Cogs.googlemodule",
    "wikipedia": "Cogs.wikipedia",
    "useful": "Cogs.useful_commands",
    "tags": "Cogs.tags",
    "greetingModule": "Cogs.GreetingModule",
    "twitter": "Cogs.Twitter.TwitterManager",
    "music": "Cogs.MusicModule",
    "hourly_fox": "Cogs.HourlyFox",
}

# that's a must be last extension therefore it's added separately
extensions.update({
    "help": "Cogs.HelpModule",
})

dependencies = {
    "event_manager": "Core.Events.FluffyEventSystem",
}

storage = {}

birds_to_follow = {}
