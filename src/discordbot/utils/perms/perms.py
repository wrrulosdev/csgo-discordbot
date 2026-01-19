import discord


class PermsCheck:
    @staticmethod
    def is_admin(interaction: discord.Interaction) -> bool:
        """
        Checks if the user has administrator permissions in the guild.
        :param interaction: The Discord interaction object.
        :return: True if the user has administrator permissions, False otherwise.
        """
        if interaction.user.guild_permissions.administrator:
            return True

        return False

    @staticmethod
    def is_from_dm(interaction: discord.Interaction) -> bool:
        """
        Check if the interaction is from a DM (Direct Message) channel.
        :param interaction: The interaction object.
        :return: Whether the interaction is from a DM channel.
        """
        return isinstance(interaction.channel, discord.DMChannel)
