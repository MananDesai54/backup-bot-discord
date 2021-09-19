from discord.ext.commands.context import Context


def is_it_tester(ctx: Context):
    return ctx.author.id == 866313133308116992
