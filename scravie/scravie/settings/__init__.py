import os


current_environment = os.getenv("ENVIRONMENT_SETTINGS")

if current_environment == "PRODUCTION":
    from scravie.settings.production import *
elif current_environment == "DEVELOPMENT":
    from scravie.settings.development import *
elif current_environment == "STAGING":
    from scravie.settings.staging import *
