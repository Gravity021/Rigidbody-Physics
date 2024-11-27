from unittest import TestCase

import pygame

from app_main.core.app import *

class ApplicationTests(TestCase):
    def test_init(self):
        app = Application()

        self.assertTrue(pygame.get_init(), "Check pygame is initialised")
        self.assertTrue(app.running, "app.running")

        self.assertIsNotNone(app.window, "window")
        self.assertIsNotNone(app.event_manager, "event_manager")