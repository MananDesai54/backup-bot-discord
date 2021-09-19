from utils.file_operation import read_from_file
from discord.ext.commands.bot import Bot
from discord.message import Message


def get_prefix(client: Bot, message: Message):
    prefixes = read_from_file('data/prefix.json')
    return prefixes[str(message.guild.id)]
