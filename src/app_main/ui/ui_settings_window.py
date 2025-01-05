import pygame
import pygame_gui

from ..core.event_manager import EventManager

class SettingsWindow(pygame_gui.elements.UIWindow):
    def __init__(self, ui_manager: pygame_gui.UIManager):
        super().__init__(pygame.Rect(270, 50, 220, 400), ui_manager, "Settings", resizable=True)
    
    def on_close_window_button_pressed(self):
        super().hide()