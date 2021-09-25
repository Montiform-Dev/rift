from __future__ import annotations

from typing import List, Literal, TypedDict

__all__ = ("SubscriptionData", "EventCategoryLiteral", "EventTypeLiteral")

EventCategoryLiteral = Literal[
    "ALLIANCE", "FORUM", "NATION", "TREATY"
]  # ATTACK, COLOR, PRICE, TRADE, TREASURE, WAR
EventTypeLiteral = Literal["CREATE", "DELETE", "UPDATE"]  # ACCEPT, VICTORY


class SubscriptionData(TypedDict):
    id: int
    token: str
    guild_id: int
    channel_id: int
    category: EventCategoryLiteral
    type: EventTypeLiteral
    sub_types: List[str]
    arguments: List[int]