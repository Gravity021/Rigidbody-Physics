from unittest import TestCase

from app_main.maths.Vector2 import Vector2
from app_main.physics.object import Object
from app_main.util.debug import Debug

class ObjectTests(TestCase):
    def assertErrorLogged(self, msg: str = None):
        error = False
        for message in Debug._messages:
            error |= message["level"] == "ERROR"
            if error: break
        
        self.assertTrue(error, msg)
        
        Debug._messages = []  # Reset messages for next test case
    
    def assertNoErrorLogged(self, msg: str = None):
        error = False
        for message in Debug._messages:
            error |= message["level"] == "ERROR"
            if error: break
        
        self.assertFalse(error, msg)
        
        Debug._messages = []  # Reset messages for next test case

    def test_valid_constructor(self):
        Object(Object.ObjectType.NONE, Vector2(1, 1), Vector2(1, 1), 1)
        self.assertNoErrorLogged()

        Object(Object.ObjectType.CIRCLE, Vector2(10, 10), Vector2(2, -1), 3, 2, (100, 175, 50))
        self.assertNoErrorLogged()

    def test_object_type_validation(self):
        # Test Invalid conditions
        Object(2, Vector2(1, 1), Vector2(1, 1), 1)
        self.assertErrorLogged()
        Object(3, Vector2(1, 1), Vector2(1, 1), 1)
        self.assertErrorLogged()

        # Test Valid conditions
        Object(Object.ObjectType.CIRCLE, Vector2(1, 1), Vector2(1, -1), 1)
        self.assertNoErrorLogged()
        Object(Object.ObjectType.RECTANGLE, Vector2(1, 1), Vector2(1, 1), 1)
        self.assertNoErrorLogged()
    
    def test_dimensions_validation(self):
        # Test Valid conditions
        Object(Object.ObjectType.CIRCLE, Vector2(1, 1), Vector2(1, -1), 1)
        self.assertNoErrorLogged()
        Object(Object.ObjectType.RECTANGLE, Vector2(1, 1), Vector2(1, 1), 1)
        self.assertNoErrorLogged()

        # Test Invalid conditions
        Object(Object.ObjectType.RECTANGLE, Vector2(1, 1), Vector2(0, 1), 1)
        self.assertErrorLogged()
        Object(Object.ObjectType.RECTANGLE, Vector2(1, 1), Vector2(1, -1), 1)
        self.assertErrorLogged()

        Object(Object.ObjectType.CIRCLE, Vector2(1, 1), Vector2(0, 1), 1)
        self.assertErrorLogged()
        Object(Object.ObjectType.CIRCLE, Vector2(1, 1), Vector2(-1, 1), 1)
        self.assertErrorLogged()
        Object(Object.ObjectType.CIRCLE, Vector2(1, 1), Vector2(1, 1), 1)
        self.assertErrorLogged()
    
    def test_mass_validation(self):
        # Test Valid conditions
        Object(Object.ObjectType.NONE, Vector2(1, 1), Vector2(1, 1), 1)
        self.assertNoErrorLogged()

        # Test Invalid conditions
        Object(Object.ObjectType.NONE, Vector2(1, 1), Vector2(1, 1), 0)
        self.assertErrorLogged()
        Object(Object.ObjectType.NONE, Vector2(1, 1), Vector2(1, 1), -10)
        self.assertErrorLogged()
    
    def test_colour_validation(self):
        # Test Valid conditions
        obj = Object(Object.ObjectType.NONE, Vector2(1, 1), Vector2(1, 1), 1, colour=[100, 175, 50])
        self.assertEqual(obj.colour, [100, 175, 50])
        obj = Object(Object.ObjectType.NONE, Vector2(1, 1), Vector2(1, 1), 1, colour=[255, 0, 0, 255])
        self.assertEqual(obj.colour, [255, 0, 0, 255])

        # Test Invalid conditions
        obj = Object(Object.ObjectType.NONE, Vector2(1, 1), Vector2(1, 1), 1, colour=[-1, 500, 7, 255])
        self.assertEqual(obj.colour, [0, 255, 7, 255])