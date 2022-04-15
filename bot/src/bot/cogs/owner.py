from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from discord.utils import MISSING

from ... import funcs
from ...cache import cache
from ...data.classes import Nation, User
from ...env import __version__
from ...errors import EmbedErrorMessage
from ...ref import Rift, RiftContext


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot: Rift):
        self.bot = bot

    async def cog_check(self, ctx: RiftContext):  # type: ignore
        if TYPE_CHECKING:
            assert isinstance(ctx.author, discord.User)
        return await self.bot.is_owner(ctx.author)

    async def cog_command_error(self, ctx: RiftContext, error: Exception):  # type: ignore
        if not isinstance(error, commands.CheckFailure):
            await funcs.handler(ctx, error)

    @commands.command(name="unlink", aliases=["unverify", "remove-link", "removelink"])
    async def unlink(self, ctx: RiftContext, nation: Nation):
        link = cache.get_user(nation.id)
        if link is None:
            raise EmbedErrorMessage(
                ctx.author,
                f"{repr(nation)} is not linked!",
            )
        await link.delete()
        user = self.bot.get_user(link.user_id)
        if not user:
            user = await self.bot.fetch_user(link.user_id)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                user,
                f"{user.mention} has been unlinked from nation `{nation.id}`.",
                color=discord.Color.green(),
            )
        )

    @commands.command(
        name="force-link", aliases=["forcelink", "force-verify", "forceverify"]
    )
    async def force_link(
        self, ctx: RiftContext, nation: Nation, user: discord.User = MISSING
    ):
        member = user or ctx.author
        link = cache.get_user(member.id)
        if link is not None:
            raise EmbedErrorMessage(
                ctx.author,
                f"{member.mention} is already linked!",
            )
        link = cache.get_user(nation.id)
        if link is not None:
            raise EmbedErrorMessage(
                ctx.author,
                f"{repr(nation)} is already linked!",
            )
        await User.create(user, nation)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                member,
                f"Success! {member.mention} is now linked to {repr(nation)}!",
                color=discord.Color.green(),
            )
        )

    @commands.group(name="extension", invoke_without_command=True)
    async def extension(self, ctx: RiftContext):
        raise EmbedErrorMessage(
            ctx.author,
            "You forgot to give a subcommand!",
        )

    @extension.command(name="reload")  # type: ignore
    async def extension_reload(self, ctx: RiftContext, *, extension: str):
        try:
            self.bot.reload_extension(f"source.bot.cogs.{extension}")
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Extension `{extension}` has been reloaded.",
                    color=discord.Color.green(),
                )
            )
        except commands.ExtensionNotLoaded:
            raise EmbedErrorMessage(
                ctx.author,
                f"Extension `{extension}` is not loaded.",
            )
        except commands.ExtensionNotFound:
            raise EmbedErrorMessage(
                ctx.author,
                f"Extension `{extension}` does not exist.",
            )

    @extension.command(name="load")  # type: ignore
    async def extension_load(self, ctx: RiftContext, *, extension: str):
        try:
            self.bot.load_extension(f"source.bot.cogs.{extension}")
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Extension `{extension}` has been loaded.",
                    color=discord.Color.green(),
                )
            )
        except commands.ExtensionAlreadyLoaded:
            raise EmbedErrorMessage(
                ctx.author,
                f"Extension `{extension}` is already loaded.",
            )
        except commands.ExtensionNotFound:
            raise EmbedErrorMessage(
                ctx.author,
                f"Extension `{extension}` does not exist.",
            )

    @extension.command(name="unload")  # type: ignore
    async def extension_unload(self, ctx: RiftContext, *, extension: str):
        try:
            self.bot.unload_extension(f"source.bot.cogs.{extension}")
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    f"Extension `{extension}` has been unloaded.",
                    color=discord.Color.green(),
                )
            )
        except commands.ExtensionNotLoaded:
            raise EmbedErrorMessage(
                ctx.author,
                f"Extension `{extension}` is not loaded.",
            )
        except commands.ExtensionNotFound:
            raise EmbedErrorMessage(
                ctx.author,
                f"Extension `{extension}` does not exist.",
            )

    @commands.command(name="enable-debug", aliases=["debug", "enabledebug"])
    async def enable_debug(self, ctx: RiftContext):
        ctx.bot.enable_debug = not ctx.bot.enable_debug
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Debug mode has been {'enabled' if ctx.bot.enable_debug else 'disabled'}.",
            )
        )

    @commands.command(name="stats")
    async def stats(self, ctx: RiftContext):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                __version__,
                fields=[
                    {"name": "Guilds", "value": f"{len(self.bot.guilds):,}"},
                    {"name": "Users", "value": f"{len(self.bot.users):,}"},
                    {"name": "Latency", "value": f"{self.bot.latency:,}s"},
                    {"name": "Links", "value": f"{len(cache.users):,}"},
                    {
                        "name": "Owners",
                        "value": f"{len({i.owner.id for i in self.bot.guilds if i.owner is not None}):,}",
                    },
                    {
                        "name": "Unique",
                        "value": f"{len({i.owner.id for i in self.bot.guilds if i.owner is not None})/len(self.bot.guilds):,.2%}",
                    },
                ],
            )
        )

    @commands.command(name="guilds")
    async def guilds(self, ctx: RiftContext):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "\n".join(f"{i.name} - {i.member_count}" for i in self.bot.guilds),
                title=f"{len(self.bot.guilds):,} guilds",
            )
        )

    @commands.command(name="owners")
    async def owners(self, ctx: RiftContext):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "\n".join(
                    f"{i.name} - {i.member_count} - <@{i.owner_id}>"
                    for i in self.bot.guilds
                ),
                title=f"{len(self.bot.guilds):,} guilds",
            ),
        )

    @commands.command(name="owner-mentions")
    async def owner_mentions(self, ctx: RiftContext):
        await ctx.reply(
            "".join(f"<@{i.owner_id}>" for i in self.bot.guilds if i.owner is not None),
            allowed_mentions=discord.AllowedMentions(users=False),
        )


def setup(bot: Rift):
    bot.add_cog(Owner(bot))