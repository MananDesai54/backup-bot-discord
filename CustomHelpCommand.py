import discord
from discord.ext import commands

# class CustomHelpCommand(commands.HelpCommand):
#     def __init__(self, **options):
#         super().__init__(**options)

#     async def send_bot_help(self, mapping):
#         destination = self.get_destination()
#         e = discord.Embed(color=discord.Color.blurple(), description='')
#         for page in self.paginator.pages:
#             e.description += page
#         await destination.send(embed=e)

#     async def send_cog_help(self, cog):
#         return await super().send_cog_help(cog)

#     async def send_command_help(self, command):
#         return await super().send_command_help(command)

#     async def send_error_message(self, error):
#         return await super().send_error_message(error)

#     async def send_group_help(self, group):
#         return await super().send_group_help(group)


class CustomHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Color.blurple(), description='')
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)