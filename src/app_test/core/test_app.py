from unittest import TestCase

import pygame

from app_main.core.app import *

class ApplicationTests(TestCase):
    """Test the Application class."""

    def test_init(self):
        """Test the Application constructor."""
        
        app = Application()

        self.assertTrue(pygame.get_init(), "Check pygame is initialised")
        self.assertTrue(app.running, "app.running")

        self.assertIsNotNone(app.window, "window")
        self.assertIsNotNone(app.event_manager, "event_manager")

        atexit.unregister(app.on_close)

        del app
        pygame.quit()