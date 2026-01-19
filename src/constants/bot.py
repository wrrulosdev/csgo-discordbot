from src.utilities import EnvManager


class BotConstants:
    TOKEN: str = EnvManager.get("DISCORD_TOKEN")
    GUILD_ID: int = int(EnvManager.get("DISCORD_GUILD_ID"))
    COG_PATH: str = 'src.discordbot.cogs'
    COGS_PATH: str = 'src/discordbot/cogs'
    AUTOROLES_CHANNEL_ID: str = int(EnvManager.get("AUTOROLES_CHANNEL_ID"))
    ROLES_AUTOROLES_MESSAGE_ID: str = EnvManager.get("ROLES_AUTOROLES_MESSAGE_ID")
    PREMIER_AUTOROLES_MESSAGE_ID: str = EnvManager.get("PREMIER_AUTOROLES_MESSAGE_ID")
    FACEIT_AUTOROLES_MESSAGE_ID: str = EnvManager.get("FACEIT_AUTOROLES_MESSAGE_ID")
