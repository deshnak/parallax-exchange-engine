from __future__ import annotations

import pytest

from lobsim.engine.book import OrderBook
from lobsim.engine.types import Order, OrderType, Side

def make_order(
    order_id: int,
    side: Side,
    price: int,
    quantity: int = 10,
    agent_id: int = 1,
) -> Order:
    return Order(
        order_id=order_id,
        agent_id=agent_id,
        side=side,
        order_type=OrderType.LIMIT,
        quantity=quantity,
        price=price,
    )

def test_empty_book() -> None:
    book = OrderBook()
    assert book.bbid() is None
    assert book.bask() is None

def test_add_single_bid() -> None:
    book = OrderBook()
    order = make_order(order_id=1, side=Side.BUY, price=100)
    book.add(order)
    assert book.bbid() == order
    assert book.bask() is None

def test_add_single_ask() -> None:
    book = OrderBook()
    order = make_order(order_id=1, side=Side.SELL, price=101)
    book.add(order)
    assert book.bbid() is None
    assert book.bask() is order

def test_best_bid_ask() -> None:
    book = OrderBook()
    bid1 = make_order(order_id=1, side=Side.BUY, price=100)
    bid2 = make_order(order_id=2, side=Side.BUY, price=101)
    ask1 = make_order(order_id=3, side=Side.SELL, price=102)
    ask2 = make_order(order_id=4, side=Side.SELL, price=101)
    book.add(bid1)
    book.add(bid2)
    book.add(ask1)
    book.add(ask2)
    assert book.bbid() is bid2
    assert book.bask() is ask2

def test_best_bid()-> None:
    book = OrderBook()
    bid1 = make_order(order_id=1, side=Side.BUY, price=100)
    bid2 = make_order(order_id=2, side=Side.BUY, price=101)
    book.add(bid1)
    book.add(bid2)
    assert book.bbid() is bid2

def test_fifo_with_same_price() -> None:
    book = OrderBook()
    bid1 = make_order(order_id=1, side=Side.BUY, price=100)
    bid2 = make_order(order_id=2, side=Side.BUY, price=100)
    book.add(bid1)
    book.add(bid2)
    assert book.bbid() is bid1

def test_remove_order() -> None:
    book = OrderBook()
    bid1 = make_order(order_id=1, side=Side.BUY, price=100)
    bid2 = make_order(order_id=2, side=Side.BUY, price=101)
    book.add(bid1)
    book.add(bid2)
    removed = book.remove(order_id=2)
    assert removed is bid2
    assert book.bbid() is bid1

def test_keyerror_on_remove_nonexistent_order() -> None:
    book = OrderBook()
    with pytest.raises(KeyError):
        book.remove(order_id=999)

def test_remove_empties_price_level() -> None:
    book = OrderBook()
    bid1 = make_order(order_id=1, side=Side.BUY, price=100)
    book.add(bid1)
    book.remove(order_id=1)
    assert book.bbid() is None

def test_remove_one_of_many_orders_at_price() -> None:
    book = OrderBook()
    bid1 = make_order(order_id=1, side=Side.BUY, price=100)
    bid2 = make_order(order_id=2, side=Side.BUY, price=100)
    book.add(bid1)
    book.add(bid2)
    book.remove(order_id=1)
    assert book.bbid() is bid2
