import json
from asyncio import TimeoutError
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from ... import funcs
from ...checks import has_manage_permissions
from ...data.classes import Menu, MenuItem
from ...data.query import query_menus_guild
from ...flags import ButtonFlags, SelectFlags, SelectOptionFlags
from ...ref import Rift


class Menus(commands.Cog):
    def __init__(self, bot: Rift):
        self.bot = bot

    @commands.group(
        name="menu",
        aliases=["menus", "role-menu", "rolemenu", "reaction-menu", "reactionmenu"],
        help="A group of commands related to menus.",
        case_insensitive=True,
        invoke_without_command=True,
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def menu(self, ctx: commands.Context, menu: Menu = None):
        # sourcery skip: merge-nested-ifs
        if ctx.invoked_with is not None:
            if ctx.invoked_with.lower() == "menus":
                await self.menu_list.invoke(ctx)
                return
        if menu is None:
            return await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author, "You didn't specify a menu!", color=discord.Color.red()
                )
            )
        if TYPE_CHECKING:
            assert isinstance(menu, Menu)
        await ctx.send(str(menu))
        view = await menu.get_view()
        message = await ctx.reply("View", view=view)
        await menu.new_interface(message)

    @menu.command(
        name="list",
        aliases=["l", "li"],
        help="List the menu configurations for this guild.",
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def menu_list(self, ctx: commands.Context):
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        menus = await query_menus_guild(guild_id=ctx.guild.id)
        menus = [Menu(data=i) for i in menus]
        if menus:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "\n".join(str(i) for i in menus),
                    color=discord.Color.blue(),
                )
            )
        else:
            await ctx.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author, "You don't have any menus!", color=discord.Color.red()
                )
            )

    @menu.command(
        name="create",
        aliases=["new"],
        help="Create a new menu configuration.",
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def menu_create(
        self, ctx: commands.Context, *, description: str = None
    ):  # sourcery no-metrics
        message: discord.Message
        if TYPE_CHECKING:
            assert isinstance(ctx.guild, discord.Guild)
        menu = Menu.default(ctx.interaction.id, ctx.guild.id)
        menu.description = (
            description
            or "This is a menu! Someone was lazy and didn't put a description. :)"
        )
        main_message = await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                "Waiting for followup messages to assemble a menu...",
                color=discord.Color.blue(),
            ),
            return_message=True,
        )
        try:
            running = True
            while running:
                message = await self.bot.wait_for(
                    "message",
                    check=lambda message: message.author.id == ctx.author.id
                    and message.channel.id == ctx.channel.id,
                    timeout=300,
                )
                lower = message.content.lower()
                if (
                    lower.startswith("finish")
                    or lower.startswith("cancel")
                    or lower.startswith("complete")
                    or lower.startswith("done")
                ):
                    running = False
                    continue
                if lower.startswith("button "):
                    flags = ButtonFlags.parse_flags(message.content[7:])
                    row = await funcs.utils.get_row(
                        message, "button", flags, menu.items
                    )
                    if row is None:
                        continue
                    if "id" in flags:
                        try:
                            if TYPE_CHECKING:
                                assert isinstance(flags["id"], str)
                            item = await MenuItem.fetch(int(flags["id"]), ctx.guild.id)
                            if item.guild_id == ctx.author.id:
                                menu.add_item(item, row)
                                continue
                        except IndexError:
                            pass
                    if not MenuItem.validate_flags(flags):
                        await ctx.reply(
                            embed=funcs.get_embed_author_member(
                                ctx.author, "Invalid item.", color=discord.Color.red()
                            )
                        )
                        continue
                    flags = await MenuItem.format_flags(ctx, flags)
                    item = MenuItem(
                        {
                            "item_id": message.id,
                            "guild_id": ctx.guild.id,
                            "type_": "button",
                            "data_": flags,
                        }
                    )
                    menu.add_item(item, row)
                elif lower.startswith("select "):
                    flags = SelectFlags.parse_flags(message.content[7:])
                    row = await funcs.utils.get_row(
                        message, "select", flags, menu.items
                    )
                    if row == -1:
                        continue
                    while True:
                        message = await self.bot.wait_for(
                            "message",
                            check=lambda message: message.author.id == ctx.author.id
                            and message.channel.id == ctx.channel.id,
                            timeout=300,
                        )
                        lower = message.content.lower()
                        if lower.startswith(
                            ("finish", "cancel", "complete", "done", "save")
                        ):
                            break
                        if lower.startswith("option "):
                            flags = SelectOptionFlags.parse_flags(message.content[7:])
            else:
                if not any(menu.items):
                    return await ctx.reply(
                        embed=funcs.get_embed_author_member(
                            ctx.author,
                            "You didn't add any items!",
                            color=discord.Color.red(),
                        )
                    )
                for row in menu.items:
                    for item in row:
                        await item.save()
                await menu.save()
                await main_message.reply(
                    embed=funcs.get_embed_author_member(
                        ctx.author,
                        f"Menu ID: {menu.menu_id}\n\n"
                        + "\n\n".join(str(j) for i in menu.items for j in i),
                        color=discord.Color.green(),
                    )
                )
        except TimeoutError:
            await main_message.reply(
                embed=funcs.get_embed_author_member(
                    ctx.author,
                    "Menu creation timed out. Please try again.",
                    color=discord.Color.red(),
                )
            )

    @menu.command(
        name="send",
        aliases=["post"],
        help="Send a menu configuration to a channel.",
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def menu_send(
        self, ctx: commands.Context, menu: Menu, *, channel: discord.TextChannel
    ):
        view = await menu.get_view()
        embed = menu.get_description_embed(ctx)
        message = await channel.send(embed=embed, view=view)
        await menu.new_interface(message)
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Menu {menu.menu_id} sent to {channel.mention}!",
                color=discord.Color.green(),
            ),
            ephemeral=True,
        )

    @menu.command(
        name="info",
        aliases=["details"],
        help="Get information about a menu configuration.",
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def menu_info(self, ctx: commands.Context, *, menu: Menu):
        await menu._make_items()
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                f"Menu ID: {menu.menu_id}\n\n"
                "\n\n".join(str(j) for i in menu.items for j in i),
                color=discord.Color.green(),
            )
        )

    @menu.command(
        name="item",
        aliases=["items"],
        help="Get information about a menu item.",
        type=commands.CommandType.chat_input,
    )
    @commands.guild_only()
    @has_manage_permissions()
    async def menu_item(self, ctx: commands.Context, *, item: MenuItem):
        await ctx.reply(
            embed=funcs.get_embed_author_member(
                ctx.author,
                str(item) + f"\nOptions: {None if (o := item.data.get('options', None)) is not None else ', '.join(r.mention for i in o if(r := ctx.guild.get_role(i))) if item.data.get('action') in {'ADD_ROLE', 'REMOVE_ROLE', 'ADD_ROLES', 'REMOVE_ROLES'} else ', '.join(str(i) for i in o)}",  # type: ignore
                color=discord.Color.green(),
            )
        )


def setup(bot: Rift):
    bot.add_cog(Menus(bot))
