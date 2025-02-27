import pygame
import pygame_gui

from .ui_fields import *

from ..physics.object import Object

from ..util.debug import Debug

class AddObjectWindow(pygame_gui.elements.UIWindow):
    """A window for adding new objects to the simulation."""

    def __init__(self, ui_manager: pygame_gui.UIManager):
        super().__init__(pygame.Rect(510, 50, 220, 400), ui_manager, "Add Object", resizable=True, visible=0)

        self.scene_ref = None

        self.object_type_label, self.object_type_entry = create_dropdown_field(ui_manager, self, "Object Type", ["None", "Circle", "Rectangle"], "None", pygame.Rect(10, 10, 200, 30))

        self.position_label, self.position_entry_x, self.position_entry_y = create_vector2_field(ui_manager, self, "Position", Vector2(0, 0), pygame.Rect(10, 50, 200, 30))

        self.dimensions_label, self.dimensions_entry_x, self.dimensions_entry_y = create_vector2_field(ui_manager, self, "Dimensions", Vector2(0, 0), pygame.Rect(10, 90, 200, 30))

        self.mass_label, self.mass_entry = create_float_field(ui_manager, self, "Mass", 1, pygame.Rect(10, 130, 200, 30))

        self.velocity_label, self.velocity_entry_x, self.velocity_entry_y = create_vector2_field(ui_manager, self, "Velocity", Vector2(0, 0), pygame.Rect(10, 170, 200, 30))

        self.force_label, self.force_entry_x, self.force_entry_y = create_vector2_field(ui_manager, self, "Force", Vector2(0, 0), pygame.Rect(10, 210, 200, 30))
        
        self.colour_label, self.colour_surface, self.colour_image, self.colour_button, self.colour_window = create_colour_field(ui_manager, self, "Colour", [255, 255, 255, 255], pygame.Rect(10, 250, 200, 30))

        self.create_button = pygame_gui.elements.UIButton(
            pygame.Rect(0, -50, 200, 40),
            "Create Object",
            ui_manager,
            command = self.create_object,
            parent_element = self,
            container = self,
            anchors = {"bottom": "bottom", "centerx": "centerx"}
        )
    
    def create_object(self):
        if self.object_type_entry.current_state.selected_option[0] == "Circle":
            obj_type = Object.ObjectType.CIRCLE
        elif self.object_type_entry.current_state.selected_option[0] == "Rectangle":
            obj_type = Object.ObjectType.RECTANGLE
        else:
            Debug.log_error("Failed to create new object: invalid object type")
            return
        
        try:
            position = Vector2(float(self.position_entry_x.get_text()), float(self.position_entry_y.get_text()))
        except ValueError:
            Debug.log_error(f"Failed to create new object: position field contains invalid float strings: ({self.position_entry_x.get_text()}, {self.position_entry_y.get_text()})")
            return
        
        try:
            dimensions = Vector2(float(self.dimensions_entry_x.get_text()), float(self.dimensions_entry_y.get_text()))
        except ValueError:
            Debug.log_error(f"Failed to create new object: dimensions field contains invalid float strings: ({self.dimensions_entry_x.get_text()}, {self.dimensions_entry_y.get_text()})")
            return
    
        try:
            mass = float(self.mass_entry.get_text())
        except ValueError:
            Debug.log_error(f"Failed to create new object: mass field contains invalid float string: {self.mass_entry.get_text()}")
            return

        try:
            velocity = Vector2(float(self.velocity_entry_x.get_text()), float(self.velocity_entry_y.get_text()))
        except ValueError:
            Debug.log_error(f"Failed to create new object: velocity field contains invalid float strings: ({self.velocity_entry_x.get_text()}, {self.velocity_entry_y.get_text()})")
            return
        
        try:
            force = Vector2(float(self.force_entry_x.get_text()), float(self.force_entry_y.get_text()))
        except ValueError:
            Debug.log_error(f"Failed to create new object: force field contains invalid float strings: ({self.force_entry_x.get_text()}, {self.force_entry_y.get_text()})")
            return
        
        colour = self.colour_surface.get_at((0, 0))

        new_object = Object(obj_type, position, dimensions, mass, velocity, force, 0, colour)

        self.scene_ref.objects.append(new_object)
    
    def on_colour_change(self, event):
        if event.ui_element == self.colour_window:
            self.colour_surface.fill(pygame.Color(*event.colour))
            self.colour_image.set_image(self.colour_surface)

    def on_close_window_button_pressed(self):
        """Override method to only hide the window when the close button is pressed."""

        super().hide()