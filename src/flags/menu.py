from typing import Optional, Tuple, Union

from discord import PartialEmoji
from discord.emoji import Emoji
from discord.ext.commands.flags import flag

from .base import BaseFlagConverter


class ButtonFlags(BaseFlagConverter):
    action: Optional[str]
    url: Optional[str]
    disabled: Optional[bool] = flag(default=False)
    style: Optional[str] = flag(aliases=["color"])
    label: str = flag(aliases=["name"])
    emoji: Optional[Union[PartialEmoji, Emoji]]
    options: Tuple[str, ...]
    row: Optional[int]


class SelectFlags(BaseFlagConverter):
    placeholder: Optional[str]
    min_values: Optional[int]
    max_values: Optional[int]


class SelectOptionFlags(BaseFlagConverter):
    default: bool
    description: str
    emoji: Union[PartialEmoji, Emoji]
    label: str = flag(name="label", aliases=["name"])
    action: str
    options: Tuple[str, ...]
    row: Optional[int]