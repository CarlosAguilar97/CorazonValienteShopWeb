from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class OrderItem:
    id: Optional[int]
    product_id: int
    product_name: str
    color: Optional[str]
    size: Optional[str]
    price: float
    quantity: int


@dataclass
class Order:
    id: Optional[int]
    name: str
    address: str
    notes: Optional[str]
    total: float
    voucher_url: Optional[str]
    status: str = "Pendiente"
    created_at: Optional[datetime] = None
    items: List[OrderItem] = field(default_factory=list)
