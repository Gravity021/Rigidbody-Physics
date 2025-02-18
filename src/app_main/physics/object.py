from enum import Enum

from ..core.window import Window

from ..maths.Vector2 import Vector2

class Object:
    """A Plain-old-data object representing a physical object."""

    # TODO: Add a .give_impulse helper method

    class ObjectType(Enum):
        """A type representing the type of an object."""

        NONE = 0,
        CIRCLE = 1,
        RECTANGLE = 2,

    def __init__(self, object_type: ObjectType,
                 position: Vector2,
                 dimensions: Vector2,
                 mass: float,
                 rotation: float = 0,
                 colour: list[int] = [255, 255, 255, 255]) -> None:
        
        # Initialse private variables
        self._object_type = Object.ObjectType.NONE
        
        self._dimensions = None

        self._mass = None
        self._colour = None

        # Pass through parameters through validation processes      
        self.object_type = object_type

        self.position = position
        self.velocity = Vector2()
        self.force = Vector2()

        self.rotation = rotation

        self.mass = mass

        self.colour = colour
        self.dimensions = dimensions
    
    @property
    def object_type(self) -> ObjectType:
        return self._object_type
    
    @object_type.setter
    def object_type(self, value: ObjectType) -> None:
        if value in Object.ObjectType:
            self._object_type = value
        else:
            raise ValueError(f"Invalid object type of {value}.")
    
    @property
    def mass(self) -> float:
        return self._mass
    
    @mass.setter
    def mass(self, value: float) -> None:
        if value > 0:
            self._mass = value
        else:
            raise ValueError(f"Mass must be a positive value. Value provided was {value}.")
    
    @property
    def colour(self) -> list[int]:
        return self._colour
    
    @colour.setter
    def colour(self, value: list[int]) -> None:
        self._colour = Window.validate_colour(value)
    
    @property
    def dimensions(self) -> Vector2:
        return self._dimensions

    @dimensions.setter
    def dimensions(self, value: Vector2) -> None:
        x_invalid = False
        y_invalid = False

        if value.x <= 0: x_invalid = True
        
        if self._object_type == Object.ObjectType.CIRCLE:
            if value.y != -1: y_invalid = True
            
            if x_invalid and y_invalid:
                raise ValueError(f"Both x and y-components of dimensions for a circle are invalid. x-component must be positive and y-component must be '-1'. Values provided were {value.x} and {value.y}.")
            elif x_invalid:
                raise ValueError(f"x-component of dimensions for a circle must be positive. Value provided was {value.x}.")
            elif y_invalid:
                raise ValueError(f"y-component of dimensions for a circle must be '-1'. Value provided was {value.y}.")

        elif self._object_type == Object.ObjectType.RECTANGLE:
            if value.y <= 0: y_invalid = True
            
            if x_invalid and y_invalid:
                raise ValueError(f"Both x and y-components of dimensions for a rectangle are invalid. Both components must be positive. Values provided were {value.x} and {value.y}.")
            elif x_invalid:
                raise ValueError(f"x-component of dimensions for a rectangle must be positive. Value provided was {value.x}.")
            elif y_invalid:
                raise ValueError(f"y-component of dimensions for a rectangle must be positive. Value provided was {value.y}.")
        
        self._dimensions = value

