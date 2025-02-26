from copy import copy
from enum import Enum

import pygame

from ..util.debug import Debug
from ..util.time import Time

from ..maths.Vector2 import Vector2

from . import PhysicsManager as pm
from .object import Object

class Scene:
    """The object representing the physics simulation scene.
    
    Contains a list of objects that exist in the scene, and methods to update and render them to a given surface."""

    class SceneState(Enum):
        NONE = 0,
        EDIT = 1,
        PAUSE = 2,
        PLAY = 3

    def __init__(self):
        self._state: Scene.SceneState = Scene.SceneState.EDIT

        self.file_path: str = None

        self.step_interval: float = 0.5

        self.objects: list[Object] = []
        self._sim_objects: list[Object] = None

    def update(self):
        """Update the physics simulation scene."""

        if self._state == Scene.SceneState.PLAY:
            pm.step(self._sim_objects, Time.dt)
    
    def step(self, delta):
        """Update the simulation by a fixed amount of time."""

        for i in range(int(delta * 60)):
            pm.step(self._sim_objects, 1/60)
    
    def render(self, surface: pygame.Surface):
        """Render the physics simulation scene to the given surface."""

        objects = self._sim_objects
        if self._state == Scene.SceneState.EDIT:
            objects = self.objects

        # Ensure all objects are rendered to the screen.
        for object in objects:
            if object.object_type == Object.ObjectType.CIRCLE: # If the object is a circle ...
                # ... then render a circle.
                pos = pm.world_to_screen_space(object.position)
                pygame.draw.circle(surface, object.colour, Vector2(pos.x, surface.height - pos.y).list, pm.world_to_screen_space(object.dimensions.x))
            elif object.object_type == Object.ObjectType.RECTANGLE: # If the object is a rectangle...
                #... then render a rectangle.
                top_left = [pm.world_to_screen_space(object.position.x) - (pm.world_to_screen_space(object.dimensions.x) // 2),
                            surface.height - pm.world_to_screen_space(object.position.y) - (pm.world_to_screen_space(object.dimensions.y) // 2)]
                pygame.draw.rect(surface, object.colour, top_left + pm.world_to_screen_space(object.dimensions).list)

    def change_state(self, new_state: SceneState):
        """Change the scene into a new state."""

        if new_state not in Scene.SceneState:
            Debug.log_error(f"Invalid SceneState of {new_state}")
            return
        
        if new_state == Scene.SceneState.EDIT:
            self._sim_objects = None
        elif new_state == Scene.SceneState.PLAY and self._state == Scene.SceneState.EDIT:
            self._sim_objects = [copy(obj) for obj in self.objects]
        elif new_state == Scene.SceneState.PAUSE and self._state == Scene.SceneState.EDIT:
            self._sim_objects = [copy(obj) for obj in self.objects]
        
        self._state = new_state
    
    @property
    def state(self) -> SceneState:
        return self._state