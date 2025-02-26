import pygame
import pygame_gui
from pygame_gui._constants import OldType

class UIColourPickerDialog(pygame_gui.windows.UIColourPickerDialog):

    def process_event(self, event: pygame.event.Event) -> bool:
        """
        Handles events that this UI element is interested in. In this case we are responding to
        the colour channel elements being changed, the OK or Cancel buttons being pressed or the
        user clicking the mouse inside the Saturation & Value picking square.

        :param event: The pygame Event to process.

        :return: True if event is consumed by this element and should not be passed on to other
                 elements.

        """

        # Copied from https://github.com/MyreMylar/pygame_gui/blob/main/pygame_gui/windows/ui_colour_picker_dialog.py#L538 with some slight alterations
        
        # consumed_event = super().process_event(event)
        consumed_event = super(pygame_gui.elements.UIWindow, self).process_event(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.cancel_button:
            # self.kill()
            self.hide()

        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.ok_button:
            # old event - to be removed in 0.8.0
            event_data = {'user_type': OldType(pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED),
                          'colour': self.current_colour,
                          'ui_element': self,
                          'ui_object_id': self.most_specific_combined_id}
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, event_data))
            # new event
            event_data = {'colour': self.current_colour,
                          'ui_element': self,
                          'ui_object_id': self.most_specific_combined_id}
            pygame.event.post(pygame.event.Event(pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED, event_data))
            # self.kill()
            self.hide()

        if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_CHANNEL_CHANGED:
            if event.ui_element in [self.hue_channel, self.sat_channel, self.value_channel]:
                self.current_colour.hsva = (self.hue_channel.current_value,
                                            self.sat_channel.current_value,
                                            self.value_channel.current_value,
                                            100)
                self.changed_hsv_update_rgb()
            elif event.ui_element in [self.red_channel, self.green_channel, self.blue_channel]:
                self.current_colour[event.channel_index] = event.value
                self.changed_rgb_update_hsv()

            self.update_current_colour_image()
            self.update_saturation_value_square()

            # Update 2D slider values
            self.update_colour_2d_slider()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            scaled_mouse_pos = self.ui_manager.calculate_scaled_mouse_position(event.pos)
            rect = self.sat_value_square.rect
            extended_rect = pygame.Rect(rect.x, rect.y, rect.w + 1, rect.h + 1)
            if extended_rect.collidepoint(scaled_mouse_pos):
                relative_click_pos = [scaled_mouse_pos[0] - self.sat_value_square.rect.left,
                                      scaled_mouse_pos[1] - self.sat_value_square.rect.top]
                # put in range 0 - 100 and reverse y
                x_value = int((relative_click_pos[0] / self.sat_value_square.rect.width) * 100)
                y_value = int((relative_click_pos[1] / self.sat_value_square.rect.height) * 100)
                value = min(100, max(0, x_value))
                saturation = min(100, max(0, 100 - y_value))

                self.sat_channel.set_value(saturation)
                self.value_channel.set_value(value)
                self.current_colour.hsva = (self.hue_channel.current_value,
                                            self.sat_channel.current_value,
                                            self.value_channel.current_value,
                                            100)
                self.changed_hsv_update_rgb()
                self.update_current_colour_image()

                # Update 2D slider values
                self.update_colour_2d_slider()

        if event.type == pygame_gui.UI_2D_SLIDER_MOVED and event.ui_element == self.colour_2d_slider:
            v, s = self.colour_2d_slider.get_current_value()
            self.sat_channel.set_value(s)
            self.value_channel.set_value(v)
            self.current_colour.hsva = (self.hue_channel.current_value,
                                        self.sat_channel.current_value,
                                        self.value_channel.current_value,
                                        100)
            self.changed_hsv_update_rgb()
            self.update_current_colour_image()

        return consumed_event