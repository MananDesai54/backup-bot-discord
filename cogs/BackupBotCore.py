import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context


class BackupBotCore(commands.Cog):
    def __init__(self, client: Bot) -> None:
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(
            status=discord.Status.idle,
            activity=discord.Game("Looking for backups"))
        print(f"We have logged in as {self.client.user}")

    # Commands
    @commands.command(aliases=['hello', 'hey'])
    async def ping(self, ctx: Context):
        await ctx.send(f"Pong {round(self.client.latency * 1000)}ms")

    @commands.command()
    async def clear(self, ctx: Context, amount=5):
        await ctx.channel.purge(limit=amount)


def setup(client: Bot):
    client.add_cog(BackupBotCore(client))
