import os
from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog, QWidget

from pyfx.audio.audio_controller import PyFxAudioController
from pyfx.audio.audio_source import AudioSourceType
from pyfx.logger import pyfx_log
from pyfx.ui.audio_preferences_widget_ui import Ui_AudioPreferencesWidget
from pyfx.widgets.channel_configuration_widget import ChannelConfigurationWidget


class AudioPreferencesWidget(QWidget, Ui_AudioPreferencesWidget):
    default_audio_folder = Path(os.environ.get("AUDIO_ASSETS_FOLDER")).resolve().as_posix()
    file_mode_set = Signal()
    interface_mode_set = Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._audio_controller: PyFxAudioController = None
        self.input_channel_configuration: ChannelConfigurationWidget = None
        self.output_channel_configuration: ChannelConfigurationWidget = None

    @property
    def audio_controller(self):
        return self._audio_controller

    @audio_controller.setter
    def audio_controller(self, audio_controller: PyFxAudioController):
        self._audio_controller = audio_controller
        self.setup_audio_preferences()

    def setup_audio_preferences(self):
        for audio_driver_info in self.audio_controller.audio_drivers:
            self.driver_type_combobox.addItem(audio_driver_info.driver_name, audio_driver_info)

        self.audio_input_device_combobox.addItem("Audio File", None)
        for audio_input_device in self.audio_controller.audio_input_devices:
            self.audio_input_device_combobox.addItem(audio_input_device.name, audio_input_device)

        for audio_output_device in self.audio_controller.audio_output_devices:
            self.audio_output_device_combobox.addItem(audio_output_device.name, audio_output_device)

        self.audio_folder_editbox.setText(self.default_audio_folder)

        default_buffer_size = self.audio_controller.buffer_size
        for buffer_size in self.audio_controller.buffer_sizes:
            self.buffer_size_combobox.addItem(f"{buffer_size} Samples", buffer_size)
        self.buffer_size_combobox.setCurrentText(f"{default_buffer_size} Samples")

        default_sample_rate = self.audio_controller.sample_rate
        for sample_rate in self.audio_controller.sample_rates:
            self.sample_rate_combobox.addItem(f"{sample_rate} Hz", sample_rate)
        self.sample_rate_combobox.setCurrentText(f"{default_sample_rate} Hz")

        self.tone_volume_spinbox.setValue(self.audio_controller.test_tone_audio_source.volume_db)
        self.tone_frequency_spinbox.setValue(self.audio_controller.test_tone_audio_source.frequency)
        self.simulated_cpu_usage_slider.setValue(
            int(self.audio_controller.test_tone_audio_source.simulated_cpu_usage * 100)
        )

    def driver_type_changed(self, audio_driver_name: str):
        self.audio_controller.stop()
        pyfx_log.debug(f"Driver type changed to {audio_driver_name}")
        audio_driver = self.driver_type_combobox.currentData()
        self.audio_controller.set_audio_driver(audio_driver)
        self.audio_controller.start()

    def audio_input_device_changed(self, audio_input_device_name: str):
        self.audio_controller.stop()
        pyfx_log.debug(f"Audio input device changed to {audio_input_device_name}")
        audio_input_device = self.audio_input_device_combobox.currentData()

        self.audio_controller.set_audio_input_device(audio_input_device)
        if audio_input_device is None:
            self.file_mode_set.emit()
            self.audio_controller.set_audio_source(AudioSourceType.FILE)
            self.input_config_button.setEnabled(False)
        else:
            self.interface_mode_set.emit()
            self.audio_controller.set_audio_source(AudioSourceType.INTERFACE)
            self.input_config_button.setEnabled(True)
            self.input_channel_configuration = ChannelConfigurationWidget(audio_input_device)
            self.input_channel_configuration.channel_config_changed.connect(
                self.audio_controller.interface_audio_source.set_audio_input_channels
            )
            self.input_channel_configuration.set_initial_channels()
        self.audio_controller.start()

    def audio_output_device_changed(self, audio_output_device_name: str):
        self.audio_controller.stop()
        pyfx_log.debug(f"Audio output device changed to {audio_output_device_name}")
        audio_output_device = self.audio_output_device_combobox.currentData()
        self.output_channel_configuration = ChannelConfigurationWidget(audio_output_device)
        self.output_channel_configuration.channel_config_changed.connect(
            self.audio_controller.interface_audio_consumer.set_audio_output_channels
        )
        self.output_channel_configuration.set_initial_channels()
        self.audio_controller.set_audio_output_device(audio_output_device)
        self.audio_controller.start()

    def input_config_button_pressed(self):
        pyfx_log.debug("Input config button pressed")
        audio_input_device = self.audio_input_device_combobox.currentData()
        if audio_input_device is not None:
            self.input_channel_configuration.show()

    def output_config_button_pressed(self):
        pyfx_log.debug("Output config button pressed")
        audio_output_device = self.audio_output_device_combobox.currentData()
        if audio_output_device is not None:
            self.output_channel_configuration.show()

    def audio_folder_browse_button_pressed(self):
        initial_folder = self.audio_folder_editbox.text()
        folder_path = QFileDialog.getExistingDirectory(self, "Select Audio Folder", initial_folder)
        if folder_path:
            self.audio_folder_editbox.setText(folder_path)

    def audio_folder_editing_finished(self):
        audio_folder = Path(self.audio_folder_editbox.text())
        if audio_folder.exists() and audio_folder.is_dir():
            pyfx_log.debug(f"Updating audio folder to {audio_folder.as_posix()}")
            self.audio_folder_editbox.setStyleSheet("QLineEdit { background-color: #FFFFFF; }")
        else:
            pyfx_log.debug(f"{audio_folder.as_posix()} is not a valid folder")
            self.audio_folder_editbox.setStyleSheet("QLineEdit { background-color: #FF8888; }")

    def sample_rate_changed(self, sample_rate: int):
        self.audio_controller.stop()
        pyfx_log.debug(f"Sample rate changed to {sample_rate}")
        sample_rate_data = self.sample_rate_combobox.currentData()
        self.audio_controller.set_sample_rate(sample_rate_data)
        self.audio_controller.start()

    def buffer_size_changed(self, buffer_size_combobox_index: int):
        self.audio_controller.stop()
        buffer_size = self.buffer_size_combobox.itemData(buffer_size_combobox_index)
        pyfx_log.debug(f"Buffer size changed to {buffer_size}")
        self.audio_controller.set_buffer_size(buffer_size)
        self.audio_controller.start()

    def test_tone_button_toggled(self, state):
        pyfx_log.debug(f"Test tone turned {'on' if state else 'off'}")
        if state:
            self.test_tone_button.setText("On")
            self.audio_controller.play_test_tone()
        else:
            self.test_tone_button.setText("Off")
            self.audio_controller.stop_test_tone()

    def test_tone_volume_changed(self, volume_db: int):
        pyfx_log.debug(f"Test tone volume changed to {volume_db} dB")
        self.audio_controller.set_test_tone_volume_db(volume_db)

    def test_tone_frequency_changed(self, frequency: int):
        pyfx_log.debug(f"Test tone frequency changed to {frequency} dB")
        self.audio_controller.set_test_tone_frequency(frequency)

    def simulated_cpu_usage_changed(self, simulated_cpu_usage: int):
        pyfx_log.debug(f"Simulated CPU usage changed to {simulated_cpu_usage}")
        self.audio_controller.set_simulated_cpu_usage(simulated_cpu_usage * 0.01)
        self.simulated_cpu_usage_editbox.setText(f"{simulated_cpu_usage} %")
