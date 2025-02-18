import pygame

from ..maths.Vector2 import Vector2

from . import PhysicsManager as pm
from .object import Object

class Scene:
    """The object representing the physics simulation scene.
    
    Contains a list of objects that exist in the scene, and methods to update and render them to a given surface."""

    def __init__(self):
        self.objects: list[Object] = []

    def update(self):
        """Update the physics simulation scene."""

        pm.step(self.objects)
    
    def render(self, surface: pygame.Surface):
        """Render the physics simulation scene to the given surface."""

        # Ensure all objects are rendered to the screen.
        for object in self.objects:
            if object.object_type == Object.ObjectType.CIRCLE: # If the object is a circle ...
                # ... then render a circle.
                pos = pm.world_to_screen_space(object.position)
                pygame.draw.circle(surface, object.colour, Vector2(pos.x, surface.height - pos.y).list, pm.world_to_screen_space(object.dimensions.x))
            elif object.object_type == Object.ObjectType.RECTANGLE: # If the object is a rectangle...
                #... then render a rectangle.
                top_left = [pm.world_to_screen_space(object.position.x) - (pm.world_to_screen_space(object.dimensions.x) // 2),
                            surface.height - pm.world_to_screen_space(object.position.y) - (pm.world_to_screen_space(object.dimensions.y) // 2)]
                pygame.draw.rect(surface, object.colour, top_left + pm.world_to_screen_space(object.dimensions).list)
