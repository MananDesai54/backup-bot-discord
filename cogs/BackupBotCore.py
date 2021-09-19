from utils.file_operation import read_from_file, write_to_file
from discord.abc import GuildChannel
from utils.is_it_tester import is_it_tester
import discord
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from itertools import cycle

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
    async def on_guild_join(self, guild: GuildChannel):
        prefixes = read_from_file('data/prefix.json')
        prefixes[str(guild.id)] = '>'
        write_to_file('data/prefix.json', prefixes)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: GuildChannel):
        prefixes = read_from_file('data/prefix.json')
        prefixes.pop(str(guild.id))
        write_to_file('data/prefix.json', prefixes)

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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx: Context, new_prefix):
        prefixes = read_from_file('data/prefix.json')
        prefixes[str(ctx.guild.id)] = new_prefix
        write_to_file('data/prefix.json', prefixes)
        await ctx.send(f"Prefix Changed to {new_prefix}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(read_message_history=True)
    async def create(self, ctx: Context, type="database", custom=""):
        await ctx.send("Creating Backup...")
        channels = list(self.client.get_all_channels())
        text_data = {}
        voice_data = {}
        category_data = {}
        stage_data = {}
        for channel in channels:
            if isinstance(channel, discord.TextChannel):
                text_data[channel.id] = {
                    'channel_id': channel.id,
                    'channel_name': channel.name,
                    'category_name': channel.category,
                    'category_id': channel.category_id,
                    'messages': []
                }
                async for msg in channel.history(limit=None,
                                                 oldest_first=True):
                    text_data[channel.id]['messages'].append(
                        {'content': msg.content})
            elif isinstance(channel, discord.VoiceChannel):
                voice_data[channel.id] = {
                    'channel_id': channel.id,
                    'channel_name': channel.name,
                    'category_name': channel.category,
                    'category_id': channel.category_id,
                }
            elif isinstance(channel, discord.CategoryChannel):
                category_data[channel.id] = {
                    'channel_id': channel.id,
                    'channel_name': channel.name
                }
            elif isinstance(channel, discord.StageChannel):
                stage_data[channel.id] = {
                    'channel_id': channel.id,
                    'channel_name': channel.name,
                    'category_name': channel.category,
                    'category_id': channel.category_id,
                }
        await ctx.send("Backup Created.")

    # Tasks
    @tasks.loop(seconds=10)
    async def update_status(self):
        activity = discord.Activity(type=discord.ActivityType.watching,
                                    name=next(status))
        await self.client.change_presence(activity=activity)


def setup(client: Bot):
    client.add_cog(BackupBotCore(client))
