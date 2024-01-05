"""Override the Default Help Command"""
import discord
from discord.ext.commands import HelpCommand


class MyHelpCommand(HelpCommand):
    """Custom Help Command"""

    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        """

        @param mapping:
        @return:
        """
        prefix = self.context.prefix
        embed = discord.Embed(
            title="My Bot Help",
            description="Here are the available commands:",
            color=discord.Color.blue(),
        )

        for cog, commands in mapping.items():
            if cog:
                command_signatures = [
                    f"**``{prefix}{command.name}``**: {command.short_doc}"
                    for command in commands
                    if command.short_doc
                ]
                cog_name = cog.qualified_name
                embed.add_field(
                    name=cog_name, value="\n".join(command_signatures), inline=False
                )
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        """

        @param command:
        @return:
        """
        prefix = self.context.prefix
        command_signature = f"{prefix}{command.name}"
        embed = discord.Embed(
            title=f"Help for `{command_signature}`",
            description=command.help,
            color=discord.Color.blue(),
        )
        await self.get_destination().send(embed=embed)
