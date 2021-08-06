import os

env = os.environ.get("ENV", "development")

if env == "development":
    from .development import *
elif env == "production":
    from .production import *
