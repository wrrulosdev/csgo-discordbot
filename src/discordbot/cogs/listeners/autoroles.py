from typing import Optional

from discord import RawReactionActionEvent, Guild, PartialEmoji, Message, Role, TextChannel, Emoji
from discord.member import Member
from discord.ext import commands
from discord.ext.commands import Bot
from loguru import logger

from src.constants import BotConstants


class AutoRolesListener(commands.Cog):
    ROLES: dict[str, dict[str, int]] = {
        BotConstants.ROLES_AUTOROLES_MESSAGE_ID: {
            1462761771076030475: 1462259164381450411,  # Awper
            "🧠": 1462258609885941863,  # IGL
            "🚪": 1462259199315808562,  # Entry Fragger
            "🛠️": 1462259261785640960,  # Support
            "🕶️": 1462259288272670862,  # Lurker
        },
        BotConstants.FACEIT_AUTOROLES_MESSAGE_ID: {
            1462765370380128337: 1462763603013668874,  # 1
            1462765387547541515: 1462763764439978065,  # 2
            1462765402277941320: 1462763782907629568,  # 3
            1462765416584712360: 1462763816243826709,  # 4
            1462765429469610165: 1462763837374595132,  # 5
            1462765446242500671: 1462763972838293602,  # 6
            1462765462176796736: 1462763993449107489,  # 7
            1462765479792869438: 1462764008967897181,  # 8
            1462765494229667872: 1462764025858494607,  # 9
            1462765510713278587: 1462764048390291516,  # 10
            1462765566736728218: 1462764068694790149,  # Challenger
        },
        BotConstants.PREMIER_AUTOROLES_MESSAGE_ID: {
            1462734115060187200: 1462259803597308078,  # 0 to 5k premier
            1462734228876951586: 1462259916176625938,  # 5k to 10k premier
            1462734277623156860: 1462259974175457454,  # 10k to 15k premier
            1462734308090450113: 1462260073442312467,  # 15k to 20k premier
            1462734344006275094: 1462260101271388353,  # 20k to 25k premier
            1462734374125572179: 1462260159064576153,  # 25k to 30k premier
            1462734416328786023: 1462260187099562267,  # 30k premier
        }
    }

    def __init__(self, bot: Bot):
        """
        Initializes the AutoRolesListener cog.

        :param bot: The Discord bot instance.
        """
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Ensures that all autorole messages contain the required reactions.
        Runs when the bot becomes ready and connected to Discord.
        """
        logger.info("AutoRolesListener is ensuring bot reactions...")
        channel_id: int = int(BotConstants.AUTOROLES_CHANNEL_ID)

        for guild in self.bot.guilds:
            channel: Optional[TextChannel] = guild.get_channel(channel_id)

            if channel is None:
                logger.critical(f'Channel {channel_id} not found in guild {guild.name}')
                continue

            for message_id, emojis in self.ROLES.items():
                try:
                    message: Message = await channel.fetch_message(int(message_id))

                except Exception as e:
                    logger.warning(
                        f'Could not fetch message {message_id} in channel {channel.name}: {e}'
                    )
                    continue

                for emoji_id in emojis.keys():
                    emoji: Optional[Emoji] = (
                        guild.get_emoji(emoji_id)
                        if isinstance(emoji_id, int)
                        else emoji_id
                    )

                    if emoji is None:
                        logger.warning(
                            f'Emoji ID {emoji_id} not found in guild {guild.name}, skipping...'
                        )
                        continue

                    if not any(r.emoji.id == emoji.id and r.me for r in message.reactions):
                        try:
                            await message.add_reaction(emoji)
                            logger.info(
                                f'Added missing reaction {emoji.name} to message {message_id}'
                            )

                        except Exception as e:
                            logger.warning(
                                f'Could not add reaction {emoji_id} to message {message_id}: {e}'
                            )

    @commands.Cog.listener()
    @logger.catch
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent) -> None:
        """
        Handles reaction additions on autorole messages.
        Assigns the corresponding role to the reacting user.

        :param payload: The raw reaction event payload.
        """
        if str(payload.message_id) not in self.ROLES or payload.user_id == self.bot.user.id:
            return

        guild: Guild = self.bot.get_guild(payload.guild_id)

        if guild is None:
            logger.critical(f'Guild with ID {payload.guild_id} could not be found!')
            return

        user: Optional[Member] = guild.get_member(payload.user_id)

        if user is None:
            logger.critical(
                f'User {payload.user_id} could not be retrieved from autoroles listener'
            )
            return

        await self.reaction_check(user, payload.emoji, payload, guild, add=True)

    @commands.Cog.listener()
    @logger.catch
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent) -> None:
        """
        Handles reaction removals on autorole messages.
        Removes the corresponding role from the user.

        :param payload: The raw reaction event payload.
        """
        if str(payload.message_id) not in self.ROLES or payload.user_id == self.bot.user.id:
            return

        guild: Guild = self.bot.get_guild(payload.guild_id)

        if guild is None:
            logger.critical(f'Guild with ID {payload.guild_id} could not be found!')
            return

        user: Optional[Member] = guild.get_member(payload.user_id)

        if user is None:
            logger.critical(
                f'User {payload.user_id} could not be retrieved from autoroles listener'
            )
            return

        await self.reaction_check(user, payload.emoji, payload, guild, add=False)

    async def reaction_check(
        self,
        user: Member,
        emoji: PartialEmoji,
        payload: RawReactionActionEvent,
        guild: Guild,
        add: bool = True
    ) -> None:
        """
        Validates the reaction and applies or removes the corresponding role.

        If the emoji does not match any configured role, the reaction is removed.

        :param user: The member who reacted.
        :param emoji: The emoji used in the reaction.
        :param payload: The raw reaction event payload.
        :param guild: The guild where the reaction occurred.
        :param add: Whether to add or remove the role.
        """
        message_roles: Optional[dict[str, int]] = self.ROLES.get(str(payload.message_id))

        if not message_roles:
            return

        emoji_id = emoji.id if emoji.id else str(emoji)
        role_id = message_roles.get(emoji_id)

        if not role_id:
            if not add:
                return

            message: Message = await guild.get_channel(
                payload.channel_id
            ).fetch_message(payload.message_id)
            await message.remove_reaction(emoji, user)
            return

        role: Optional[Role] = guild.get_role(role_id)

        if role is None:
            logger.critical(
                f'The role with ID {role_id} ({emoji_id}) was not found in guild {guild.name}'
            )
            return

        if not add:
            await user.remove_roles(role)
            logger.info(f'Removed role {role.name} from {user.name}')
            return

        await user.add_roles(role)
        logger.info(f'Added role {role.name} to {user.name}')


async def setup(bot: commands.Bot) -> None:
    """
    Adds the AutoRolesListener cog to the bot.

    :param bot: The Discord bot instance.
    """
    await bot.add_cog(AutoRolesListener(bot))
