from typing import Callable
import pygame
import pygame_gui

from .ui_menu_bar import MenuBar
from .ui_demo_window import DemoWindow
from .ui_settings_window import SettingsWindow
from .ui_add_object_window import AddObjectWindow
from .ui_selected_object_window import SelectedObjectWindow

# TODO: Properly comment UI components

class UIManager(pygame_gui.UIManager):
    """The main UIManager.
    
    Wraps `pygame_gui.UIManager`, with some additional changes.
    This wrapper is offset by 30px from the top of the window, to allow for the menu bar.
    
    Stores and responsible for all UI Windows in the application."""

    def __init__(self, window_size: tuple[int, int], register_event_handler: Callable[[int, Callable[[pygame.Event], None]], None]) -> None:
        super().__init__([window_size[0], window_size[1] - 31])
        self.root_container.set_position((0, 30))                       # Offset root container by 30px from the top of the window

        self.register_event_fn = register_event_handler                 # Store a method to add event handlers
        
        self.register_event_fn(pygame.WINDOWRESIZED, lambda event: self.set_window_resolution((event.x, event.y - 30)))     # Resize window on window resize
        self.register_event_fn(pygame.KEYDOWN, lambda event: self.toggle_visual_debug_mode(event))                          # Toggle debug mode on F1 press

        # Instantiate UI windows
        self.test_window = DemoWindow(self)
        
        self.settings_window = SettingsWindow(self)

        self.add_object_window = AddObjectWindow(self)
        self.selected_object_window = SelectedObjectWindow(self)
    
    def toggle_visual_debug_mode(self, event) -> None:
        """Toggles the visual debug mode."""

        if event.key == pygame.K_F1:
            print("UIManager: ")
            self.set_visual_debug_mode(not self.visual_debug_active)

class MenuBarUIManager(pygame_gui.UIManager):
    """The secondary UIManager for the menu bar.
    
    Wraps `pygame_gui.UIManager`, with some additional changes.
    This wrapper is only 200px tall to allow for the menu bar, and nothing else.
    
    Responsible only for the menu bar."""

    def __init__(self, window_size: tuple[int, int], register_event_handler: Callable[[int, Callable[[pygame.Event], None]], None]) -> None:
        super().__init__([window_size[0], 200])

        self.register_event_fn = register_event_handler                 # Store a method to add event handlers
        
        self.register_event_fn(pygame.WINDOWRESIZED, lambda event: self.set_window_resolution((event.x, 200)))      # Resize window on window resize
        self.register_event_fn(pygame.KEYDOWN, lambda event: self.toggle_visual_debug_mode(event))                  # Toggle debug mode on F1 press

        self.menu_bar = MenuBar(self, window_size[0])

        self.register_event_fn(pygame_gui.UI_FILE_DIALOG_PATH_PICKED, self.menu_bar._save_simulation)
        self.register_event_fn(pygame_gui.UI_FILE_DIALOG_PATH_PICKED, self.menu_bar._load_simulation)
    
    def toggle_visual_debug_mode(self, event) -> None:
        """Toggles the visual debug mode."""

        if event.key == pygame.K_F1:
            print("MenuBarUIManager: ")
            self.set_visual_debug_mode(not self.visual_debug_active)
