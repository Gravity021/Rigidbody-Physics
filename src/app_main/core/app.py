# (c) Isaac Godman 2024

import pygame, sys, os

from .window import Window
from .event_manager import EventManager

from ..physics.scene import Scene

from ..ui.ui_manager import *

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

        # Ensure that the window size is correct for scaled displays on windows
        # TODO: Make this work on other platforms?
        os.environ["SDL_WINDOWS_DPI_AWARENESS"] = "permonitorv2"

        # Ensure pygame is initialized
        pygame.init()
        
        # Begin initialising variables
        self.running: bool = True

        self.window: Window = Window(1024, 768, "Rigidbody Physics", True, [32, 32, 32])
        self.event_manager: EventManager = EventManager()

        self.ui_manager = UIManager(self.window.size, self.event_manager.register_action)
        self.menu_bar_manager = MenuBarUIManager(self.window.size, self.event_manager.register_action)

        self.scene = Scene()

        self.menu_bar_manager.menu_bar.set_scene_ref(self.scene)
        self.ui_manager.settings_window.set_step_interval = self.scene.set_step_interval
        self.ui_manager.add_object_window.scene_ref = self.scene

    def update(self):
        """The method to update the application."""

        self.event_manager.handle_events(self.menu_bar_manager.process_events, self.ui_manager.process_events)
        self.running = not self.event_manager.should_close

        # do logic
        self.scene.update()

        self.ui_manager.update(Time.true_dt)
        self.menu_bar_manager.update(Time.true_dt)

        Time.update()
        self.menu_bar_manager.menu_bar.fps_label.set_text(f"FPS: {{:.2f}}".format(1 / Time.true_dt))

    def render(self):
        """The method to render the application to the window."""

        self.window.clear()

        # rendering code goes here
        self.scene.render(self.window.screen)

        self.ui_manager.draw_ui(self.window.screen)
        self.menu_bar_manager.draw_ui(self.window.screen)

        self.window.update()

    def run(self):
        """The method to run the application.
        
        Repeatedly calls the 'update' and 'render' methods until the application closes."""

        Time.start_timer()

        while self.running:
            self.update()
            self.render()
    
    def on_close(self):
        """The destructor.
        
        We just need to tidy up after ourselves before we can finish."""

        pygame.quit()

        Debug.log_info(f"Quitting Application: {"Session ended by user" if not self.running else "Session ended unexpectedly"}")
        Debug.print_pretty_logs()