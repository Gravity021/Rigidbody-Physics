import pygame
import pygame_gui

class SelectedObjectWindow(pygame_gui.elements.UIWindow):
    def __init__(self, ui_manager: pygame_gui.UIManager):
        super().__init__(pygame.Rect(750, 50, 220, 400), ui_manager, "Selected Object", resizable=True)
    
    def on_close_window_button_pressed(self):
        super().hide()