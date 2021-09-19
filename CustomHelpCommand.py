import discord
from discord.ext import commands


class Help(commands.HelpCommand):
    def __init__(self, **options):
        super().__init__(**options)

    async def send_bot_help(self, mapping):
        return await super().send_bot_help(mapping)

    async def send_cog_help(self, cog):
        return await super().send_cog_help(cog)

    async def send_command_help(self, command):
        return await super().send_command_help(command)

    async def send_error_message(self, error):
        return await super().send_error_message(error)

    async def send_group_help(self, group):
        return await super().send_group_help(group)