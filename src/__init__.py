import subprocess
import sys

import discord
from discord.ext.commands import Bot
from tongopy import load_language, set_language, translate_message
from loguru import logger

from src.constants import BotConstants
from src.discordbot.bot import DiscordBot


class CSGODiscordBot:
    def __init__(self) -> None:
        subprocess.run('clear || cls', shell=True)
        self._bot: Bot = DiscordBot.create_bot(
            command_prefix='!!!!!!!#!!!!!!',
            help_command=None,
            intents=discord.Intents.all()
        )
        self._start_bot()

    @logger.catch
    def _logger_setup(self) -> None:
        """
        Configures the Loguru logger for the application.
        Sets up the log file, format, retention, rotation, and enables queueing for thread safety.

        :return: None
        """
        logger.add(
            'debug.log',
            format='[{time:YYYY-MM-DD HH:mm:ss} {level} - {file}, {line}] ⮞ <level>{message}</level>',
            retention='16 days',
            rotation='12:00',
            enqueue=True
        )

    @logger.catch
    def _start_bot(self) -> None:
        """
        Starts the Discord bot using the provided token from BotConstants.

        :return: None
        """
        self._bot.run(BotConstants.TOKEN)