import pygame
import pygame_gui

class SelectedObjectWindow(pygame_gui.elements.UIWindow):
    """A window for displaying information about the currently selected object."""

    def __init__(self, ui_manager: pygame_gui.UIManager):
        super().__init__(pygame.Rect(750, 50, 220, 400), ui_manager, "Selected Object", resizable=True, visible=0)
    
    def on_close_window_button_pressed(self):
        """Override method to only hide the window when the close button is pressed."""
        
        super().hide()