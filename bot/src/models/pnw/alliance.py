from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

import attrs

from ... import enums, models, utils

__all__ = ("Alliance",)

if TYPE_CHECKING:
    import decimal
    from typing import Any, ClassVar

    from pnwkit.data import Alliance as PnWKitAlliance

    from ...commands.common import CommonSlashCommand
    from ...types.models.pnw.alliance import Alliance as AllianceData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Alliance:
    TABLE: ClassVar[str] = "alliances"
    INCREMENT: ClassVar[tuple[str, ...]] = ()
    ENUMS: ClassVar[tuple[str, ...]] = ("color",)
    id: int
    name: str
    acronym: str
    score: decimal.Decimal
    color: enums.Color = attrs.field(converter=enums.Color)
    date: datetime.datetime
    accepts_members: bool
    flag: str
    forum_link: str
    discord: str
    estimated_resources: models.Resources

    async def save(self, insert: bool = False) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: AllianceData) -> Alliance:
        ...

    def to_dict(self) -> AllianceData:
        ...

    def update(self, data: Alliance) -> Alliance:
        ...

    @classmethod
    def from_data(cls, data: PnWKitAlliance) -> Alliance:
        if TYPE_CHECKING:
            assert isinstance(data.score, decimal.Decimal)
        return cls(
            id=int(data.id),
            name=data.name,
            acronym=data.acronym,
            score=data.score,
            color=getattr(enums.Color, data.color.upper()),
            date=datetime.datetime.fromisoformat(data.date),
            accepts_members=data.acceptmem,
            flag=data.flag,
            forum_link=data.forumlink,
            discord=data.irclink,
            estimated_resources=models.Resources(),
        )

    @classmethod
    async def convert(
        cls, command: CommonSlashCommand[Any], value: str, default_to_self: bool = False
    ) -> Alliance:
        ...
