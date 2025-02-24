from copy import copy
from unittest import TestCase

from app_main.maths.Vector2 import Vector2
from app_main.physics.object import Object
from app_main.physics import PhysicsManager

from app_main.util.time import Time

class PhysicsManagerTests(TestCase):
    def test_step_1(self):
        obj = Object(Object.ObjectType.CIRCLE, Vector2(1, 1), Vector2(1, -1), 1)
        obj1 = copy(obj)
        self.assertEqual(obj1.position, obj.position)
        self.assertEqual(obj1.velocity, obj.velocity)
        self.assertEqual(obj1.mass, obj.mass)

        PhysicsManager.step([obj1], 0.01)

        self.assertEqual(obj1.position.x, 1)
        self.assertEqual(obj1.position.y, 0.9995095)

        self.assertEqual(obj1.velocity.x, 0)
        self.assertEqual(obj1.velocity.y, -0.0981)
    
    def test_step_2(self):
        obj = Object(Object.ObjectType.CIRCLE, Vector2(1, 1), Vector2(1, -1), 1)
        obj1 = copy(obj)
        self.assertEqual(obj1.position, obj.position)
        self.assertEqual(obj1.velocity, obj.velocity)
        self.assertEqual(obj1.mass, obj.mass)

        for i in range(10):
            PhysicsManager.step([obj1], 0.01)

        self.assertEqual(obj1.position.x, 1)
        self.assertAlmostEqual(obj1.position.y, 0.95095)

        self.assertEqual(obj1.velocity.x, 0)
        self.assertAlmostEqual(obj1.velocity.y, -0.981)
    
    def test_step_3(self):
        delta = 10

        obj = Object(Object.ObjectType.CIRCLE, Vector2(1, 1), Vector2(1, -1), 1)
        obj1 = copy(obj)
        self.assertEqual(obj1.position, obj.position)
        self.assertEqual(obj1.velocity, obj.velocity)
        self.assertEqual(obj1.mass, obj.mass)

        for i in range(int(delta / 0.01)):
            PhysicsManager.step([obj1], 0.01)

        self.assertEqual(obj1.position.x, 1)
        self.assertAlmostEqual(obj1.position.y, -489.5)

        self.assertEqual(obj1.velocity.x, 0)
        self.assertAlmostEqual(obj1.velocity.y, -98.1)
    
    def test_step_4(self):
        delta = 100

        obj = Object(Object.ObjectType.CIRCLE, Vector2(1, 1), Vector2(1, -1), 1)
        obj1 = copy(obj)
        self.assertEqual(obj1.position, obj.position)
        self.assertEqual(obj1.velocity, obj.velocity)
        self.assertEqual(obj1.mass, obj.mass)

        for i in range(int(delta / 0.01)):
            PhysicsManager.step([obj1], 0.01)

        self.assertEqual(obj1.position.x, 1)
        self.assertAlmostEqual(obj1.position.y, 1 - 0.5 * 9.81 * delta ** 2)

        self.assertEqual(obj1.velocity.x, 0)
        self.assertAlmostEqual(obj1.velocity.y, -9.81 * delta)

    def test_step_5(self):
        delta = 325

        obj = Object(Object.ObjectType.CIRCLE, Vector2(1, 1), Vector2(1, -1), 1)
        obj1 = copy(obj)
        self.assertEqual(obj1.position, obj.position)
        self.assertEqual(obj1.velocity, obj.velocity)
        self.assertEqual(obj1.mass, obj.mass)

        for i in range(int(delta / 0.01)):
            PhysicsManager.step([obj1], 0.01)

        self.assertEqual(obj1.position.x, 1)
        self.assertAlmostEqual(obj1.position.y, 1 - 0.5 * 9.81 * delta ** 2)

        self.assertEqual(obj1.velocity.x, 0)
        self.assertAlmostEqual(obj1.velocity.y, -9.81 * delta)