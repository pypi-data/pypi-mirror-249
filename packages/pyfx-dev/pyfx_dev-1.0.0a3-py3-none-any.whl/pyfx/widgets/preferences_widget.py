from PySide6.QtWidgets import QWidget

from pyfx.audio.audio_controller import PyFxAudioController
from pyfx.ui.preferences_widget_ui import Ui_PreferencesWidget


class PreferencesWidget(QWidget, Ui_PreferencesWidget):
    def __init__(self, audio_controller: PyFxAudioController):
        super().__init__()
        self.setupUi(self)
        self.audio_preferences.audio_controller = audio_controller
