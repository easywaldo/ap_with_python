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