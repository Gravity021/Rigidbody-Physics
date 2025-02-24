from .object import Object

from ..maths.Vector2 import Vector2

global_gravity = Vector2(0, -9.81)
"""The acceleration due to gravity.

This affects all objects in the scene that are dynamic."""

world_to_screen_scale = 16
"""The scale factor to convert between world space and screen space."""

def step(objects: list[Object], delta_time: float):
    """Perform a step of the physics simulation.

    Updates the positions and velocities of the objects based on their forces and mass.
    """

    # Update the positions and velocities of the objects based on their forces and mass.
    for object in objects: 
        # Add the global gravity force to the object's force.
        object.force += global_gravity * object.mass

        # Update velocity and position based on force and mass, according to Newton's laws of motion (using Verlet Integration).
        object.position += object.velocity * delta_time + (object.force / object.mass) * 0.5 * (delta_time ** 2)
        object.velocity += object.force / object.mass * delta_time

        # Remove the global gravity force from the object.
        # This ensures that this is not affected by other forces.
        object.force -= global_gravity * object.mass
    
    # for object_a in objects: 
    #     for object_b in objects:
    #         pass

def world_to_screen_space(length: float) -> float:
    """Convert a length from world space to screen space."""

    return length * world_to_screen_scale

def world_to_screen_space(position: Vector2) -> Vector2:
    """Convert a position from world space to screen space."""

    return position * world_to_screen_scale

def screen_to_world_space(length: float) -> float:
    """Convert a length from screen space to world space."""

    return length / world_to_screen_scale

def screen_to_world_space(position: Vector2) -> Vector2:
    """Convert a position from screen space to world space."""

    return position / world_to_screen_scale