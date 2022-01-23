from __future__ import annotations

import time
from datetime import datetime
from typing import TYPE_CHECKING, List

import discord

from .. import funcs
from ..cache import cache
from ..ref import ID

__all__ = ("TreasuresView",)

if TYPE_CHECKING:
    from _typings import Field


class TreasuresView(discord.ui.View):
    def __init__(self, page: int = 1) -> None:
        super().__init__(timeout=None)
        if page == 1:
            self.one.disabled = True  # type: ignore
        else:
            self.two.disabled = True  # type: ignore

    async def callback(
        self,
        button: discord.ui.Button[discord.ui.View],
        interaction: discord.Interaction,
        page: int,
    ):
        if TYPE_CHECKING:
            assert isinstance(interaction.message, discord.Message)
            assert isinstance(interaction.user, (discord.Member, discord.User))
        if interaction.message.author.id != ID:
            return
        desc: str = interaction.message.embeds[0].description[7:]  # type: ignore
        page = page or int(desc[: desc.index("**")])
        if page == 1:
            self.one.disabled = True  # type: ignore
            self.two.disabled = False  # type: ignore
        else:
            self.two.disabled = True  # type: ignore
            self.one.disabled = False  # type: ignore
        fields: List[Field] = [
            {
                "name": i.name,
                "value": f"Color: {i.color.capitalize()}\nBonus: %{i.bonus}\nSpawn Date: <t:{int(time.mktime(datetime.fromisoformat(i.spawn_date).timetuple()))}:D>\nNation: [{i.nation}](https://politicsandwar.com/nation/id={i.nation_id})",
            }
            for i in list(cache.treasures)[(page - 1) * 15 : page * 15]
        ]
        embed = funcs.get_embed_author_member(
            interaction.user,  # type: ignore
            f"Page **{page}** of **2**",
            fields=fields,
            color=discord.Color.blue(),
        )
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(  # type: ignore
        custom_id="MYUVf8qSrCsSq78nyHcRSWuhWWlsUerBSVYFxqgQcvF2gVoTEd9OqtP3Kaa51B4rMgbVfTlvkGOAPgn3",
        label="Page 1",
        style=discord.ButtonStyle.gray,
    )
    async def one(
        self,
        button: discord.ui.Button[discord.ui.View],
        interaction: discord.Interaction,
    ):
        await self.callback(button, interaction, 1)

    @discord.ui.button(  # type: ignore
        custom_id="HipBhbpcigjQwysxH6yqHUUl2BOFJvsm3CmJHQs3ZsLY1aA5qJdHBI67u7jgY5Aq21fzbzlABU1lO3GH",
        label="Refresh",
        style=discord.ButtonStyle.gray,
    )
    async def refresh(
        self,
        button: discord.ui.Button[discord.ui.View],
        interaction: discord.Interaction,
    ):
        await self.callback(button, interaction, 0)

    @discord.ui.button(  # type: ignore
        custom_id="xMV8GXEACJcmvhFtTVKIa3M41IT38RCewSq14n62e7OVASX5U6pfMnBAyFmrkmVGPhPsvXK60ggVdngp",
        label="Page 2",
        style=discord.ButtonStyle.gray,
    )
    async def two(
        self,
        button: discord.ui.Button[discord.ui.View],
        interaction: discord.Interaction,
    ):
        await self.callback(button, interaction, 2)