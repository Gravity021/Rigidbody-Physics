import pickle

from ..physics.object import *
from ..physics.scene import Scene
from ..physics import PhysicsManager as pm

from ..util.time import Time

class SerializableData:
    def __init__(self, objects: list[Object], world_to_screen_scale: float,
                 global_gravity: Vector2, timescale: float, step_interval: float):
        self.objects = objects
        self.world_to_screen_scale = world_to_screen_scale
        self.global_gravity = global_gravity
        self.timescale = timescale
        self.step_interval = step_interval

def serialize_data(filepath: str, data: SerializableData):
    pickle_data = pickle.dumps(data)
    with open(filepath, "wb") as file:
        pickle.dump(data, file)
        # file.write(pickle_data)
        file.close()

def serialize(filepath: str, objects: list[Object], step_interval: float):
    data = SerializableData(
      objects, pm.world_to_screen_scale, pm.global_gravity, 
      Time.timescale, step_interval)

    with open(filepath, "wb") as file:
        pickle.dump(data, file)
        file.close()

def deserialize_data(filepath: str) -> SerializableData:
    with open(filepath, "rb") as file:
        obj = pickle.load(file)
        file.close()
    
    return obj

def deserialize(filepath: str, scene: Scene):
    with open(filepath, "rb") as file:
        obj = pickle.load(file)
        file.close()

    scene.objects = obj.objects
    pm.world_to_screen_scale = obj.world_to_screen_scale
    pm.global_gravity = obj.global_gravity
    Time.timescale = obj.timescale
    scene.step_interval = obj.step_interval