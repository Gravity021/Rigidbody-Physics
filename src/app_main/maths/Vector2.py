# (c) 2023-24 Isaac Godman

import math

class Vector2:
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x = x
        self.y = y
    
    def of(list: list[float, float]):
        return Vector2(list[0], list[1])
    
    def normalise(self):
        if self.magnitude != 0:
            self.x = self.x / self.magnitude
            self.y = self.y / self.magnitude
    
    def dist(self, other):
        if type(other) == Vector2:
            return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def get_normalised(self):
        if self.magnitude != 0:
            return Vector2(self.x / self.magnitude, self.y / self.magnitude)
        return Vector2()

    def dot(self, other):
        if type(other) == Vector2:
            return self.x * other.x + self.y * other.y
    
    def __str__(self) -> str:
        return f"Vector2(x={self.x}, y={self.y})"
    
    def __add__(self, other):
        if type(other) in [Vector2]:
            return Vector2(self.x + other.x, self.y + other.y)
        elif type(other) in [list[int], list[float]]:
            return Vector2(self.x + other[0], self.y + other[1])
        else:
            raise TypeError(f"Unsupported operand type for 'Vector2' + '{type(other)}'")
    
    def __sub__(self, other):
        if type(other) in [Vector2]:
            return Vector2(self.x - other.x, self.y - other.y)
        elif type(other) in [list[int], list[float]]:
            return Vector2(self.x - other[0], self.y - other[1])
        else:
            raise TypeError(f"Unsupported operand type for 'Vector2' - '{type(other)}'")
    
    def __mul__(self, other):
        if type(other) in [int, float]:
            return Vector2(self.x * other, self.y * other)
        else:
            raise TypeError(f"Unsupported operand type for 'Vector2' * '{type(other)}'")

    def __truediv__(self, other):
        if type(other) in [int, float]:
            return Vector2(self.x / other, self.y / other)
        else:
            raise TypeError(f"Unsupported operand type for 'Vector2' / '{type(other)}'")

    def __floordiv__(self, other):
        if type(other) in [int, float]:
            return Vector2(self.x // other, self.y // other)
        else:
            raise TypeError(f"Unsupported operand type for 'Vector2' // '{type(other)}'")
    
    def __pow__(self, other):
        if type(other) in [int, float]:
            return Vector2(self.x ** other, self.y ** other)
        else:
            raise TypeError(f"Unsupported operand type for 'Vector2' ** '{type(other)}'")
    
    def __iter__(self):
        return iter([self.x, self.y])
    
    @property
    def list(self):
        return [self.x, self.y]

    @property
    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    # https://www.programiz.com/python-programming/operator-overloading
