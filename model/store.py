from dataclasses import dataclass


@dataclass
class Store:
    store_id: int
    store_name: str
    phone: str
    email: str
    street: str
    city: str
    state: str
    zip_code: int

    def __str__(self):
        return self.store_name