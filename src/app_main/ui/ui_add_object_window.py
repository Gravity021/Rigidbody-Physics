import pygame
import pygame_gui

class AddObjectWindow(pygame_gui.elements.UIWindow):
    """A window for adding new objects to the simulation."""

    def __init__(self, ui_manager: pygame_gui.UIManager):
        super().__init__(pygame.Rect(510, 50, 220, 400), ui_manager, "Add Object", resizable=True, visible=0)
    
    def on_close_window_button_pressed(self):
        """Override method to only hide the window when the close button is pressed."""

        super().hide()