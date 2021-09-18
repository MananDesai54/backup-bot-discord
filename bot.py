#!/usr/bin/env python3

if __name__ == "__main__":

    import discord
    from discord.ext import commands
    import os
    from dotenv import load_dotenv
    from setUpMongo import connectMongoDB, Backup, Channel, Role

    load_dotenv()

    client = commands.Bot(command_prefix='$')

    connectMongoDB()

    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")

    @client.command()
    async def ping(ctx: commands.Context):
        await ctx.send("Pong")

    client.run(os.getenv('DISCORD_TOKEN'))
