# (c) Isaac Godman 2024

import pygame, sys

from .window import Window
from .event_manager import EventManager

from ..util.debug import *
from ..util.time import *

import atexit

class Application:
    """The main application class."""

    def __init__(self):
        atexit.register(self.on_close)

        # Log information about the application
        Debug.log_info("Starting Application: Rigidbody Physics App")
        Debug.log_info(f"Python version: Python {sys.version}")
        Debug.log_info(f"Pygame version: pygame{"-ce" if pygame.IS_CE else ""} {pygame.version.ver}")
        Debug.log_info(f"SDL version: {pygame.version.SDL.major}.{pygame.version.SDL.minor}.{pygame.version.SDL.patch}")

        # Ensure pygame is initialized
        pygame.init()
        
        # Begin initialising variables
        self.running: bool = True

        self.window: Window = Window(1024, 768, "Rigidbody Physics", True, [32, 32, 32])
        self.event_manager: EventManager = EventManager()


    def update(self):
        """The method to update the application."""

        self.event_manager.handle_events()
        self.running = not self.event_manager.should_close

        # do logic


        Time.update()
        # print(Time.dt)
        # print(1 / Time.dt)

    def render(self):
        """The method to render the application to the window."""

        self.window.clear()

        # rendering code goes here

        self.window.update()

    def run(self):
        """The method to run the application.
        
        Repeatedly calls the 'update' and 'render' methods until the application closes."""

        while self.running:
            self.update()
            self.render()
    
    def on_close(self):
        """The destructor.
        
        We just need to tidy up after ourselves before we can finish."""

        pygame.quit()

        Debug.log_info(f"Quitting Application: {"Session ended by user" if not self.running else "Session ended unexpectedly"}")
        Debug.print_pretty_logs()