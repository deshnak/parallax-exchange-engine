"""
Core domain types: orders, trades, sides.
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, field

class Side(Enum):
    BUY = 1
    SELL = 2

    @property
    def opposite(self) -> Side:
        return Side.SELL if self is Side.BUY else Side.BUY

class OrderType(Enum):
    LIMIT = 1
    MARKET = 2

@dataclass
class Order:
    order_id: int
    agent_id: int
    side: Side
    order_type: OrderType
    quantity: int
    price: int | None = field(default=None)
    seq: int = field(default=-1)
    remaining: int = field(default=-1)

    def __post_init__(self) -> None:
        if self.remaining == -1:
            self.remaining = self.quantity

@dataclass(frozen=True)
class Trade:
    seq: int
    price: int
    quantity: int
    aggressor_side: Side
    maker_order_id: int
    taker_order_id: int
    maker_agent_id: int
    taker_agent_id: int

@dataclass(frozen=True)
class OrderAccepted:
    seq: int
    order_id: int

@dataclass(frozen=True)
class OrderRejected:
    seq: int
    order_id: int
    reason: str

@dataclass(frozen=True)
class OrderRested:
    seq: int
    order_id: int
    remaining: int

@dataclass(frozen=True)
class OrderCancelled:
    seq: int
    order_id: int
    cancelled: int
    reason: str

@dataclass(frozen=True)
class OrderModified:
    seq: int
    order_id: int
    new_price: int | None
    new_quantity: int
    kept_priority: bool

Event = Trade | OrderAccepted | OrderRejected | OrderRested | OrderCancelled | OrderModified
