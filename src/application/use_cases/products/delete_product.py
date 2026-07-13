from src.domain.repositories.product_repository import ProductRepository


class DeleteProductUseCase:
    def __init__(self, repo: ProductRepository):
        self._repo = repo

    def execute(self, product_id: int) -> bool:
        return self._repo.delete(product_id)
