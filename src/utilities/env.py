import os
import sys

from loguru import logger

from dotenv import load_dotenv

load_dotenv()


class EnvManager:
    _loaded: bool = False
    _env: dict[str, str] = {}
    REQUIRED_ENV_VARS: list[str] = [
        "DISCORD_TOKEN",
        "DISCORD_GUILD_ID",
        'AUTOROLES_CHANNEL_ID',
        "ROLES_AUTOROLES_MESSAGE_ID",
        "PREMIER_AUTOROLES_MESSAGE_ID",
        "FACEIT_AUTOROLES_MESSAGE_ID"
    ]

    @classmethod
    def load(cls) -> None:
        """
        Loads and validates required environment variables.
        If any required variable is missing, logs a critical error and exits the program.

        :return: None
		"""
        if cls._loaded:
            return

        missing: list[str] = []

        for var in cls.REQUIRED_ENV_VARS:
            value = os.environ.get(var)

            if not value:
                missing.append(var)

            else:
                cls._env[var] = value

        if missing:
            logger.critical(f'Missing required environment variables: {", ".join(missing)}')
            sys.exit(1)

        cls._loaded = True

    @classmethod
    def get(cls, key: str) -> str:
        """
        Gets the value of a managed environment variable.

        :param key: The environment variable key.
        :return: The value of the environment variable.
        :raises KeyError: If the environment variable is not managed.
        """
        if not cls._loaded:
            cls.load()

        try:
            return cls._env[key]

        except KeyError:
            raise KeyError(f'Environment variable "{key}" is not managed by EnvManager')