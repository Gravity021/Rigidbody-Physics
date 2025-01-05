from typing import Callable
import pygame
import pygame_gui

from .ui_menu_bar import MenuBar
from .ui_demo_window import DemoWindow
class UIManager(pygame_gui.UIManager):
    def __init__(self, window_size: tuple[int, int], register_event_handler: Callable[[int, Callable[[pygame.Event], None]], None]) -> None:
        super().__init__(window_size)

        self.menu_bar = MenuBar(self, window_size[0])

        self.test_window = DemoWindow(self)
    
    def toggle_visual_debug_mode(self, event) -> None:
        if event.key == pygame.K_F1:
            self.set_visual_debug_mode(not self.visual_debug_active)