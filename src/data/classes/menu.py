from __future__ import annotations

from json import dumps, loads
from typing import (
    Any,
    Dict,
    List,
    Mapping,
    MutableMapping,
    Sequence,
    TYPE_CHECKING,
    Union,
)

import discord
from discord.ext import commands

from ..db import execute_query, execute_read_query
from ..query import get_menu, get_menu_item, insert_interface
from .base import Defaultable, Fetchable, Initable, Makeable, Saveable, Setable


class View(discord.ui.View):
    def __init__(self, *args, **kwargs) -> None:
        self.menu_id = kwargs.pop("menu_id")
        self.bot = kwargs.pop("bot")
        super().__init__(*args, **kwargs)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if TYPE_CHECKING:
            assert isinstance(interaction.message, discord.Message)
        return bool(
            await execute_read_query(
                "SELECT * FROM menu_interfaces WHERE menu_id = $1 AND message_id = $2;",
                self.menu_id,
                interaction.message.id,
            )
        )


class Button(discord.ui.Button):
    def __init__(self, *args, **kwargs) -> None:
        self.action = kwargs.pop("action")
        self.options = kwargs.pop("options")
        super().__init__(*args, **kwargs)

    async def callback(self, interaction: discord.Interaction) -> None:
        # sourcery no-metrics
        from .embassy import Embassy
        from .ticket import Ticket
        from ...funcs import get_embed_author_member
        from ...ref import bot

        if TYPE_CHECKING:
            assert isinstance(interaction.user, discord.Member)
            assert isinstance(interaction.guild, discord.Guild)
        bot_member = interaction.guild.get_member(interaction.application_id)
        if TYPE_CHECKING:
            assert isinstance(bot_member, discord.Member)
        highest_role = bot_member.top_role
        if self.action is None:
            return await interaction.response.defer()
        if self.action in {"ADD_ROLE", "ADD_ROLES"}:
            roles = []
            for role in self.options:
                role = interaction.guild.get_role(role)
                if role is None:
                    continue
                if role < highest_role and role not in interaction.user.roles:
                    roles.append(role)
            if roles:
                await interaction.user.add_roles(*roles)
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        f"Added the following roles: {', '.join(role.mention for role in roles)}",
                    ),
                )
            else:
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        "No roles were added since you have them all already.",
                    ),
                )
        elif self.action in {"REMOVE_ROLE", "REMOVE_ROLES"}:
            roles = []
            for role in self.options:
                role = interaction.guild.get_role(role)
                if role is None:
                    continue
                if role < highest_role and role not in interaction.user.roles:
                    roles.append(role)
            if roles:
                await interaction.user.remove_roles(*roles)
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        f"Removed the following roles from you: {', '.join(role.mention for role in roles)}",
                    ),
                )
            else:
                await interaction.response.send_message(
                    ephemeral=True,
                    embed=get_embed_author_member(
                        interaction.user,
                        "No roles were removed since you you don't have any of them.",
                    ),
                )
        elif self.action in {"CREATE_TICKET", "CREATE_TICKETS"}:
            ...
        elif self.action in {"CLOSE_TICKET", "CREATE_TICKETS"}:
            ...
        elif self.action in {"CREATE_EMBASSY", "CREATE_EMBASSIES"}:
            Ticket
        elif self.action in {"CLOSE_EMBASSY", "CLOSE_EMBASSIES"}:
            ...


class Select(discord.ui.Select):
    async def callback(self, interaction: discord.Interaction) -> None:
        values = self.values.copy()


class SelectOption(discord.SelectOption):
    def __init__(self, *args, **kwargs) -> None:
        self.action = kwargs.pop("action")
        self.options = kwargs.pop("options")
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return f"Label: {self.label} - Description: {self.description} - Emoji: {self.emoji} - Default: {self.default} - Action: {self.action}"


class Menu(Defaultable, Fetchable, Initable, Makeable, Saveable, Setable):
    menu_id: int
    items: Sequence[List[MenuItem]]
    name: str
    description: str
    item_ids: Sequence[Sequence[int]]
    permissions: Mapping[str, Any]

    def __init__(self, data: Dict[str, Any]) -> None:
        self.menu_id = data["menu_id"]
        self.owner_id = data["owner_id"]
        self.name = data["name"]
        self.description = data["description"]
        self.item_ids = loads(data["items"]) if data["items"] else []
        self.permissions = loads(data["permissions"]) if data["permissions"] else {}

    @classmethod
    async def convert(cls, ctx: commands.Context, argument):
        return await cls.fetch(int(argument), ctx.author.id)

    @classmethod
    async def fetch(cls, menu_id: int, owner_id: int) -> Menu:
        try:
            return cls(data=await get_menu(menu_id=menu_id))
        except IndexError:
            return cls.default(menu_id=menu_id, owner_id=owner_id)

    @classmethod
    def default(cls, menu_id: int, owner_id: int) -> Menu:
        menu = cls(
            data={
                "menu_id": menu_id,
                "owner_id": owner_id,
                "name": None,
                "description": None,
                "items": [],
                "permissions": {},
            }
        )
        menu.items = [[], [], [], [], []]
        return menu

    async def _make_items(self) -> None:
        items = []
        for i in self.item_ids:
            if i:
                items.append([(await MenuItem.fetch(j)) for j in i])
            else:
                items.append([])
        self.items = items

    async def set_(self, **kwargs: Mapping[str, Any]) -> Menu:
        sets = [f"{key} = ${e+2}" for e, key in enumerate(kwargs)]
        sets = ", ".join(sets)
        args = tuple(kwargs.values())
        await execute_query(
            f"""
        UPDATE menus SET {sets} WHERE menu_id = $1;
        """,
            self.menu_id,
            *args,
        )
        return self

    async def save(self) -> None:
        await execute_query(
            f"""
        INSERT INTO menus (menu_id, owner_id, name, description, items, permissions) VALUES ($1, $2, $3, $4, $5, $6);
        """,
            self.menu_id,
            self.owner_id,
            self.name,
            self.description,
            dumps([[i.item_id for i in row] for row in self.items])
            if self.items
            else [
                [],
                [],
                [],
                [],
                [],
            ],
            dumps(self.permissions) if self.permissions else None,
        )

    def add_item(self, item: MenuItem, row: int) -> None:
        self.items[row].append(item)

    def remove_item(self, item_id: str) -> None:
        for i in self.items:
            for j in i:
                if j.item_id == item_id:
                    del j

    async def get_view(self) -> View:
        from ...ref import bot

        await self.make_attrs("items")
        self.view = View(bot=bot, menu_id=self.menu_id, timeout=None)
        for index, item_set in enumerate(self.items):
            for item in item_set:
                self.view.add_item(item.get_item(self.menu_id, index))
        return self.view

    def get_description_embed(self, ctx: commands.Context) -> discord.Embed:
        from ...funcs import get_embed_author_guild

        self.embed = get_embed_author_guild(ctx.guild, self.description)
        return self.embed

    async def new_interface(self, message: discord.Message) -> None:
        await insert_interface(menu_id=self.menu_id, message=message)

    def __str__(self) -> str:
        if self.name is None:
            return f"{self.menu_id}"
        return f"{self.menu_id} - {self.name}"


class MenuItem(Fetchable, Initable, Saveable):
    def __init__(self, data: Mapping[str, Any]) -> None:
        self.item_id = data["item_id"]
        self.owner_id = data["owner_id"]
        self.type = data["type_"]
        self.data = loads(data["data_"]) if data["data_"] else {}

    @classmethod
    async def fetch(cls, item_id: int) -> MenuItem:
        return cls(data=await get_menu_item(item_id=item_id))

    def get_item(self, menu_id: int, row: int) -> Union[Button, Select]:
        custom_id = f"{menu_id}-{self.item_id}"
        if self.type == "button":
            return Button(
                style=discord.ButtonStyle[self.data.get("style", "blurple")],
                label=self.data.get("label", None),
                disabled=self.data.get("disabled", False),
                custom_id=custom_id,
                url=self.data.get("url", None),
                emoji=self.data.get("emoji", None),
                row=row,
                action=self.data.get("action", None),
                options=self.data.get("options", []),
            )
        elif self.type == "select":
            return Select(
                custom_id=custom_id,
                placeholder=self.data.get("placeholder", None),
                min_values=self.data.get("min_values", 1),
                max_values=self.data.get("max_values", 1),
                options=[
                    SelectOption(
                        label=option["label"],
                        description=option.get("description", None),
                        emoji=option.get("emoji", None),
                        default=option.get("default", False),
                        action=self.data.get("action", None),
                        options=self.data.get("options", []),
                    )
                    for option in self.data["options"]
                ],
                row=row,
            )
        else:
            raise Exception(f"Unknown item type {self.type}")

    async def save(self) -> None:
        await execute_query(
            f"""
        INSERT INTO menu_items (item_id, owner_id, type_, data_) VALUES ($1, $2, $3, $4);
        """,
            self.item_id,
            self.owner_id,
            self.type,
            dumps(self.data),
        )

    @staticmethod
    def validate_flags(flags: Mapping[str, Any]) -> bool:
        if "action" in flags and flags.get("action", "ADD_ROLE")[0].upper().replace(
            " ", "_"
        ) not in {
            "ADD_ROLE",
            "REMOVE_ROLE",
            "ADD_ROLES",
            "REMOVE_ROLES",
            "CREATE_TICKET",
            "CLOSE_TICKET",
            "CREATE_TICKETS",
            "CLOSE_TICKETS",
            "CREATE_EMBASSY",
            "CLOSE_EMBASSY",
            "CREATE_EMBASSIES",
            "CLOSE_EMBASSIES",
        }:
            return False
        if "style" in flags and flags.get("style", ["red"])[0].lower() not in [
            "primary",
            "secondary",
            "success",
            "danger",
            "link",
            "blurple",
            "grey",
            "gray",
            "green",
            "red",
            "url",
        ]:
            return False
        return True

    @staticmethod
    async def format_flags(
        ctx: commands.Context, flags: Mapping[str, List[Any]]
    ) -> MutableMapping[str, Any]:
        from .ticket import Ticket
        from .embassy import Embassy

        formatted_flags = {}
        if "action" in flags:
            formatted_flags["action"] = flags["action"][0].upper().replace(" ", "_")
        if "style" in flags:
            formatted_flags["style"] = discord.ButtonStyle[flags["style"][0].lower()]
        if "options" in flags:
            formatted_flags["options"] = set()
            for i in flags["options"]:
                for j in i.split(" "):
                    if formatted_flags["action"] in {
                        "ADD_ROLE",
                        "REMOVE_ROLE",
                        "ADD_ROLES",
                        "REMOVE_ROLES",
                    }:
                        formatted_flags["options"].add(
                            (await commands.RoleConverter().convert(ctx, j)).id
                        )
                    elif formatted_flags["action"] in {
                        "CREATE_TICKET",
                        "CLOSE_TICKET",
                        "CREATE_TICKETS",
                        "CLOSE_TICKETS",
                    }:
                        formatted_flags["options"].add(
                            int(await Ticket.convert(ctx, j))
                        )
                    elif formatted_flags["action"] in {
                        "CREATE_EMBASSY",
                        "CLOSE_EMBASSY",
                        "CREATE_EMBASSIES",
                        "CLOSE_EMBASSIES",
                    }:
                        formatted_flags["options"].add(
                            int(await Embassy.convert(ctx, j))
                        )
            formatted_flags["options"] = list(formatted_flags["options"])
        for key, value in flags.items():
            if key not in formatted_flags:
                formatted_flags[key] = value[0]
        return formatted_flags

    def __str__(self) -> str:
        if self.type == "button":
            return f"ID: {self.item_id} - Type: {self.type} - Style: {self.data.get('style', 'blurple').capitalize()} - Label: {self.data.get('label', None)} - Disabled: {self.data.get('disabled', False)} - URL: {self.data.get('url', None)} - Emoji: {self.data.get('emoji', None)} - Row: {self.data.get('row', None)} - Action: {self.data.get('action', None)}"
        if self.type == "select":
            return f"ID: {self.item_id} - Type: {self.type} - Placeholder: {self.data.get('placeholder', None)} - Min Values: {self.data.get('min_values', 1)} - Max Values: {self.data.get('max_values', 1)} - Options: {', '.join(str(option) for option in self.data.get('options', [None]))}"
        return f"ID: {self.item_id} - Type: {self.type}"
