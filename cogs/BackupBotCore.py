from utils.is_it_tester import is_it_tester
import discord
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from itertools import cycle
from discord.ext.commands.core import command

from discord.ext.commands.errors import CommandError

status = cycle(['>help', "For Backups"])


class BackupBotCore(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        # await self.client.change_presence(
        #     status=discord.Status.idle,
        #     activity=discord.Game("Watching >help"))
        activity = discord.Activity(type=discord.ActivityType.watching,
                                    name=">help")
        await self.client.change_presence(activity=activity)
        self.update_status.start()
        print(f"We have logged in as {self.client.user}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Provide all required arguments")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(
                "Sorry That command not found, Please try >help to get list of commands"
            )
        elif isinstance(error, commands.errors.MissingPermissions):
            await ctx.send(
                "Sorry You do not have Permission to perform that task")
        else:
            print(error.__class__)
            print(error)

    # Commands
    @commands.command(aliases=['hello', 'hey'])
    async def ping(self, ctx: Context):
        await ctx.send(f"Pong {round(self.client.latency * 1000)}ms")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: Context, amount: int):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    @commands.check(is_it_tester)
    async def testBot(self, ctx: Context):
        await ctx.send(f"Hey, {ctx.author} only you can access this")

    # Tasks
    @tasks.loop(seconds=10)
    async def update_status(self):
        activity = discord.Activity(type=discord.ActivityType.watching,
                                    name=next(status))
        await self.client.change_presence(activity=activity)


def setup(client: Bot):
    client.add_cog(BackupBotCore(client))
