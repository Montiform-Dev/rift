from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("Condition",)

if TYPE_CHECKING:
    from typing import Any, ClassVar

    from ..commands.common import CommonSlashCommand
    from ..types.models.condition import Condition as ConditionData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class Condition:
    TABLE: ClassVar[str] = "conditions"
    id: int
    name: str
    owner_id: int
    value: str
    public: bool
    use_condition: str

    async def save(self) -> None:
        ...

    async def delete(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: ConditionData) -> Condition:
        ...

    def to_dict(self) -> ConditionData:
        ...

    def update(self, data: Condition) -> Condition:
        ...

    @classmethod
    async def convert(cls, command: CommonSlashCommand[Any], value: str) -> Condition:
        ...
