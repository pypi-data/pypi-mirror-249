import dataclasses

@dataclasses.dataclass
class Class:
    a: int
    b: str = 'hi'


class Sub(Class):
    c: float = 4

Class(a=4.3, b=4)

