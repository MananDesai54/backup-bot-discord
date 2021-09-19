import discord
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from itertools import cycle

from discord.ext.commands.errors import CommandError

status = cycle(['Looking for Backups', "Restoring Backups"])


class BackupBotCore(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(
            status=discord.Status.idle,
            activity=discord.Game("Looking for backups"))
        self.update_status.start()
        print(f"We have logged in as {self.client.user}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Provide all required arguments")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(
                "Sorry That command not found, Please try $help to get list of commands"
            )
        else:
            print(error)

    # Commands
    @commands.command(aliases=['hello', 'hey'])
    async def ping(self, ctx: Context):
        await ctx.send(f"Pong {round(self.client.latency * 1000)}ms")

    @commands.command()
    async def clear(self, ctx: Context, amount: int):
        await ctx.channel.purge(limit=amount)

    # Tasks
    @tasks.loop(seconds=10)
    async def update_status(self):
        await self.client.change_presence(activity=discord.Game(next(status)))


def setup(client: Bot):
    client.add_cog(BackupBotCore(client))
