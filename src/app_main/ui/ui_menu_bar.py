import os
import pygame
import pygame_gui
from pygame_gui.core.utility import get_default_manager

from app_main.serialization import serializer

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
        self.new_button = pygame_gui.elements.UIButton(
            pygame.Rect(2, 2, 50, 26),
            "New",
            ui_manager,
            command = self.new_command,
            parent_element = self,
            container = self,
            anchors = {"top": "top"}
        )
        self.save_button = pygame_gui.elements.UIButton(
            pygame.Rect(0, 2, 50, 26),
            "Save",
            ui_manager,
            command = self.save_command,
            parent_element = self,
            container = self,
            anchors = {"top": "top", "left_target": self.new_button}
        )
        self.load_button = pygame_gui.elements.UIButton(
            pygame.Rect(0, 2, 50, 26),
            "Load",
            ui_manager,
            command = self.load_command,
            parent_element = self,
            container = self,
            anchors = {"top": "top", "left_target": self.save_button}
        )
        self.windows_dropdown = pygame_gui.elements.UIDropDownMenu(
            ["Selected Object", "Add Object", "Settings", "Demo Window"],
            "Demo Window",
            pygame.Rect(0, 2, 150, 26),
            ui_manager,
            container = self,
            parent_element = self,
            anchors = {"left_target": self.load_button, "top": "top"},
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

    def new_command(self):
        serializer.deserialize("default.simdata", self._scene_ref)
        self._scene_ref.file_path = None
    
    def load_command(self):
        pygame_gui.windows.UIFileDialog(
            pygame.Rect(20, 20, 600, 400),
            None,
            window_title = "Load Simulation",
            initial_file_path=".",
            allow_existing_files_only=True,
        )
    
    def _load_simulation(self, event):
        if event.ui_element.window_display_title != "Load Simulation":
            return
        
        path = event.text

        if not os.path.exists(path) or path.split(".")[-1] != "simdata":
            Debug.log_error(f"Invalid file path selected: {path}")
            return

        serializer.deserialize(path, self._scene_ref)
        self._scene_ref.file_path = path
    
    def save_command(self):
        if not self._scene_ref.file_path is None:
            if not os.path.exists(self._scene_ref.file_path):
                if not (os.path.exists("\\".join(self._scene_ref.file_path.split("\\")[:-1])) and self._scene_ref.file_path.split(".")[-1] == "simdata"):
                    Debug.log_error(f"Invalid file path selected: {self._scene_ref.file_path}")
                    return
        
            serializer.serialize(self._scene_ref.file_path, self._scene_ref.objects, self._scene_ref.step_interval)
            return

        pygame_gui.windows.UIFileDialog(
            pygame.Rect(20, 20, 600, 400),
            None,
            window_title = "Save Simulation",
            initial_file_path="."
        )

    def _save_simulation(self, event):
        if event.ui_element.window_display_title != "Save Simulation":
            return
        
        path = event.text

        if not os.path.exists(path):
            if not (os.path.exists("\\".join(path.split("\\")[:-1])) and path.split(".")[-1] == "simdata"):
                Debug.log_error(f"Invalid file path selected: {path}")
                return
        
        serializer.serialize(path, self._scene_ref.objects, self._scene_ref.step_interval)
        self._scene_ref.file_path = path

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