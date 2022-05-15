from __future__ import annotations

from typing import TYPE_CHECKING

from .. import consts, strings, utils

__all__ = (
    "menu_has_no_space_error",
    "menu_item_created",
    "menu_item_deleted",
    "menu_item_edited",
    "menu_item",
    "menu_item_has_no_menu_error",
    "menu_item_moved",
    "menu",
    "menu_deleted",
    "menu_sent",
)

if TYPE_CHECKING:
    import quarrel
    from quarrel import Missing

    from .. import models


def menu_has_no_space_error(
    interaction: quarrel.Interaction,
    menu: models.Menu,
    item: models.MenuItem,
    row: Missing[int],
    column: Missing[int],
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.menu_has_no_space(menu, item, row, column),
        color=consts.ERROR_EMBED_COLOR,
    )


def menu_item_created(
    interaction: quarrel.Interaction, item: models.MenuItem
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.menu_item_created(item),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def menu_item_deleted(
    interaction: quarrel.Interaction, item: models.MenuItem
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.menu_item_deleted(item),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def menu_item_edited(
    interaction: quarrel.Interaction, item: models.MenuItem
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.menu_item_edited(item),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def menu_item(interaction: quarrel.Interaction, item: models.MenuItem) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        fields=[
            utils.embed_field("ID", item.id),
            utils.embed_field("Menu ID", item.menu_id),
            utils.embed_field("Type", strings.enum_name(item.type)),
            utils.embed_field("Style", strings.enum_name(item.style)),
            utils.embed_field("Label", item.label),
            utils.embed_field("Disabled", item.disabled),
            utils.embed_field("URL", item.url),
            utils.embed_field("Emoji", item.emoji),
            utils.embed_field(
                "Action",
                strings.enum_name(item.action) if item.action else None,
            ),
            utils.embed_field(
                "Action Options",
                ", ".join([str(i) for i in item.action_options]),
            ),
        ],
        color=consts.SUCCESS_EMBED_COLOR,
    )


def menu_item_has_no_menu_error(
    interaction: quarrel.Interaction, item: models.MenuItem
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.menu_item_has_no_menu(item),
        color=consts.ERROR_EMBED_COLOR,
    )


def menu_item_moved(
    interaction: quarrel.Interaction,
    item: models.MenuItem,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.menu_item_moved(item),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def menu(
    interaction: quarrel.Interaction,
    menu: models.Menu,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        fields=[
            utils.embed_field("ID", menu.id),
            utils.embed_field("Name", menu.name),
            utils.embed_field("Description", menu.description, inline=False),
        ],
        color=consts.SUCCESS_EMBED_COLOR,
    )


def menu_deleted(
    interaction: quarrel.Interaction,
    menu: models.Menu,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.menu_deleted(menu),
        color=consts.SUCCESS_EMBED_COLOR,
    )


def menu_sent(
    interaction: quarrel.Interaction,
    menu: models.Menu,
    channel: quarrel.TextChannel | quarrel.Thread,
) -> quarrel.Embed:
    return utils.build_single_embed_from_user(
        author=interaction.user,
        description=strings.menu_sent(menu, channel),
        color=consts.SUCCESS_EMBED_COLOR,
    )
