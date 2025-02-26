import pygame
import pygame_gui

from ..maths.Vector2 import Vector2

from .ui_colour_picker import UIColourPickerDialog

numerical_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '.']

# TODO: None of these pairs resize properly
    # Have the label fixed and the fields resize?

def create_float_field(ui_manager: pygame_gui.UIManager, window: pygame_gui.elements.UIWindow, label: str, initial_value: float, rect: pygame.Rect) -> tuple[pygame_gui.elements.UILabel, pygame_gui.elements.UITextEntryLine]:
    label = pygame_gui.elements.UILabel(
        pygame.Rect(rect.x, rect.y, rect.width // 2, rect.height),
        label,
        ui_manager,
        container=window,
        parent_element=window,
        anchors={"left": "left", "right": "right"}
        # anchors={"left": "left"}
    )
    entry = pygame_gui.elements.UITextEntryLine(
        pygame.Rect(rect.x + rect.width // 2, rect.y, rect.width // 2, rect.height),
        # pygame.Rect(-10 - rect.width // 2, rect.y, rect.width // 2, rect.height),
        # pygame.Rect(0, rect.y, rect.width // 2, rect.height),/
        ui_manager,
        initial_text=str(initial_value),
        container=window,
        parent_element=window,
        anchors={"left": "left", "right": "right"}
        # anchors={"left_target": label, "right": "right", "left": "left"}
        # anchors={"left_target": label}
    )
    entry.set_allowed_characters(numerical_characters)

    return label, entry

def create_vector2_field(ui_manager: pygame_gui.UIManager, window: pygame_gui.elements.UIWindow, label: str, initial_value: Vector2, rect: pygame.Rect) -> tuple[pygame_gui.elements.UILabel, pygame_gui.elements.UITextEntryLine, pygame_gui.elements.UITextEntryLine]:
    label = pygame_gui.elements.UILabel(
        pygame.Rect(rect.x, rect.y, rect.width // 2, rect.height),
        label,
        ui_manager,
        container=window,
        parent_element=window,
        anchors={"left": "left", "right": "right"}
    )
    entry_x = pygame_gui.elements.UITextEntryLine(
        pygame.Rect(rect.x + rect.width // 2, rect.y, rect.width // 4, rect.height),
        ui_manager,
        initial_text=str(initial_value.x),
        container=window,
        parent_element=window,
        anchors={"left": "left", "right": "right"}
    )
    entry_x.set_allowed_characters(numerical_characters)
    entry_y = pygame_gui.elements.UITextEntryLine(
        pygame.Rect(rect.x + 3 * rect.width // 4, rect.y, rect.width // 4, rect.height),
        ui_manager,
        initial_text=str(initial_value.y),
        container=window,
        parent_element=window,
        anchors={"left": "left", "right": "right"}
    )
    entry_y.set_allowed_characters(numerical_characters)

    return label, entry_x, entry_y

def create_dropdown_field(ui_manager: pygame_gui.UIManager, window: pygame_gui.elements.UIWindow, label: str, options: list[str], initial_value: str, rect: pygame.Rect) -> tuple[pygame_gui.elements.UILabel, pygame_gui.elements.UIDropDownMenu]:
    label = pygame_gui.elements.UILabel(
        pygame.Rect(rect.x, rect.y, rect.width // 2, rect.height),
        label,
        ui_manager,
        container=window,
        parent_element=window,
        anchors={"left": "left", "right": "right"}
    )
    dropdown = pygame_gui.elements.UIDropDownMenu(
        options,
        initial_value,
        pygame.Rect(rect.x + rect.width // 2, rect.y, rect.width // 2, rect.height),
        ui_manager,
        container=window,
        parent_element=window,
        anchors={"left": "left", "right": "right"}
    )

    return label, dropdown

def create_colour_field(ui_manager: pygame_gui.UIManager, window: pygame_gui.elements.UIWindow, label: str, initial_value: tuple[int, int, int, int], rect: pygame.Rect) -> tuple[pygame_gui.elements.UILabel, pygame.Surface, pygame_gui.elements.UIImage, pygame_gui.elements.UIButton, UIColourPickerDialog]:
    label = pygame_gui.elements.UILabel(
        pygame.Rect(rect.x, rect.y, rect.width // 2, rect.height),
        label,
        ui_manager,
        container=window,
        parent_element=window,
        anchors={"left": "left", "right": "right"}
    )
    surface = pygame.Surface((rect.width // 4, rect.height - 4))
    surface.fill(initial_value)
    image = None
    image = pygame_gui.elements.UIImage(
        pygame.Rect(rect.x + rect.width // 2, rect.y + 2, rect.width // 4, rect.height -4),
        surface,
        ui_manager,
        container=window,
        parent_element=window,
        anchors={"left": "left", "right": "right"}
    )

    picker_window = UIColourPickerDialog(
        pygame.Rect(10, 10, 300, 300),
        ui_manager,
        initial_colour=pygame.Color(initial_value),
    )
    picker_window.hide()

    button =  pygame_gui.elements.UIButton(
        pygame.Rect(rect.x + 3 * rect.width // 4, rect.y, rect.width // 4, rect.height),
        "Change",
        ui_manager,
        command=lambda : picker_window.show(),
        container=window,
        parent_element=window,
        anchors={"left": "left", "right": "right"}
    )

    return label, surface, image, button, picker_window