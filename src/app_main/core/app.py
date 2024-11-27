# (c) Isaac Godman 2024

import pygame, sys

from .window import Window
from .event_manager import EventManager

from ..util.debug import *
from ..util.time import *


class Application:
    """The main application class."""

    def __init__(self):
        Debug.log_info("Starting Application: Rigidbody Physics App")
        Debug.log_info(f"Python version: Python {sys.version}")
        Debug.log_info(f"Pygame version: pygame{"-ce" if pygame.IS_CE else ""} {pygame.version.ver}")
        Debug.log_info(f"SDL version: {pygame.version.SDL.major}.{pygame.version.SDL.minor}.{pygame.version.SDL.patch}")

        pygame.init()

        Debug()
        Time()
        
        self.running: bool = True

        self.window: Window = Window(int(1024 * 0.75), int(768 * 0.75), "Rigidbody Physics", False, [32, 32, 32])
        # self.window: Window = Window(int(1024 * 0.75), int(768 * 0.75), "Rigidbody Physics", True, [32, 32, 32])
        self.event_manager: EventManager = EventManager()

        self.event_manager.register_action(pygame.KEYDOWN, pygame.K_ESCAPE, lambda: print("Hello, World!"))

    def update(self):
        self.event_manager.handle_events()
        self.running = not self.event_manager.should_close

        # do logic
        print(self.event_manager.mouse_buttons[0])

        Time.update()
        # print(Time.dt)
        # print(1 / Time.dt)

    def render(self):
        self.window.clear()

        # rendering code goes here

        self.window.update()

    def run(self):
        while self.running:
            self.update()
            self.render()
    
    def __del__(self):
        pygame.quit()

        Debug.log_info(f"Quitting Application: {"Session ended by user" if not self.running else "Session ended unexpectedly"}")
        Debug.print_pretty_logs()