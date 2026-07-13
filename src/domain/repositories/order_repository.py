from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.order import Order


class OrderRepository(ABC):

    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def find_all(self) -> List[Order]:
        pass

    @abstractmethod
    def find_by_id(self, order_id: int) -> Optional[Order]:
        pass

    @abstractmethod
    def delete(self, order_id: int) -> bool:
        pass
