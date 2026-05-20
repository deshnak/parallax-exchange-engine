"""
Tests the types file in engine folder
"""
from __future__ import annotations
import pytest
from dataclasses import FrozenInstanceError
from lobsim.engine.types import Order, OrderType, Side, Trade


def test_side_opposite() -> None:
    assert Side.BUY.opposite is Side.SELL
    assert Side.SELL.opposite is Side.BUY

def test_order_default() -> None:
    order = Order(
        order_id=1,
        agent_id=42,
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        quantity=100,
        price=10_000,
    )
    assert order.remaining == 100
    assert order.seq == -1

def test_order_explicit() -> None:
    order = Order(
        order_id=2,
        agent_id=42,
        side=Side.BUY,
        order_type=OrderType.LIMIT,
        quantity=100,
        price=10_000,
        remaining=30,
    )
    assert order.remaining == 30
def test_immutable_trade() -> None:
    trade = Trade(
        seq=1,
        price=10_000,
        quantity=10,
        aggressor_side=Side.BUY,
        maker_order_id=1,
        taker_order_id=2,
        maker_agent_id=7,
        taker_agent_id=8,
    )
    with pytest.raises(FrozenInstanceError):
        trade.price = 9999

