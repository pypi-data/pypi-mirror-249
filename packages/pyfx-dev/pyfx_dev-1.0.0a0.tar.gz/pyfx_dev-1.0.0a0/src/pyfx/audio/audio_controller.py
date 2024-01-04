import threading
import time

import numpy as np
import pyaudio
from numpy.typing import DTypeLike

from pyfx.audio.audio_consumer import AudioConsumer, AudioConsumerType, InterfaceAudioConsumer
from pyfx.audio.audio_device import AudioDeviceInfo
from pyfx.audio.audio_driver import AudioDriverInfo
from pyfx.audio.audio_interface_info import AudioInterfaceInfo
from pyfx.audio.audio_processor import AudioProcessor
from pyfx.audio.audio_source import (
    AudioSource,
    AudioSourceType,
    FileAudioSource,
    InterfaceAudioSource,
    TestToneAudioSource,
)
from pyfx.logger import pyfx_log


class PyFxAudioController:
    def __init__(self):
        self.initialized = False
        self.pa = pyaudio.PyAudio()
        self.audio_interface_info = AudioInterfaceInfo(self.pa)
        self.thread = None
        self.running = False

        self._sample_rate_observers = []
        self._buffer_size_observers = []
        self._data_type_observers = []

        self.sample_rate = 44100
        self.sample_rates = [8000, 16000, 32000, 44100, 48000, 96000]
        self.buffer_size = 128
        self.buffer_sizes = [2**x for x in range(1, 13)]
        self.data_type = np.float32

        # Setup Test Tone Audio Source
        self.test_tone_audio_source = TestToneAudioSource()
        self.add_sample_rate_observer(self.test_tone_audio_source.set_sample_rate)
        self.add_buffer_size_observer(self.test_tone_audio_source.set_buffer_size)
        self.add_data_type_observer(self.test_tone_audio_source.set_data_type)

        # Setup File Audio Source
        self.file_audio_source = FileAudioSource()
        self.add_buffer_size_observer(self.file_audio_source.set_buffer_size)
        self.add_data_type_observer(self.file_audio_source.set_data_type)

        # Setup Interface Audio Source
        self.interface_audio_source = InterfaceAudioSource(self.pa)
        self.add_sample_rate_observer(self.interface_audio_source.set_sample_rate)
        self.add_buffer_size_observer(self.interface_audio_source.set_buffer_size)
        self.add_data_type_observer(self.interface_audio_source.set_data_type)

        # Setup Audio Processor
        self.audio_processor: AudioProcessor = None
        self.set_audio_processor(AudioProcessor(name="Default Audio Processor"))

        # Setup Interface Audio Consumer
        self.interface_audio_consumer = InterfaceAudioConsumer(self.pa)
        self.add_sample_rate_observer(self.interface_audio_consumer.set_sample_rate)
        self.add_buffer_size_observer(self.interface_audio_consumer.set_buffer_size)
        self.add_data_type_observer(self.interface_audio_consumer.set_data_type)

        # Audio Source Setup
        self.audio_sources: dict[AudioSourceType, AudioSource] = {
            AudioSourceType.FILE: self.file_audio_source,
            AudioSourceType.INTERFACE: self.interface_audio_source,
            AudioSourceType.TEST_TONE: self.test_tone_audio_source,
        }
        self.audio_source = self.file_audio_source

        # Audio Consumer Setup
        self.audio_consumers: dict[AudioConsumerType, AudioConsumer] = {
            AudioConsumerType.INTERFACE: self.interface_audio_consumer,
        }
        self.audio_consumer = self.interface_audio_consumer

        self.set_audio_driver(self.audio_drivers[0])
        self.set_audio_input_device(self.audio_input_devices[0])
        self.set_audio_output_device(self.audio_output_devices[0])

    def initialize(self):
        self.initialized = True
        self.start()

    def start(self):
        if self.initialized and not self.running:
            self.audio_consumer.start_stream()
            self.audio_source.start_stream()
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

    def _run(self):
        while self.running:
            data = self.audio_source.read()
            if data is not None:
                if self.audio_processor:
                    data = self.audio_processor.process_audio(data)
                self.audio_consumer.write(data)
            time.sleep(0.001)

    def stop(self):
        if self.running:
            self.running = False
            if self.thread:
                self.thread.join()
            self.audio_source.stop_stream()
            self.audio_consumer.stop_stream()

    def shutdown(self):
        self.stop()
        self.pa.terminate()

    @property
    def audio_drivers(self):
        return self.audio_interface_info.audio_drivers

    @property
    def audio_input_devices(self):
        return self.audio_interface_info.audio_input_devices

    @property
    def audio_output_devices(self):
        return self.audio_interface_info.audio_output_devices

    """Sample Rate"""

    def set_sample_rate(self, sample_rate: int):
        pyfx_log.debug(f"Setting sample rate to {sample_rate} Hz")
        self.sample_rate = sample_rate
        self.notify_sample_rate_observers(sample_rate)

    def add_sample_rate_observer(self, observer):
        observer(self.sample_rate)
        self._sample_rate_observers.append(observer)

    def remove_sample_rate_observer(self, observer):
        self._sample_rate_observers.remove(observer)

    def notify_sample_rate_observers(self, sample_rate: int):
        for observer in self._sample_rate_observers:
            observer(sample_rate)

    """Buffer Size"""

    def set_buffer_size(self, buffer_size: int):
        pyfx_log.debug(f"Setting buffer size to {buffer_size} samples")
        self.buffer_size = buffer_size
        self.notify_buffer_size_observers(buffer_size)

    def add_buffer_size_observer(self, observer):
        observer(self.buffer_size)
        self._buffer_size_observers.append(observer)

    def remove_buffer_size_observer(self, observer):
        self._buffer_size_observers.remove(observer)

    def notify_buffer_size_observers(self, buffer_size: int):
        for observer in self._buffer_size_observers:
            observer(buffer_size)

    """Data Type"""

    def set_data_type(self, data_type: DTypeLike):
        pyfx_log.debug(f"Setting data type to {data_type.__name__}")
        self.data_type = data_type
        self.notify_data_type_observers(data_type)

    def add_data_type_observer(self, observer):
        observer(self.data_type)
        self._data_type_observers.append(observer)

    def remove_data_type_observer(self, observer):
        self._data_type_observers.remove(observer)

    def notify_data_type_observers(self, data_type: int):
        for observer in self._data_type_observers:
            observer(data_type)

    """Audio Source Control"""

    def set_audio_source(self, audio_source_type: AudioSourceType):
        self.stop()
        audio_source = self.audio_sources[audio_source_type]
        pyfx_log.debug(f"Setting audio source to {audio_source.name}")
        self.audio_source = audio_source
        if "_prev_sample_rate" in dir(self):
            pyfx_log.debug(f"Restoring previous sample rate to {self._prev_sample_rate}")
            self.set_sample_rate(self._prev_sample_rate)
            del self._prev_sample_rate
        self.start()

    """Audio Consumer Control"""

    def set_audio_consumer(self, audio_consumer_type: AudioConsumerType):
        self.stop()
        audio_consumer = self.audio_consumers[audio_consumer_type]
        pyfx_log.debug(f"Setting audio consumer to {audio_consumer.name}")
        self.audio_consumer = audio_consumer
        self.start()

    """Test Tone Audio Source Control"""

    def play_test_tone(self) -> None:
        pyfx_log.debug("Playing test tone")
        self._prev_audio_source_type = self.audio_source.audio_source_type
        self.set_audio_source(AudioSourceType.TEST_TONE)

    def stop_test_tone(self) -> None:
        pyfx_log.debug("Stopping test tone")
        self.set_audio_source(self._prev_audio_source_type)
        del self._prev_audio_source_type

    def set_test_tone_frequency(self, frequency: int) -> None:
        self.test_tone_audio_source.set_frequency(frequency)

    def set_test_tone_volume_db(self, volume_db: int) -> None:
        self.test_tone_audio_source.set_volume_db(volume_db)

    def set_simulated_cpu_usage(self, simulated_cpu_usage: float) -> None:
        self.test_tone_audio_source.set_simulated_cpu_usage(simulated_cpu_usage)

    """File Audio Source Control"""

    def set_audio_file(self, audio_file: str):
        self.stop()
        self.file_audio_source.set_audio_file(audio_file)
        self._prev_sample_rate = self.sample_rate
        self.set_sample_rate(self.audio_source.sample_rate)
        self.start()

    def play_audio_file(self):
        self.file_audio_source.play()

    def stop_audio_file(self):
        self.file_audio_source.stop()

    def pause_audio_file(self):
        self.file_audio_source.pause()

    def set_audio_file_loop_state(self, state: bool):  # noqa: FBT001
        if state:
            self.file_audio_source.enable_looping()
        else:
            self.file_audio_source.disable_looping()

    """Interface Audio Source Control"""

    def start_interface_audio_source_streaming(self):
        pyfx_log.debug("Starting streaming from the interface audio source")

    def stop_interface_audio_source_streaming(self):
        pyfx_log.debug("Stop streaming from the interface audio source")

    """Audio Processor Control"""

    def set_audio_processor(self, audio_processor: AudioProcessor):
        pyfx_log.debug(f"Setting audio processor to {audio_processor.__class__.__name__}")
        if self.audio_processor is not None:
            self.remove_sample_rate_observer(self.audio_processor.set_sample_rate)
            self.remove_buffer_size_observer(self.audio_processor.set_buffer_size)
            self.remove_data_type_observer(self.audio_processor.set_data_type)
        self.audio_processor = audio_processor
        self.add_sample_rate_observer(self.audio_processor.set_sample_rate)
        self.add_buffer_size_observer(self.audio_processor.set_buffer_size)
        self.add_data_type_observer(self.audio_processor.set_data_type)

    """Interface Audio Consumer Control"""

    def start_interface_audio_consumer_streaming(self):
        pyfx_log.debug("Starting streaming from the interface audio consumer")

    def stop_interface_audio_consumer_streaming(self):
        pyfx_log.debug("Stop streaming from the interface audio consumer")

    """Interface Control"""

    def set_audio_driver(self, audio_driver: AudioDriverInfo):
        self.interface_audio_source.set_audio_driver(audio_driver)
        self.interface_audio_consumer.set_audio_driver(audio_driver)

    def set_audio_input_device(self, audio_input_device: AudioDeviceInfo):
        self.interface_audio_source.set_audio_input_device(audio_input_device)

    def set_audio_output_device(self, audio_output_device: AudioDeviceInfo):
        self.interface_audio_consumer.set_audio_output_device(audio_output_device)

    def set_audio_input_channels(self, channels: list[int]):
        self.interface_audio_source.set_channels(channels)

    def set_audio_output_channels(self, channels: list[int]):
        self.interface_audio_consumer.set_channels(channels)
