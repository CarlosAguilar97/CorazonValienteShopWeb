import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Phone:
    number: str

    def __post_init__(self):
        clean = re.sub(r"\D", "", self.number)
        if len(clean) < 9:
            raise ValueError(f"Número de teléfono inválido: {self.number}")
        object.__setattr__(self, "number", clean)

    def whatsapp_link(self, message: str = "") -> str:
        encoded = message.replace(" ", "%20").replace("\n", "%0A")
        return f"https://wa.me/{self.number}?text={encoded}"

    def __str__(self) -> str:
        return self.number
