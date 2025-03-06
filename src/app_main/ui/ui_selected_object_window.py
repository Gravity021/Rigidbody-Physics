import pygame
import pygame_gui

from ..util.debug import Debug

from .ui_fields import *

from ..physics.object import *

class SelectedObjectWindow(pygame_gui.elements.UIWindow):
    """A window for displaying information about the currently selected object."""

    def __init__(self, ui_manager: pygame_gui.UIManager):
        super().__init__(pygame.Rect(750, 50, 220, 400), ui_manager, "Selected Object", resizable=True, visible=0)

        self.scene_ref = None
        self._object = None
        self._time_since_update = 0

        self.object_type_label, self.object_type_entry = create_dropdown_field(
            ui_manager, self, "Object Type", ["None", "Circle", "Rectangle"], "None", pygame.Rect(10, 10, 200, 30))
        self.object_type_entry.disable()

        self.position_label, self.position_entry_x, self.position_entry_y = create_vector2_field(
            ui_manager, self, "Position", Vector2(0, 0), pygame.Rect(10, 50, 200, 30))
        self.position_entry_x.disable()
        self.position_entry_y.disable()

        self.dimensions_label, self.dimensions_entry_x, self.dimensions_entry_y = create_vector2_field(
            ui_manager, self, "Dimensions", Vector2(0, 0), pygame.Rect(10, 90, 200, 30))
        self.dimensions_entry_x.disable()
        self.dimensions_entry_y.disable()

        self.mass_label, self.mass_entry = create_float_field(
            ui_manager, self, "Mass", 0, pygame.Rect(10, 130, 200, 30))
        self.mass_entry.disable()

        self.velocity_label, self.velocity_entry_x, self.velocity_entry_y = create_vector2_field(
            ui_manager, self, "Velocity", Vector2(0, 0), pygame.Rect(10, 170, 200, 30))
        self.velocity_entry_x.disable()
        self.velocity_entry_y.disable()

        self.force_label, self.force_entry_x, self.force_entry_y = create_vector2_field(
            ui_manager, self, "Force", Vector2(0, 0), pygame.Rect(10, 210, 200, 30))
        self.force_entry_x.disable()
        self.force_entry_y.disable()
        
        self.colour_label, self.colour_surface, self.colour_image, self.colour_button, self.colour_window = create_colour_field(
            ui_manager, self, "Colour", [255, 255, 255, 255], pygame.Rect(10, 250, 200, 30))
        self.colour_button.disable()

    def set_object(self, new_object: Object):
        if new_object is None:
            self.object_type_entry = pygame_gui.elements.UIDropDownMenu(
                ["None"],
                "None",
                self.object_type_entry.get_relative_rect(),
                self.object_type_entry.ui_manager,
                container=self.object_type_entry.ui_container,
                parent_element=self.object_type_entry.parent_element,
                anchors={"left": "left", "right": "right"}
            )
            self.object_type_entry.disable()
            
            self.position_entry_x.set_text("0")
            self.position_entry_x.disable()
            self.position_entry_y.set_text("0")
            self.position_entry_y.disable()
            
            self.dimensions_entry_x.set_text("0")
            self.dimensions_entry_x.disable()
            self.dimensions_entry_y.set_text("0")
            self.dimensions_entry_y.disable()
            
            self.mass_entry.set_text("0")
            self.mass_entry.disable()
            
            self.velocity_entry_x.set_text("0")
            self.velocity_entry_x.disable()
            self.velocity_entry_y.set_text("0")
            self.velocity_entry_y.disable()
            
            self.force_entry_x.set_text("0")
            self.force_entry_x.disable()
            self.force_entry_y.set_text("0")
            self.force_entry_y.disable()
            
            self.colour_surface.fill((255, 255, 255, 255))
            self.colour_image.set_image(self.colour_surface)
            self.colour_window.set_colour(pygame.Color(255, 255, 255, 255))
            self.colour_button.disable()
        
        else:
            obj_type = "None"
            if new_object.object_type == Object.ObjectType.CIRCLE: obj_type = "Circle"
            elif new_object.object_type == Object.ObjectType.RECTANGLE: obj_type = "Rectangle"
            self.object_type_entry = pygame_gui.elements.UIDropDownMenu(
                ["None", "Circle", "Rectangle"],
                obj_type,
                self.object_type_entry.get_relative_rect(),
                self.object_type_entry.ui_manager,
                container=self.object_type_entry.ui_container,
                parent_element=self.object_type_entry.parent_element,
                anchors={"left": "left", "right": "right"}
            )
            
            self.position_entry_x.set_text(str(new_object.position.x))
            self.position_entry_x.enable()
            self.position_entry_y.set_text(str(new_object.position.y))
            self.position_entry_y.enable()

            self.dimensions_entry_x.set_text(str(new_object.dimensions.x))
            self.dimensions_entry_x.enable()
            self.dimensions_entry_y.set_text(str(new_object.dimensions.y))
            self.dimensions_entry_y.enable()

            self.mass_entry.set_text(str(new_object.mass))
            self.mass_entry.enable()

            self.velocity_entry_x.set_text(str(new_object.velocity.x))
            self.velocity_entry_x.enable()
            self.velocity_entry_y.set_text(str(new_object.velocity.y))
            self.velocity_entry_y.enable()

            self.force_entry_x.set_text(str(new_object.force.x))
            self.force_entry_x.enable()
            self.force_entry_y.set_text(str(new_object.force.y))
            self.force_entry_y.enable()

            self.colour_surface.fill(new_object.colour)
            self.colour_image.set_image(self.colour_surface)
            self.colour_window.set_colour(pygame.Color(new_object.colour))
            self.colour_button.enable()

    def update(self, time_delta):
        super().update(time_delta)

        if self._object != self.scene_ref.selected_object:
            self._object = self.scene_ref.selected_object
            self.set_object(self._object)

        self._time_since_update += time_delta
        if self._time_since_update > 0.5:
            self._time_since_update = 0
            
            if self._object != None:
                if self.object_type_entry.current_state.selected_option[0] == "Circle":
                    obj_type = Object.ObjectType.CIRCLE
                elif self.object_type_entry.current_state.selected_option[0] == "Rectangle":
                    obj_type = Object.ObjectType.RECTANGLE
                else:
                    Debug.log_error("Failed to update selected object: invalid object type")
                    return
                
                try:
                    position = Vector2(float(self.position_entry_x.get_text()), float(self.position_entry_y.get_text()))
                except ValueError:
                    Debug.log_error(f"Failed to update selected object: position field contains invalid float strings: ({
                        self.position_entry_x.get_text()}, {self.position_entry_y.get_text()})")
                    return
                
                try:
                    dimensions = Vector2(float(self.dimensions_entry_x.get_text()), float(self.dimensions_entry_y.get_text()))
                except ValueError:
                    Debug.log_error(f"Failed to update selected object: dimensions field contains invalid float strings: ({
                        self.dimensions_entry_x.get_text()}, {self.dimensions_entry_y.get_text()})")
                    return
            
                try:
                    mass = float(self.mass_entry.get_text())
                except ValueError:
                    Debug.log_error(f"Failed to update selected object: mass field contains invalid float string: {
                        self.mass_entry.get_text()}")
                    return

                try:
                    velocity = Vector2(float(self.velocity_entry_x.get_text()), float(self.velocity_entry_y.get_text()))
                except ValueError:
                    Debug.log_error(f"Failed to update selected object: velocity field contains invalid float strings: ({
                        self.velocity_entry_x.get_text()}, {self.velocity_entry_y.get_text()})")
                    return
                
                try:
                    force = Vector2(float(self.force_entry_x.get_text()), float(self.force_entry_y.get_text()))
                except ValueError:
                    Debug.log_error(f"Failed to update selected object: force field contains invalid float strings: ({
                        self.force_entry_x.get_text()}, {self.force_entry_y.get_text()})")
                    return
                
                colour = self.colour_surface.get_at((0, 0))

                self._object.object_type = obj_type
                self._object.position = position
                self._object.dimensions = dimensions
                self._object.mass = mass
                self._object.velocity = velocity
                self._object.force = force
                self._object.colour = colour
            
    def on_colour_change(self, event):
        if event.ui_element == self.colour_window:
            self.colour_surface.fill(pygame.Color(*event.colour))
            self.colour_image.set_image(self.colour_surface)

    def on_close_window_button_pressed(self):
        """Override method to only hide the window when the close button is pressed."""
        
        super().hide()