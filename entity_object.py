from dataclasses import dataclass
from typing import NamedTuple

@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str

class Person:

    def __init__(self, name: Name):
        self.name = name
        
def test_barry_is_harry():
    harry = Person(Name("Harry", "Percival"))
    barry = harry

    barry.name = Name("Barry", "Percival")

    assert harry is barry and barry is harry
    
test_barry_is_harry()


from dataclasses import dataclass
from typing import NewType

Quantity = NewType("Quantity", int)
Sku = NewType("Sku", str)
Reference = NewType("Reference", str)
...

class Batch:
    def __init__(self, ref: Reference, sku: Sku, qty: Quantity):
        self.sku = sku
        self.reference = ref
        self._purchased_quantity = qty
        
    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)


def test_batch_is_same():
    batch_first: Batch = Batch(Reference("odry"), Sku("color-yellow"), Quantity(100))
    batch_two: Batch = Batch(Reference("odry"), Sku("color-green"), Quantity(100))
    print(batch_first)
    print(batch_two)
    assert batch_first == batch_two
    
    batch_third = batch_first
    batch_third.sku = Sku("color-pink")
    print(batch_third)
    print(batch_first)
    assert batch_first == batch_third
    
test_batch_is_same()