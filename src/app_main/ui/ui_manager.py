from typing import Callable
import pygame
import pygame_gui

class UIManager(pygame_gui.UIManager):
    def __init__(self, window_size: tuple[int, int], register_event_handler: Callable[[int, Callable[[pygame.Event], None]], None]) -> None:
        super().__init__(window_size)
    
    def toggle_visual_debug_mode(self, event) -> None:
        if event.key == pygame.K_F1:
            self.set_visual_debug_mode(not self.visual_debug_active)