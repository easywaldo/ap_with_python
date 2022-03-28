from collections import namedtuple
from dataclasses import dataclass
from typing import List, NamedTuple

import pytest

@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str
    

class Money(NamedTuple):
    currency: str
    value: int

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


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

class Batch:
    def __init__(self, ref: Reference, sku: Sku, qty: Quantity):
        self.sku = sku
        self.reference = ref
        self._purchased_quantity = qty
        self._allocations = set()
        
    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)
    
    def __gt__(self, other):
        if self.qty is None:
            return False
        if other.qty is None:
            return True
        return self.qty > other.qty
    
    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)
            
    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty


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


def test_value_object_match():
    Line = namedtuple('Line', ['sku', 'qty'])
    assert Money('gbp', 10) == Money('gbp', 10)
    assert Name('Harry', 'Percival') != Name('Bob', 'Gregory')
    assert Line('RED-CHAIR', 5) == Line('RED-CHAIR', 5)

test_value_object_match()


def test_barry_is_harry():
    harry = Person(Name("Harry", "Percival"))
    barry = harry

    barry.name = Name("Barry", "Percival")

    assert harry is barry and barry is harry
    print(barry)
    print(harry)
    

test_barry_is_harry()

def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(
            b for b in sorted(batches) if b.can_allocate(line)
        )
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f'Out of stock {line.qty}')

class OutOfStock(Exception):
    pass


def test_raise_out_of_stock_exception_if_cannot_allocate():
    batch = Batch('batch1', 'SMALL-FORK', 10)
    allocate(OrderLine('order1', 'SMALL-FORK', 10), [batch])

    with pytest.raises(OutOfStock, match='Out of stock 1'):
        allocate(OrderLine('order2', 'SMALL-FORK', 1), [batch])
    
test_raise_out_of_stock_exception_if_cannot_allocate()
