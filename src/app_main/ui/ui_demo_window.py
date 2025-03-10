import pygame
import pygame_gui

class DemoWindow(pygame_gui.elements.UIWindow):
    """The test window for the UI system.
    
    Contains a button and a dropdown menu."""

    def __init__(self, ui_manager: pygame_gui.UIManager):
        super().__init__(pygame.Rect(20, 50, 220, 400), ui_manager, "Demo Window", resizable=True, visible=0)

        # Create the contents of the window
        self.demo_button = pygame_gui.elements.UIButton(
            pygame.Rect(10, 10, 200, 50), 
            "Press Me!", 
            self.ui_manager, 
            command = lambda : print("Pressed! 🌼"), 
            container = self, 
            anchors = {'left': 'left', 'right': 'right'},
            parent_element = self
        )
        self.drop_down_menu = pygame_gui.elements.UIDropDownMenu(
            ["Pick an Option", "Item 1", "Item 2", "Item 3", "Item 4"], 
            "Pick an Option", 
            pygame.Rect(10, 70, 200, 50), 
            self.ui_manager, 
            container = self, 
            parent_element = self,
            anchors = {'left': 'left', 'right': 'right'},
            expand_on_option_click = False
        )
    
    def on_close_window_button_pressed(self):
        """Override method to only hide the window when the close button is pressed."""

        super().hide()