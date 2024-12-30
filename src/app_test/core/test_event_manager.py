import unittest
from unittest import TestCase

from app_main.core.event_manager import *

class EventManagerTests(TestCase):
    """Test the EventManager class."""
    
    def test_init(self):
        """Test the EventManager constructor."""

        pygame.init()
        event_manager = EventManager()

        self.assertEqual(event_manager._event_map, {pygame.KEYDOWN: [], pygame.KEYUP: []}, "'_event_map' init")

        self.assertEqual(event_manager._mouse_pos, (-1, -1), "'_mouse_pos' init")

        self.assertEqual(event_manager._mouse_buttons, [False, False, False, False, False], "'_mouse_buttons' init")

        self.assertEqual(event_manager._should_close, False, "'_should_close' init")

    @unittest.skip
    def handle_space(self, event: pygame.Event):
        if event.key == pygame.K_SPACE: Debug.log("Space key pressed!")

    def test_handle_events(self):
        """Test the EventManager 'handle_events' method."""

        Debug._messages = []

        pygame.init()

        event_manager = EventManager()

        # Test Keydown with no listener
        pygame.event.post(pygame.event.Event(
            pygame.KEYDOWN,
            {"key": 27}
        ))
        event_manager.handle_events()
        
        log_found = False
        for message in Debug._messages: log_found |= message["message"] == "Unhandled event of type KeyDown"
        self.assertTrue(log_found, "keydown handled")
        
        Debug._messages = []

        # Test Keyup with no listener
        pygame.event.post(pygame.event.Event(
            pygame.KEYUP,
            {"key": 27}
        ))
        event_manager.handle_events()
        
        log_found = False
        for message in Debug._messages: log_found |= message["message"] == "Unhandled event of type KeyUp"
        self.assertTrue(log_found, "keyup handled")
        
        Debug._messages = []
        
        # Test Mousebuttondown
        pygame.event.post(pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {"button": 1}
        ))
        event_manager.handle_events()
        
        self.assertTrue(event_manager._mouse_buttons[0], "mousebuttondown handled")
        
        Debug._messages = []

        # Test Mousebuttonup
        pygame.event.post(pygame.event.Event(
            pygame.MOUSEBUTTONUP,
            {"button": 1}
        ))
        event_manager.handle_events()
        
        self.assertFalse(event_manager._mouse_buttons[0], "mousebuttonup handled")
        
        Debug._messages = []

        # Test quit event
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        event_manager.handle_events()
        
        self.assertTrue(event_manager._should_close)

        Debug._messages = []

        event_manager._event_map[pygame.KEYDOWN].append(self.handle_space)
        # Test Keydown with listener
        pygame.event.post(pygame.event.Event(
            pygame.KEYDOWN,
            {"key": 32}
        ))
        event_manager.handle_events()
        
        log_found = False
        for message in Debug._messages: log_found |= message["message"] == "Space key pressed down!"
        self.assertTrue(log_found, "custom keydown action handled")
        
    
    @unittest.skip
    def runnable(self):
        """An arbitrary method used in some tests"""
        print("Hello, World!")

    def test_register_action(self):
        """Test the EventManager 'register_action' method."""

        event_manager = EventManager()

        event_manager.register_action(pygame.KEYDOWN, self.runnable)

        self.assertEqual(event_manager._event_map, {768: [self.runnable], 769: []}, "event map")