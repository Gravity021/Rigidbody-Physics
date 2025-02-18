# (c) Isaac Godman 2024

from typing import Callable
import pygame

from ..util.debug import Debug

class EventManager:
    """The class responsible for handling events collected by pygame."""

    def __init__(self) -> None:
        self._event_map = {}
        self.reset_event_map()

        self._mouse_pos = (-1, -1)
        # self._last_mouse_pos = (-1, -1)
        self._mouse_buttons = [False, False, False, False, False]
        # self._last_mouse_buttons = [False, False, False, False, False]
        self._should_close = False

    def handle_events(self, *handlers: list[Callable[[pygame.Event], bool]]):
        # self._last_mouse_buttons = self._mouse_buttons.copy()
        
        # self._last_mouse_pos = deepcopy(self._mouse_pos)

        # Copy the mouse position from pygame
        self._mouse_pos = pygame.mouse.get_pos()

        # Handle events from pygame
        for event in pygame.event.get():
            # If the event is the quit button press, then set that we should close
            if event.type == pygame.QUIT:
                self._should_close = True
            
            # If the event is a mouse button event, set the appropriate button to the appropriate state
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_buttons[event.button - 1] = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_buttons[event.button - 1] = False

            if (event.type in self._event_map.keys()):
                if len(self._event_map[event.type]) == 0:
                    Debug.log_warning(f"Unhandled event of type {pygame.event.event_name(event.type)}")
                    print(f"Unhandled event of type {pygame.event.event_name(event.type)}")
                else: 
                    for action in self._event_map[event.type]: action(event)
            
            handled = False  # Assume no event is handled by default
            for handler in handlers:
                handled = handler(event)
                if handled: break
    
    def reset_event_map(self) -> None:
        """Set the event map to a default."""

        self._event_map = {
            pygame.KEYDOWN: [],
            pygame.KEYUP: []
        }
    
    def register_action(self, event_type: int, action: Callable[[pygame.Event], None]) -> None:
        """Add an action to the event map.
        
        Parameters:
        - event_type (int): The ID corresponding to the type of event to listen to.
        - action (Callable): The method to perform when the required event is received. Must accept a 'pygame.Event'."""

        if not event_type in self._event_map:
            self._event_map[event_type] = []

        self._event_map[event_type].append(action)

    @property
    def mouse_pos(self) -> tuple[int, int]:
        return self._mouse_pos
    
    # @property
    # def last_mouse_pos(self):
    #     return self._last_mouse_pos
    
    @property
    def mouse_buttons(self) -> list[bool, bool, bool, bool, bool]:
        return self._mouse_buttons
    
    # @property
    # def last_mouse_buttons(self):
    #     return self._last_mouse_buttons
    
    @property
    def should_close(self) -> bool:
        """Get if the window should close this frame."""
        return self._should_close

    def set_should_close(self) -> None:
        """Set that the window should close this frame."""
        self._should_close = True
