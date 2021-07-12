import sys
import traceback

import discord
from discord.ext import commands

from .embeds import get_embed_author_member
from .utils import get_command_signature


async def print_handler(ctx, error):
    if hasattr(ctx.command, "on_error"):
        return
    cog = ctx.cog
    print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


async def handler(ctx, error):
    try:
        if isinstance(error, commands.CommandInvokeError):
            error = error.original
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"You forgot an argument!\n\n`{await get_command_signature(ctx)}`",
                )
            )
        elif isinstance(error, discord.Forbidden):
            await ctx.reply(
                'I don\'t have permission to do that! Please make sure I have the "Embed Links" permission.'
            )
        elif isinstance(error, commands.MemberNotFound):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author, "I couldn't find that member!"
                )
            )
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    f"You gave an invalid argument!\n\n`{await get_command_signature(ctx)}`",
                )
            )
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    "You can't use that command in DMs! Try it in a server instead.",
                )
            )
        elif isinstance(error, commands.PrivateMessageOnly):
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    "You can't use that command in a server! Try it in DMs instead.",
                )
            )
        else:
            await ctx.reply(
                embed=get_embed_author_member(
                    ctx.author,
                    "Unknown Fatal Error. Please try again. If this problem persists please contact <@!258298021266063360> for assistance.\nPlease remember the bot is still in Alpha, there is a good chance new features may result in new bugs to older features. To report an issue please send a message to <@!258298021266063360> so it can be addressed as soon as possible.",
                )
            )
            await print_handler(ctx, error)
    except discord.Forbidden:
        await ctx.reply(
            'I don\'t have permission to do that! Please make sure I have the "Embed Links" permission.'
        )