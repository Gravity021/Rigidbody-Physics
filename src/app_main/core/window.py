# (c) Isaac Godman

import time
import pygame, math

from ..util.debug import Debug

class Window:
    """The class representing the wrapper for the pygame window."""

    def __init__(self, width: int, height: int, title: str, resizable: bool, clear_colour: list[3] = [255, 255, 255], vsync: bool = True):
        """The class representing the wrapper for the pygame window.
        
        Constructor parameters:
        - width (int): The initial width of the window
        - height (int): The initial height of the window
        - title (str): The title of the window
        - resizable (bool): Should the window be able to be resized

        - clear_colour (list[3] of int): The background colour of the window (defaults to white)
        - vsync (bool): Shoud the window try to synchronize with the display (defaults to True) 
        """

        self.width = width
        self.height = height
        self.title = title
        pygame.display.set_caption(self.title)

        self.clear_colour = Window.validate_colour(clear_colour)

        self._window_flags = 0
        # self._window_flags |= pygame.OPENGL
        if resizable: self._window_flags |= pygame.RESIZABLE
        self._vsync = int(vsync)
        
        try:
            self.screen = pygame.display.set_mode((width, height), self._window_flags, vsync=self._vsync)
        except pygame.error as err:
            # TODO: check it is v-sync causing the issue
            self.screen = pygame.display.set_mode((width, height), self._window_flags)
            self._vsync = 0
            Debug.log_warning("Requested v-sync, but not available. Continuing without.")
    
    def clear(self) -> None:
        """A method to clear the window.
        
        Clears the window to 'Window.clear_colour'."""

        self.screen.fill(self.clear_colour)
    
    def fill(self, colour: list[int, int, int] | tuple[int, int, int]) -> None:
        """A method to fill the window with a solid colour.
        
        Parameters:
            colour (list[3] of int): the colour to fill the window with."""
        
        self.screen.fill(Window.validate_colour(colour))

    def update(self) -> None:
        """The method to update the pygame window."""

        pygame.display.flip()

    @property
    def resizable(self) -> bool:
        """Returns if the window is resizable."""
        return bool(self._window_flags & pygame.RESIZABLE)
    
    @property
    def size(self) -> tuple[int, int]:
        """Returns the size of the window."""
        return (self.width, self.height)

    @property
    def centre(self) -> tuple[int, int]:
        """Returns the center of the window."""
        return (self.width // 2, self.height // 2)
    
    def validate_colour(colour) -> list[int, int, int]:
        """Ensure that a colour specified is valid for use in pygame.
        
        Clamps each component to [0 - 255] inclusive."""
        return [
            max(0, min(colour[0], 255)),
            max(0, min(colour[1], 255)),
            max(0, min(colour[2], 255))
        ]