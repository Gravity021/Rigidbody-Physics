from unittest import TestCase

import pygame
from pygame import Color

import time

from app_main.core.window import Window

from app_main.maths.Vector2 import Vector2

from app_main.physics.scene import Scene
from app_main.physics.object import Object

class SceneTests(TestCase):
    
    @classmethod
    def setUpClass(self):
        pygame.init()
        
        # Set up some objects for rendering
        self.window = Window(400, 400, "Scene Tests Window", False, clear_colour=[125, 125, 125])
        self.scene = Scene()
        
    def test_render_1(self):
        """Test 1 - Circle with centre (16, 16) and radius 8"""

        self.scene.objects.append(Object(Object.ObjectType.CIRCLE, Vector2(1, 25 - 1), Vector2(0.5, -1), 1))

        self.window.clear()
        self.scene.render(self.window.screen)
        self.window.update()

        self.assertEqual(self.window.screen.get_at((16, 16)), Color([255, 255, 255, 255]))   # Test the centre is in the correct place

        self.assertEqual(self.window.screen.get_at((16,  8)), Color([255, 255, 255, 255]))   # Test the top edge is in the correct place
        self.assertEqual(self.window.screen.get_at((16, 23)), Color([255, 255, 255, 255]))   # Test the bottom edge is in the correct place
        self.assertEqual(self.window.screen.get_at((8,  16)), Color([255, 255, 255, 255]))   # Test the left edge is in the correct place
        self.assertEqual(self.window.screen.get_at((23, 16)), Color([255, 255, 255, 255]))   # Test the right edge is in the correct place

    def test_render_2(self):
        """Test 2 - Circle with centre (48, 32) and radius 16"""

        self.scene.objects = [Object(Object.ObjectType.CIRCLE, Vector2(3, 25 - 2), Vector2(1, -1), 1, colour=[255, 0, 255])]

        self.window.clear()
        self.scene.render(self.window.screen)
        self.window.update()

        self.assertEqual(self.window.screen.get_at((48, 32)), Color([255, 0, 255, 255]))     # Test the centre is in the correct place

        self.assertEqual(self.window.screen.get_at((48, 47)), Color([255, 0, 255, 255]))     # Test the top edge is in the correct place
        self.assertEqual(self.window.screen.get_at((48, 16)), Color([255, 0, 255, 255]))     # Test the bottom edge is in the correct place
        self.assertEqual(self.window.screen.get_at((32, 32)), Color([255, 0, 255, 255]))     # Test the left edge is in the correct place
        self.assertEqual(self.window.screen.get_at((63, 32)), Color([255, 0, 255, 255]))     # Test the right edge is in the correct place

    def test_render_3(self):
        """Test 3 - Rectangle with centre (160, 160) and dimensions (48, 16)"""
        
        self.scene.objects = [Object(Object.ObjectType.RECTANGLE, Vector2(10, 25 - 10), Vector2(3, 1), 1, colour=[255, 0, 0])]
        
        self.window.clear()
        self.scene.render(self.window.screen)
        self.window.update()

        self.assertEqual(self.window.screen.get_at((160, 160)), Color([255, 0, 0, 255]))     # Test the centre is in the correct place

        self.assertEqual(self.window.screen.get_at((136, 152)), Color([255, 0, 0, 255]))     # Test the top left corner is in the correct place
        self.assertEqual(self.window.screen.get_at((136, 167)), Color([255, 0, 0, 255]))     # Test the top right corner is in the correct place
        self.assertEqual(self.window.screen.get_at((183, 152)), Color([255, 0, 0, 255]))     # Test the bottom left corner is in the correct place
        self.assertEqual(self.window.screen.get_at((183, 167)), Color([255, 0, 0, 255]))     # Test the bottom right corner is in the correct place

    def test_render_4(self):
        """Test 4 - Rectangle with centre (80, 32) and dimensions (32, 16)"""

        self.scene.objects = [Object(Object.ObjectType.RECTANGLE, Vector2(5, 25 - 2), Vector2(2, 1), 1)]
        
        self.window.clear()
        self.scene.render(self.window.screen)
        self.window.update()

        self.assertEqual(self.window.screen.get_at((80, 32)), Color([255, 255, 255, 255]))   # Test the centre is in the correct place

        self.assertEqual(self.window.screen.get_at((64, 24)), Color([255, 255, 255, 255]))   # Test the top left corner is in the correct place
        self.assertEqual(self.window.screen.get_at((64, 39)), Color([255, 255, 255, 255]))   # Test the top right corner is in the correct place
        self.assertEqual(self.window.screen.get_at((95, 24)), Color([255, 255, 255, 255]))   # Test the bottom left corner is in the correct place
        self.assertEqual(self.window.screen.get_at((95, 39)), Color([255, 255, 255, 255]))   # Test the bottom right corner is in the correct place
    
    @classmethod
    def tearDownClass(self):
        pygame.quit()
        del self.window
        del self.scene
