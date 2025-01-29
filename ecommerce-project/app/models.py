from typing import TypedDict

class Item(TypedDict):
    """
    Represents an item in the e-commerce system.

    Attributes:
        id: The unique identifier of the item.
        name: The name of the item.
        price: The price of the item.
    """
    id: int
    name: str
    price: float

class CreateItem(TypedDict):
    """
    Represents data used to create an item in the e-commerce system.
     Attributes:
        name: The name of the item.
        price: The price of the item.
    """
    name: str
    price: float

class UpdateItem(TypedDict):
    """
    Represents data used to update an item in the e-commerce system.
     Attributes:
        name: The name of the item.
        price: The price of the item.
    """
    name: str
    price: float
