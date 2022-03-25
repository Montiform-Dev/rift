from __future__ import annotations

from typing import TYPE_CHECKING

import attrs

from .. import utils

__all__ = ("User",)

if TYPE_CHECKING:
    import uuid
    from typing import ClassVar

    from ..types.models.user import User as UserData


@utils.model
@attrs.define(weakref_slot=False, auto_attribs=True, kw_only=True, eq=False)
class User:
    TABLE: ClassVar[str] = "users"
    user_id: int
    nation_id: int
    uuid: uuid.UUID

    async def save(self) -> None:
        ...

    @classmethod
    def from_dict(cls, data: UserData) -> User:
        ...

    @property
    def key(self) -> int:
        return self.user_id
