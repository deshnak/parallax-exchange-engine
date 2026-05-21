"""
order book implementation using sortedcontainers for efficient price level management.
"""
from lobsim.engine.types import Order, Side
from sortedcontainers import SortedDict
from collections import deque

class OrderBook:

    # Initialize empty order book with sorted dictionaries for bids and asks.
    def __init__(self) -> None:
        self.bids: SortedDict[int, deque[Order]] = SortedDict()
        self.asks: SortedDict[int, deque[Order]] = SortedDict()
        self.orders: dict[int, Order] = {}

    # Add an order to the book.
    def add(self, order: Order) -> None:
        book_side = self.bids if order.side is Side.BUY else self.asks
        if order.price not in book_side:
            book_side[order.price] = deque()
        book_side[order.price].append(order)
        self.orders[order.order_id] = order

    # Remove an order from the book by order_id.
    def remove(self, order_id: int) -> Order:
        # Relies on orders_by_id and the deque holding the same Order instance
        order = self.orders.pop(order_id)
        book_side = self.bids if order.side is Side.BUY else self.asks
        orders_at_price = book_side[order.price]
        orders_at_price.remove(order)
        if not orders_at_price:
            del book_side[order.price]
        return order
    
    # Get the best bid and ask prices and quantities.
    def bbid(self) -> Order | None:
        if not self.bids:
            return None
        best_price = self.bids.peekitem(-1)[0]
        return self.bids[best_price][0]
    
    # Get the best ask price and quantity.
    def bask(self) -> Order | None:
        if not self.asks:
            return None
        best_price = self.asks.peekitem(0)[0]
        return self.asks[best_price][0]
    
    # Get an order by order_id.
    def get(self, order_id: int) -> Order | None:
        return self.orders.get(order_id)