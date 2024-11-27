# (c) Isaac Godman 2024

from typing import Callable
import pygame
from copy import deepcopy

from ..util.debug import Debug

class EventManager:
    """The class responsible for handling events collected by pygame."""

    def __init__(self):
        self._event_map = {}
        self.reset_event_map()

        self._mouse_pos = (-1, -1)
        # self._last_mouse_pos = (-1, -1)
        self._mouse_buttons = [False, False, False, False, False]
        # self._last_mouse_buttons = [False, False, False, False, False]
        self._should_close = False

    def handle_events(self):
        # self._last_mouse_buttons = self._mouse_buttons.copy()
        
        # self._last_mouse_pos = deepcopy(self._mouse_pos)
        self._mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._should_close = True
            
            elif event.type == pygame.KEYDOWN:
                try: 
                    for action in self._event_map[pygame.KEYDOWN][event.key]: action()
                except KeyError as err: Debug.log_warning(f"KEYDOWN event for key {event.key} with no listener!")
            
            elif event.type == pygame.KEYUP:
                try:
                    for action in self._event_map[pygame.KEYUP][event.key]: action()
                except KeyError as err: Debug.log_warning(f"KEYUP event for key {event.key} with no listener!")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_buttons[event.button - 1] = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_buttons[event.button - 1] = False

    def reset_event_map(self):
        self._event_map = {
            pygame.KEYDOWN: {},
            pygame.KEYUP: {}
        }
    
    def register_action(self, event_type: int, event_action: int, action: Callable) -> None:
        if not event_type in self._event_map:
            self._event_map[event_type] = {}
        if not event_action in self._event_map[event_type]:
            self._event_map[event_type][event_action] = []

        self._event_map[event_type][event_action].append(action)

    @property
    def mouse_pos(self):
        return self._mouse_pos
    
    # @property
    # def last_mouse_pos(self):
    #     return self._last_mouse_pos
    
    @property
    def mouse_buttons(self):
        return self._mouse_buttons
    
    # @property
    # def last_mouse_buttons(self):
    #     return self._last_mouse_buttons
    
    @property
    def should_close(self):
        return self._should_close

    def set_should_close(self) -> None:
        self._should_close = True
