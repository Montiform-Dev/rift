from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("TargetRater",)

if TYPE_CHECKING:
    from typing import Any, ClassVar

    from ..commands.common import CommonSlashCommand
    from ..types.models.target_rater import TargetRater as TargetRaterData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class TargetRater:
    TABLE: ClassVar[str] = "target_raters"
    id: int
    cities: str
    infrastructure: str
    activity: str
    soldiers: str
    tanks: str
    aircraft: str
    ships: str
    missiles: str
    nukes: str
    money: str
    coal: str
    oil: str
    uranium: str
    iron: str
    bauxite: str
    lead: str
    gasoline: str
    munitions: str
    steel: str
    aluminum: str
    food: str

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: TargetRaterData) -> TargetRater:
        ...

    def to_dict(self) -> TargetRaterData:
        ...

    def update(self, data: TargetRater) -> TargetRater:
        ...

    @classmethod
    async def convert(cls, command: CommonSlashCommand[Any], value: str) -> TargetRater:
        ...
