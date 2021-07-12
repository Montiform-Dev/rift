from __future__ import annotations
from ...checks import has_manage_permissions

from typing import TYPE_CHECKING

import discord
from discord import NotFound
from discord.ext import commands
from discord.guild import Guild

from ... import funcs
from ...data.classes import GuildSettings
from ...data.classes import Nation


if TYPE_CHECKING:
    from ...ref import Rift


class Settings(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="user-settings",
        aliases=["us", "usersettings", "my-settings", "mysettings"],
        invoke_without_command=True,
    )
    async def user_settings(self, ctx: commands.Context):
        ...

    @commands.group(
        name="server-settings",
        aliases=["ss", "serversettings", "settings"],
        invoke_without_command=True,
    )
    @commands.guild_only()
    async def server_settings(self, ctx: commands.Context):
        ...

    @server_settings.command(name="purpose", aliases=["p"])
    async def server_settings_purpose(self, ctx: commands.Context):
        ...

    @server_settings.command(name="welcome-message", aliases=["wm", "welcomemessage"])
    @has_manage_permissions()
    async def server_settings_welcome_messge(
        self, ctx: commands.Context, message: str = None
    ):
        settings = await GuildSettings.fetch(str(ctx.guild.id), "welcome_settings")
        message = message.strip("\n ")
        await settings.welcome_settings.set_(welcome_message=message)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                description=f"The welcome message has been set to:\n\n{message}",
            )
        )

    @server_settings.command(
        name="verified-nickname", aliases=["vn", "verifiednickname"]
    )
    @has_manage_permissions()
    async def server_settings_verified_nickname(
        self, ctx: commands.Context, nickname: str = None
    ):
        settings = await GuildSettings.fetch(str(ctx.guild.id), "welcome_settings")
        message = nickname.strip("\n ")
        await settings.welcome_settings.set_(verified_nickname=nickname)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                description=f"The verified nickname format has been set to:\n\n`{nickname}`",
            )
        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # sourcery skip: merge-nested-ifs
        if member.pending:
            return
        try:
            nation = await funcs.get_link_user(member.id)
            nation = int(nation[1])
            nation: Nation = await Nation.fetch(nation)
            await nation.make_attrs("alliance")
        except IndexError:
            nation = None
        settings = await GuildSettings.fetch(str(member.guild.id), "welcome_settings")
        settings = settings.welcome_settings
        if settings.welcome_channels:
            for channel in settings.welcome_channels:
                try:
                    channel = await self.bot.fetch_channel(channel)
                except NotFound:
                    continue
                try:
                    embed = settings.format_welcome_embed(member, bool(nation))
                    await channel.send(embed=embed)
                except discord.Forbidden:
                    try:
                        await channel.send(
                            f"Something went wrong welcoming {member.mention} to the server!"
                        )
                    except discord.Forbidden:
                        continue
            roles: list[discord.Role] = []
            highest_role: discord.Role = member.guild.get_member(
                self.bot.user.id
            ).top_role
            for role in settings.join_roles:
                role: discord.Role = member.guild.get_role(role)
                if highest_role > role:
                    roles.append(role)
            if roles:
                await member.add_roles(*roles)
            roles = []
            if nation:
                if settings.verified_nickname:
                    if member.guild.get_member(
                        self.bot.user.id
                    ).guild_permissions.manage_nicknames:
                        await settings.set_verified_nickname(member, nation)
                roles = []
                for role in settings.verified_roles:
                    role: discord.Role = member.guild.get_role(role)
                    if highest_role > role:
                        roles.append(role)
                if roles:
                    await member.add_roles(*roles)
                roles = []
                ...  # implement the rest of the welcome stuff below, will need to set up alliance settings and embassies first though

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.pending and not after.pending:
            await self.on_member_join(after)


def setup(bot: Rift):
    bot.add_cog(Settings(bot))