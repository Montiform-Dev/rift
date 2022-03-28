from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("InactiveAlert",)

if TYPE_CHECKING:
    import datetime
    from typing import ClassVar

    from ..types.models.inactive_alert import InactiveAlert as InactiveAlertData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class InactiveAlert:
    TABLE: ClassVar[str] = "inactive_alerts"
    PRIMARY_KEY: ClassVar[str] = "nation_id"
    nation_id: int
    last_alert: datetime.datetime

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: InactiveAlertData) -> InactiveAlert:
        ...

    def to_dict(self) -> InactiveAlertData:
        ...

    def update(self, data: InactiveAlert) -> InactiveAlert:
        ...

    @property
    def key(self) -> int:
        return self.nation_id
