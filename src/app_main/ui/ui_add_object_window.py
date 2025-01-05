import pygame
import pygame_gui

from ..core.event_manager import EventManager

class AddObjectWindow(pygame_gui.elements.UIWindow):
    def __init__(self, ui_manager: pygame_gui.UIManager):
        super().__init__(pygame.Rect(510, 50, 220, 400), ui_manager, "Add Object", resizable=True)
    
    def on_close_window_button_pressed(self):
        super().hide()