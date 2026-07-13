from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "PEN"  # Sol peruano por defecto

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("El monto no puede ser negativo")

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("No se pueden sumar montos con diferente moneda")
        return Money(round(self.amount + other.amount, 2), self.currency)

    def __str__(self) -> str:
        return f"S/ {self.amount:.2f}"
