from typing import List
from src.domain.entities.order import Order
from src.domain.repositories.order_repository import OrderRepository


class ListOrdersUseCase:

    def __init__(self, repo: OrderRepository):
        self._repo = repo

    def execute(self) -> List[Order]:
        return self._repo.find_all()
