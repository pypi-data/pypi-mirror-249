from functools import partial

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QGridLayout, QLabel, QPushButton, QWidget

from pyfx.audio.audio_device import AudioDeviceInfo
from pyfx.logger import pyfx_log
from pyfx.ui.channel_configuration_widget_ui import Ui_ChannelConfigurationWidget


class ChannelConfigurationButton(QPushButton):
    def __init__(self, channels: list[int]):
        super().__init__()
        self.channels = channels
        button_text = ", ".join([str(channel + 1) for channel in channels])
        self.setText(button_text)
        self.setFixedWidth(100)
        self.setCheckable(True)
        self.setContentsMargins(0, 0, 0, 0)


class ChannelConfigurationWidget(QWidget, Ui_ChannelConfigurationWidget):
    channel_config_changed = Signal(object)

    def __init__(self, audio_device: AudioDeviceInfo):
        super().__init__()
        self.setupUi(self)
        self.audio_device = audio_device
        self.input_button_widgets: list[ChannelConfigurationButton] = []
        self.output_button_widgets: list[ChannelConfigurationButton] = []
        num_inputs = audio_device.max_input_channels
        num_outputs = audio_device.max_output_channels

        if num_inputs == 0:
            self.input_channel_configuration_label.hide()
        else:
            self._populate_channel_config_layout(
                self.input_channel_configuration_layout,
                num_inputs,
                self.input_button_widgets,
                "input",
            )

        if num_outputs == 0:
            self.output_channel_configuration_label.hide()
        else:
            self._populate_channel_config_layout(
                self.output_channel_configuration_layout,
                num_outputs,
                self.output_button_widgets,
                "output",
            )

    def set_initial_channels(self):
        if self.input_button_widgets:
            self.input_button_widgets[0].click()

        if self.output_button_widgets:
            self.output_button_widgets[0].click()

    def update_audio_device(self, audio_device: AudioDeviceInfo):
        self.__init__(audio_device)

    def _populate_channel_config_layout(
        self,
        channel_config_layout: QGridLayout,
        num_channels: int,
        buttton_list: list[ChannelConfigurationButton],
        channel_type: str,
    ):
        mono_channel_label = QLabel("Mono Channels")
        mono_channel_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        stereo_channel_label = QLabel("Stereo Channels")
        stereo_channel_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Setup stereo channel layout
        channel_config_layout.addWidget(stereo_channel_label, 0, 1)
        for row, channel in enumerate(range(0, num_channels, 2), start=1):
            channels = [channel, channel + 1]
            channel_config_button = ChannelConfigurationButton(channels)
            channel_config_button.pressed.connect(partial(self.channel_config_button_pressed, channel_type, channels))
            buttton_list.append(channel_config_button)
            channel_config_layout.addWidget(channel_config_button, row, 1)

        # Setup mono channel layout
        channel_config_layout.addWidget(mono_channel_label, 0, 0)
        for row, channel in enumerate(range(num_channels), start=1):
            channels = [channel]
            channel_config_button = ChannelConfigurationButton(channels)
            channel_config_button.pressed.connect(partial(self.channel_config_button_pressed, channel_type, channels))
            buttton_list.append(channel_config_button)
            channel_config_layout.addWidget(channel_config_button, row, 0)

    def channel_config_button_pressed(self, channel_type: str, channels: list[int]):
        pyfx_log.debug(f"Channel configuration button pressed - {channel_type} channels: {channels}")
        self.channel_config_changed.emit(channels)

        if channel_type == "input":
            button_widget_list = self.input_button_widgets
        else:  # output
            button_widget_list = self.output_button_widgets

        # Disable all buttons except the one that was pressed
        for button_widget in button_widget_list:
            if button_widget.channels != channels:
                button_widget.setChecked(False)
