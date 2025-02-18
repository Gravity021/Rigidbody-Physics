from unittest import TestCase

from app_main.maths.Vector2 import Vector2
from app_main.physics.object import Object

class ObjectTests(TestCase):
    def assertDoesntRaise(self, expected_exception: type[BaseException] | tuple[type[BaseException], ...], callable: (...), *_, **__) -> object:
        raises_exception = False
        try:
            callable(*_, **__)
        except expected_exception as ex:
            print(ex)
            raises_exception = True
        
        self.assertFalse(raises_exception)

    def test_valid_constructor(self):
        self.assertDoesntRaise(Exception, Object, Object.ObjectType.NONE, Vector2(1, 1), Vector2(1, 1), 1)

        self.assertDoesntRaise(Exception, Object, Object.ObjectType.CIRCLE, Vector2(10, 10), Vector2(2, -1), 3, 2, (100, 175, 50))

    def test_object_type_validation(self):
        # Test Invalid conditions
        self.assertRaises(ValueError, Object, 2, Vector2(1, 1), Vector2(1, 1), 1)
        self.assertRaises(ValueError, Object, 3, Vector2(1, 1), Vector2(1, 1), 1)

        # Test Valid conditions
        self.assertDoesntRaise(Exception, Object, Object.ObjectType.CIRCLE, Vector2(1, 1), Vector2(1, -1), 1)
        self.assertDoesntRaise(Exception, Object, Object.ObjectType.RECTANGLE, Vector2(1, 1), Vector2(1, 1), 1)
    
    def test_dimensions_validation(self):
        # Test Valid conditions
        self.assertDoesntRaise(Exception, Object, Object.ObjectType.CIRCLE, Vector2(1, 1), Vector2(1, -1), 1)
        self.assertDoesntRaise(Exception, Object, Object.ObjectType.RECTANGLE, Vector2(1, 1), Vector2(1, 1), 1)

        # Test Invalid conditions
        self.assertRaises(ValueError, Object, Object.ObjectType.RECTANGLE, Vector2(1, 1), Vector2(0, 1), 1)
        self.assertRaises(ValueError, Object, Object.ObjectType.RECTANGLE, Vector2(1, 1), Vector2(1, -1), 1)

        self.assertRaises(ValueError, Object, Object.ObjectType.CIRCLE, Vector2(1, 1), Vector2(0, 1), 1)
        self.assertRaises(ValueError, Object, Object.ObjectType.CIRCLE, Vector2(1, 1), Vector2(-1, 1), 1)
        self.assertRaises(ValueError, Object, Object.ObjectType.CIRCLE, Vector2(1, 1), Vector2(1, 1), 1)
    
    def test_mass_validation(self):
        # Test Valid conditions
        self.assertDoesntRaise(Exception, Object, Object.ObjectType.NONE, Vector2(1, 1), Vector2(1, 1), 1)

        # Test Invalid conditions
        self.assertRaises(ValueError, Object, Object.ObjectType.NONE, Vector2(1, 1), Vector2(1, 1), 0)
        self.assertRaises(ValueError, Object, Object.ObjectType.NONE, Vector2(1, 1), Vector2(1, 1), -10)
    
    def test_colour_validation(self):
        # Test Valid conditions
        obj = Object(Object.ObjectType.NONE, Vector2(1, 1), Vector2(1, 1), 1, colour=[100, 175, 50])
        self.assertEqual(obj.colour, [100, 175, 50])
        obj = Object(Object.ObjectType.NONE, Vector2(1, 1), Vector2(1, 1), 1, colour=[255, 0, 0, 255])
        self.assertEqual(obj.colour, [255, 0, 0, 255])

        # Test Invalid conditions
        obj = Object(Object.ObjectType.NONE, Vector2(1, 1), Vector2(1, 1), 1, colour=[-1, 500, 7, 255])
        self.assertEqual(obj.colour, [0, 255, 7, 255])