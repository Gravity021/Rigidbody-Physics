from unittest import TestCase

from app_main.core.window import *

class WindowTests(TestCase):
    """Test the Window class."""

    def test_init(self):
        """Test the Window constructor."""

        Debug._messages = []

        # Test case 1
        # All Valid
        pygame.init()
        window = Window(1024, 768, "Rigidbody Physics", False, [32, 32, 32])

        self.assertEqual(window.width, 1024, "width")
        self.assertEqual(window.height, 768, "height")
        self.assertEqual(window.title, "Rigidbody Physics", "title")
        self.assertEqual(pygame.display.get_caption()[0], "Rigidbody Physics", "caption")
        
        self.assertFalse(window._window_flags & pygame.RESIZABLE, "resizable")
        
        self.assertEqual(window.clear_colour, [32, 32, 32], "clear colour")

        self.assertEqual(window._vsync, 1, "v-sync. WARNING, may fail if the display doesn't support v-sync.")

        self.assertIsNotNone(window.screen, "screen")

        del window
        pygame.quit()

        # Test case 2
        # Test Resizing and invalid clear colour
        pygame.init()
        window = Window(1500, 1000, "Test Window Name", True, [-1, -1, -1])

        self.assertEqual(window.width, 1500, "width")
        self.assertEqual(window.height, 1000, "height")
        self.assertEqual(window.title, "Test Window Name", "title")
        self.assertEqual(pygame.display.get_caption()[0], "Test Window Name", "caption")
        
        self.assertTrue(window._window_flags & pygame.RESIZABLE, "resizable")
        
        self.assertEqual(window.clear_colour, [0, 0, 0], "clear colour")

        # self.assertEqual(window._vsync, 1, f"v-sync. WARNING, may fail if the display doesn't support v-sync.\n{Debug._messages}")
        present = False
        for message in Debug._messages: present |= message["message"] == "Requested v-sync, but not available. Continuing without."
        self.assertEqual(window._vsync, 1- int(present), f"v-sync")

        self.assertIsNotNone(window.screen, "screen")

        del window
        pygame.quit()

        # Test case 3
        # Test mixed clear colours, v-sync disabled
        pygame.init()
        window = Window(1500, 1000, "Test Window Name", True, [100, -500, 500], False)

        self.assertEqual(window.width, 1500, "width")
        self.assertEqual(window.height, 1000, "height")
        self.assertEqual(window.title, "Test Window Name", "title")
        self.assertEqual(pygame.display.get_caption()[0], "Test Window Name", "caption")
        
        self.assertTrue(window._window_flags & pygame.RESIZABLE, "resizable")
        
        self.assertEqual(window.clear_colour, [100, 0, 255], "clear colour")

        self.assertEqual(window._vsync, 0, "v-sync. WARNING, may fail if the display doesn't support v-sync.")

        self.assertIsNotNone(window.screen, "screen")

        del window
        pygame.quit()
    
    def test_validate_colour(self):
        """Test the Window 'validate_colour' static method."""

        self.assertEqual(Window.validate_colour([-50, 100, 400]), [0, 100, 255], "validate_colour - all negative")

    def test_clear(self):
        """Test the Window 'clear' method."""

        Debug._messages = []

        window = Window(100, 100, "Test Window", False, [255, 0, 0])

        window.clear()

        self.assertEqual(window.screen.get_at((50, 50)), pygame.Color(255, 0, 0))

        del window
        