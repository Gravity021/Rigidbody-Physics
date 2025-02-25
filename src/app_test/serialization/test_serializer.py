from copy import copy
from unittest import TestCase

from app_main.maths.Vector2 import Vector2
from app_main.physics.object import Object
from app_main.physics.scene import Scene
from app_main.physics import PhysicsManager as pm
from app_main.serialization import serializer
from app_main.util.time import Time

class SerializerTests(TestCase):
    def test_serialize_1(self):
        data = serializer.SerializableData([], 16, Vector2(0, -9.81), 1, 0.5)

        serializer.serialize_data("test_serialize_1.data", data)
        data2 = serializer.deserialize_data("test_serialize_1.data")
        
        self.assertEqual(data.objects, data2.objects)
        self.assertEqual(data.world_to_screen_scale, data2.world_to_screen_scale)
        self.assertEqual(data.global_gravity, data2.global_gravity)
        self.assertEqual(data.timescale, data2.timescale)
        self.assertEqual(data.step_interval, data2.step_interval)
    
    def test_serialize_2(self):
        data = serializer.SerializableData(
            [Object(Object.ObjectType.CIRCLE, Vector2(0, 0), Vector2(1, -1), 1), Object(Object.ObjectType.RECTANGLE, Vector2(10, 7), Vector2(2, 0.5), 2)], 
            32, Vector2(5, -3), 0.5, 0.1)

        serializer.serialize_data("test_serialize_2.data", data)
        data2 = serializer.deserialize_data("test_serialize_2.data")
        
        self.assertEqual(data.objects[0].object_type,   data2.objects[0].object_type)
        self.assertEqual(data.objects[0].position,      data2.objects[0].position)
        self.assertEqual(data.objects[0].velocity,      data2.objects[0].velocity)
        self.assertEqual(data.objects[0].force,         data2.objects[0].force)
        self.assertEqual(data.objects[0].colour,        data2.objects[0].colour)
        self.assertEqual(data.objects[0].dimensions,    data2.objects[0].dimensions)

        self.assertEqual(data.objects[1].object_type,   data2.objects[1].object_type)
        self.assertEqual(data.objects[1].position,      data2.objects[1].position)
        self.assertEqual(data.objects[1].velocity,      data2.objects[1].velocity)
        self.assertEqual(data.objects[1].force,         data2.objects[1].force)
        self.assertEqual(data.objects[1].colour,        data2.objects[1].colour)
        self.assertEqual(data.objects[1].dimensions,    data2.objects[1].dimensions)
        
        self.assertEqual(data.world_to_screen_scale,    data2.world_to_screen_scale)
        self.assertEqual(data.global_gravity,           data2.global_gravity)
        self.assertEqual(data.timescale,                data2.timescale)
        self.assertEqual(data.step_interval,            data2.step_interval)

    def test_serialize_3(self):
        scene = Scene()
        
        scale = copy(pm.world_to_screen_scale)
        gravity = copy(pm.global_gravity)
        timescale = copy(Time.timescale)

        serializer.serialize("test_serialize_3.data", [Object(Object.ObjectType.CIRCLE, Vector2(0, 0), Vector2(1, -1), 1), Object(Object.ObjectType.RECTANGLE, Vector2(10, 7), Vector2(2, 0.5), 2)], 0.5)
        serializer.deserialize("test_serialize_3.data", scene)

        self.assertEqual(scene.objects[0].object_type,   Object.ObjectType.CIRCLE)
        self.assertEqual(scene.objects[0].position,      Vector2(0, 0))
        self.assertEqual(scene.objects[0].velocity,      Vector2(0, 0))
        self.assertEqual(scene.objects[0].force,         Vector2(0, 0))
        self.assertEqual(scene.objects[0].colour,        [255, 255, 255, 255])
        self.assertEqual(scene.objects[0].dimensions,    Vector2(1, -1))

        self.assertEqual(scene.objects[1].object_type,   Object.ObjectType.RECTANGLE)
        self.assertEqual(scene.objects[1].position,      Vector2(10, 7))
        self.assertEqual(scene.objects[1].velocity,      Vector2(0, 0))
        self.assertEqual(scene.objects[1].force,         Vector2(0, 0))
        self.assertEqual(scene.objects[1].colour,        [255, 255, 255, 255])
        self.assertEqual(scene.objects[1].dimensions,    Vector2(2, 0.5))
        
        self.assertEqual(scene.step_interval, 0.5)
        self.assertEqual(pm.world_to_screen_scale, scale)
        self.assertEqual(pm.global_gravity, gravity)
        self.assertEqual(Time.timescale, timescale)

    def test_serialize_4(self):
        scene = Scene()

        pm.world_to_screen_scale = 10
        pm.global_gravity = Vector2(5, -3)
        Time.timescale = 0.5

        scale = copy(pm.world_to_screen_scale)
        gravity = copy(pm.global_gravity)
        timescale = copy(Time.timescale)

        serializer.serialize("test_serialize_4.data", [Object(Object.ObjectType.CIRCLE, Vector2(0, 0), Vector2(1, -1), 1), Object(Object.ObjectType.RECTANGLE, Vector2(10, 7), Vector2(2, 0.5), 2)], 0.1)
        serializer.deserialize("test_serialize_4.data", scene)

        self.assertEqual(scene.objects[0].object_type,   Object.ObjectType.CIRCLE)
        self.assertEqual(scene.objects[0].position,      Vector2(0, 0))
        self.assertEqual(scene.objects[0].velocity,      Vector2(0, 0))
        self.assertEqual(scene.objects[0].force,         Vector2(0, 0))
        self.assertEqual(scene.objects[0].colour,        [255, 255, 255, 255])
        self.assertEqual(scene.objects[0].dimensions,    Vector2(1, -1))

        self.assertEqual(scene.objects[1].object_type,   Object.ObjectType.RECTANGLE)
        self.assertEqual(scene.objects[1].position,      Vector2(10, 7))
        self.assertEqual(scene.objects[1].velocity,      Vector2(0, 0))
        self.assertEqual(scene.objects[1].force,         Vector2(0, 0))
        self.assertEqual(scene.objects[1].colour,        [255, 255, 255, 255])
        self.assertEqual(scene.objects[1].dimensions,    Vector2(2, 0.5))
        
        self.assertEqual(scene.step_interval, 0.1)
        self.assertEqual(pm.world_to_screen_scale, scale)
        self.assertEqual(pm.global_gravity, gravity)
        self.assertEqual(Time.timescale, timescale)