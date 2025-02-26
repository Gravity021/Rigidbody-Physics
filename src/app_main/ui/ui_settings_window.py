import pygame
import pygame_gui

from .ui_fields import *

from ..physics import PhysicsManager as pm

from ..util.debug import Debug
from ..util.time import Time

class SettingsWindow(pygame_gui.elements.UIWindow):
    """A window for adjusting settings of the application."""

    def __init__(self, ui_manager: pygame_gui.UIManager):
        # super().__init__(pygame.Rect(270, 50, 220, 400), ui_manager, "Settings", resizable=True, visible=0)
        super().__init__(pygame.Rect(270, 50, 220, 400), ui_manager, "Settings", resizable=True)

        self._time_since_update = 0

        self.set_step_interval = lambda step_interval: None

        self.global_gravity_label, self.global_gravity_entry_x, self.global_gravity_entry_y = create_vector2_field(
            ui_manager, self, "Gravity", Vector2(0, -9.81), pygame.Rect(10, 10, 200, 30))

        self.world_scale_label, self.world_scale_entry = create_float_field(
            ui_manager, self, "World Scale", 16, pygame.Rect(10, 50, 200, 30))

        self.timescale_label, self.timescale_entry = create_float_field(
            ui_manager, self, "Timescale", 1, pygame.Rect(10, 90, 200, 30))

        self.step_interval_label, self.step_interval_entry = create_float_field(
            ui_manager, self, "Step Interval", 0.5, pygame.Rect(10, 130, 200, 30))

    def update(self, time_delta):
        super().update(time_delta)

        self._time_since_update += time_delta
        if self._time_since_update > 0.5:
            self._time_since_update = 0
            
            try:
                pm.global_gravity = Vector2(
                    float(self.global_gravity_entry_x.get_text()), 
                    float(self.global_gravity_entry_y.get_text()))
            except ValueError:
                Debug.log_error(f"Global Gravity field contains invalid float strings: ({
                    self.global_gravity_entry_x.get_text()}, {self.global_gravity_entry_y.get_text()})")

            try:
                value = float(self.world_scale_entry.get_text())
                
                if value <= 0:
                    Debug.log_error(f"World Scale field should be positive! Value provided was {value}!")
                else:
                    pm.world_to_screen_scale = float(self.world_scale_entry.get_text())
            except ValueError:
                Debug.log_error(f"World Scale field contains invalid float string: {self.world_scale_entry.get_text()}")
            
            try:
                value = float(self.timescale_entry.get_text())

                if value <= 0:
                    Debug.log_error(f"Timescale field should be positive! Value provided was {value}!")
                else:
                    Time.timescale = value
            except ValueError:
                Debug.log_error(f"Timescale field contains invalid float string: {self.timescale_entry.get_text()}")
            
            try:
                value = float(self.step_interval_entry.get_text())

                if value <= 0:
                    Debug.log_error(f"Step Interval field should be positive! Value provided was {value}!")
                else:
                    self.set_step_interval(value)
            except ValueError:
                Debug.log_error(f"Step Interval field contains invalid float string: {self.step_interval_entry.get_text()}")
 
    def on_close_window_button_pressed(self):
        """Override method to only hide the window when the close button is pressed."""
        
        super().hide()