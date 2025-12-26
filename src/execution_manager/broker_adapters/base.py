"""Base Broker Adapter interface"""
from abc import ABC, abstractmethod


class BrokerAdapter(ABC):
    @abstractmethod
    def place_order(self, order, idempotency_key=None):
        """Place an order with the broker.

        Must return a dict describing the fill or order acknowledgement.
        """
        raise NotImplementedError()

    @abstractmethod
    def cancel_order(self, broker_order_id):
        """Cancel an outstanding order."""
        raise NotImplementedError()
