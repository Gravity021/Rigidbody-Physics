import pygame
import pygame_gui
from pygame_gui.core.utility import get_default_manager

from ..physics.scene import Scene

from ..util.debug import Debug

class MenuBar(pygame_gui.elements.UIPanel):
    """Menu bar for the application.
    
    Stores and is responsible for the menu bar and its contents."""

    def __init__(self, ui_manager: pygame_gui.UIManager, window_width: int):
        super().__init__(
            (0, 0, window_width, 30),
            manager = ui_manager,
            margins = {"left": 0, "right": 0, "top": 0, "bottom": 0}, 
            anchors = {'left': 'left', 'right': 'right'}
        )

        # Extend the render-able area by 100px vertically to accommodate the dropdown menu
        container_dimensions = self.panel_container.get_rect()
        container_dimensions.height += 100
        self.panel_container.set_dimensions((container_dimensions.width, container_dimensions.height))

        # Create the menu bar elements
        self.file_button = pygame_gui.elements.UIButton(
            pygame.Rect(2, 2, 60, 26),
            "File",
            ui_manager,
            command = lambda : print("File"),
            parent_element = self,
            container = self,
            anchors = {"top": "top"}
        )
        self.windows_dropdown = pygame_gui.elements.UIDropDownMenu(
            ["Selected Object", "Add Object", "Settings", "Demo Window"],
            "Demo Window",
            pygame.Rect(0, 2, 225, 26),
            ui_manager,
            container = self,
            parent_element = self,
            anchors = {"left_target": self.file_button, "top": "top"},
            expand_on_option_click = False
        )
        self.fps_label = pygame_gui.elements.UILabel(
            pygame.Rect(-100, 2, 75, 26),
            "FPS: ",
            ui_manager,
            container = self,
            parent_element = self,
            anchors = {"right": "right", "top": "top"}
        )

        self.play_pause_button = pygame_gui.elements.UIButton(
            pygame.Rect(0, 2, 60, 26),
            "Play",
            ui_manager,
            command = self.play_pause_command,
            parent_element = self,
            container = self,
            anchors = {"centerx": "centerx", "top": "top"}
        )
        self.edit_button = pygame_gui.elements.UIButton(
            pygame.Rect(-120, 2, 60, 26),
            "Edit",
            ui_manager,
            command = self.edit_command,
            parent_element = self,
            container = self,
            anchors = {"top": "top", "left_target": self.play_pause_button}
        )
        self.step_button = pygame_gui.elements.UIButton(
            pygame.Rect(0, 2, 60, 26),
            "Step",
            ui_manager,
            command = self.step_command,
            parent_element = self,
            container = self,
            anchors = {"top": "top", "left_target": self.play_pause_button}
        )
        
        # Ensure that the dropdown button opens the correct window on pressed.
        self.ui_manager.register_event_fn(pygame_gui.UI_BUTTON_PRESSED, self.handle_dropdown)

        self._scene_ref: Scene = None
    
    def play_pause_command(self):
        if self._scene_ref is None:
            Debug.log_error("No scene reference!")
            return

        if self._scene_ref.state == Scene.SceneState.EDIT:
            self._scene_ref.change_state(Scene.SceneState.PLAY)

            self.play_pause_button.set_text("Pause")
            self.step_button.disable()
        elif self._scene_ref.state == Scene.SceneState.PLAY:
            self._scene_ref.change_state(Scene.SceneState.PAUSE)

            self.play_pause_button.set_text("Play")
            self.step_button.enable()
        elif self._scene_ref.state == Scene.SceneState.PAUSE:
            self._scene_ref.change_state(Scene.SceneState.PLAY)

            self.play_pause_button.set_text("Pause")
            self.step_button.disable()

    def edit_command(self):
        if self._scene_ref is None:
            Debug.log_error("No scene reference!")
            return

        self._scene_ref.change_state(Scene.SceneState.EDIT)
        self.play_pause_button.set_text("Play")
        self.step_button.enable()

    def step_command(self):
        if self._scene_ref is None:
            Debug.log_error("No scene reference!")
            return
        
        if self._scene_ref.state == Scene.SceneState.EDIT:
            self._scene_ref.change_state(Scene.SceneState.PAUSE)
        
        self._scene_ref.step(self._scene_ref.step_interval)
    
    def set_dimensions(self, dimensions, clamp_to_container: bool = False):
        """Override method to resize the menu bar.
        
        Extend the render-able area by 100px vertically to accommodate the dropdown menu."""

        super().set_dimensions(dimensions, clamp_to_container)
        container_dimensions = self.panel_container.get_rect()
        container_dimensions.height += 100
        self.panel_container.set_dimensions((container_dimensions.width, container_dimensions.height))

    def handle_dropdown(self, event: pygame.Event):
        """Open the required window when the dropdown button is pressed."""

        if event.ui_element == self.windows_dropdown.current_state.selected_option_button:
            if self.windows_dropdown.current_state.selected_option_button.text == "Demo Window":
                get_default_manager().test_window.show()
            elif self.windows_dropdown.current_state.selected_option_button.text == "Settings":
                get_default_manager().settings_window.show()
            elif self.windows_dropdown.current_state.selected_option_button.text == "Selected Object":
                get_default_manager().selected_object_window.show()
            elif self.windows_dropdown.current_state.selected_option_button.text == "Add Object":
                get_default_manager().add_object_window.show()

    def set_scene_ref(self, scene):
        self._scene_ref = scene