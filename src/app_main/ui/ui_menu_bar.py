import pygame
import pygame_gui
from pygame_gui.core.utility import get_default_manager

class MenuBar(pygame_gui.elements.UIPanel):
    def __init__(self, ui_manager: pygame_gui.UIManager, window_width: int):
        super().__init__(
            (0, 0, window_width, 30),
            manager = ui_manager, 
            margins = {"left": 0, "right": 0, "top": 0, "bottom": 0}, 
            anchors = {'left': 'left', 'right': 'right'}
        )

        panel_dimensions = self.panel_container.get_rect()
        panel_dimensions.height += 100
        self.panel_container.set_dimensions((panel_dimensions.width, panel_dimensions.height))

        self.file_button = pygame_gui.elements.UIButton(
            pygame.Rect(2, 2, 60, 26),
            "File",
            ui_manager,
            command = lambda : print("File"),
            parent_element = self,
            container = self,
            anchors = {"top": "top", "bottom": "bottom"}
        )
        self.windows_dropdown = pygame_gui.elements.UIDropDownMenu(
            ["Selected Object", "Add Object", "Settings", "Demo Window"],
            "Demo Window",
            pygame.Rect(0, 2, 225, 26),
            ui_manager,
            container = self,
            parent_element = self,
            anchors = {"left_target": self.file_button, "top": "top", "bottom": "bottom"},
            expand_on_option_click = False
        )
        self.fps_label = pygame_gui.elements.UILabel(
            pygame.Rect(-100, 2, 75, 26),
            "FPS: ",
            ui_manager,
            container = self,
            parent_element = self,
            anchors = {"right": "right", "top": "top", "bottom": "bottom"}
        )
        
        self.ui_manager.register_event_fn(pygame_gui.UI_BUTTON_PRESSED, self.handle_dropdown)
    
    def handle_dropdown(self, event: pygame.Event):
        if event.ui_element == self.windows_dropdown.current_state.selected_option_button:
            if self.windows_dropdown.current_state.selected_option_button.text == "Demo Window":
                get_default_manager().test_window.show()
            elif self.windows_dropdown.current_state.selected_option_button.text == "Settings":
                get_default_manager().settings_window.show()
            elif self.windows_dropdown.current_state.selected_option_button.text == "Selected Object":
                get_default_manager().selected_object_window.show()
            elif self.windows_dropdown.current_state.selected_option_button.text == "Add Object":
                get_default_manager().add_object_window.show()