#!/usr/bin/env python3
from utils.get_prefix import get_prefix
from discord.ext import commands
import os
from dotenv import load_dotenv
from setUpMongo import connectMongoDB, Backup, Channel, Role
from CustomHelpCommand import Help
from discord.ext.commands.context import Context
from discord.ext.commands.core import command

if __name__ == "__main__":

    load_dotenv()

    client = commands.Bot(command_prefix=get_prefix)

    # Load/Unload Cog
    # to use run `$load filename(without .py) from cogs folder`
    @client.command()
    async def load(ctx: Context, extension):
        client.load_extension(f"cogs.{extension}")

    # to use run `$unload filename(without .py) from cogs folder`
    @client.command()
    async def unload(ctx: Context, extension):
        client.unload_extension(f"cogs.{extension}")

    for filename in os.listdir('./cogs'):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")

    # to use run `$reload filename(without .py) from cogs folder`
    @client.command()
    async def reload(ctx: Context, extension):
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")

    # connectMongoDB()

    client.run(os.getenv('DISCORD_TOKEN'))
