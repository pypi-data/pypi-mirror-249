import queue
from abc import ABC, abstractmethod
from enum import Enum
from types import MappingProxyType

import numpy as np
import pyaudio
from numpy.typing import DTypeLike

from pyfx.audio.audio_device import AudioDeviceInfo
from pyfx.audio.audio_driver import AudioDriverInfo
from pyfx.logger import pyfx_log


class AudioConsumerType(Enum):
    INTERFACE = 1


class AudioConsumer(ABC):
    def __init__(
        self,
        name: str,
        sample_rate: float | None = None,
        buffer_size: int | None = None,
        data_type: DTypeLike | None = None,
    ):
        self.name = name
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
        self.data_type = data_type

    @abstractmethod
    def write(self, data: np.ndarray) -> None:
        """Abstract Audio Consumer Write Method"""

    @property
    @abstractmethod
    def audio_consumer_type(self) -> AudioConsumerType:
        """Abstract Audio Consumer Type Property"""

    def set_sample_rate(self, sample_rate: float) -> None:
        pyfx_log.debug(f"Setting {self.name} sample rate to {sample_rate}")
        self.sample_rate = sample_rate
        self.sample_period = 1 / sample_rate

    def set_buffer_size(self, buffer_size: int) -> None:
        pyfx_log.debug(f"Setting {self.name} buffer size to {buffer_size}")
        self.buffer_size = buffer_size

    def set_data_type(self, data_type: DTypeLike) -> None:
        pyfx_log.debug(f"Setting {self.name} data type to {data_type.__name__}")
        self.data_type = data_type


class InterfaceAudioConsumer(AudioConsumer):
    audio_consumer_type = AudioConsumerType.INTERFACE

    data_type_to_pa_format_map = MappingProxyType(
        {
            np.int8: pyaudio.paInt8,
            np.int16: pyaudio.paInt16,
            np.int32: pyaudio.paInt32,
            np.float32: pyaudio.paFloat32,
        }
    )

    def __init__(self, pa: pyaudio.PyAudio, *args, **kwargs):
        super().__init__(*args, name="Interface Audio Consumer", **kwargs)
        self.pa = pa
        self.queue = queue.Queue(maxsize=20)
        self._stream: pyaudio.Stream = None
        self.audio_driver: AudioDriverInfo = None
        self.audio_output_device: AudioDeviceInfo = None
        self.channels: list[int] = []

    def reset_queue(self):
        self.queue = queue.Queue(maxsize=20)

    def set_audio_driver(self, audio_driver: AudioDriverInfo):
        self.audio_driver = audio_driver
        if audio_driver is not None:
            pyfx_log.debug(f"Setting {self.name} audio driver to {audio_driver.driver_name}")

    def set_audio_output_device(self, audio_output_device: AudioDeviceInfo):
        self.audio_output_device = audio_output_device
        if audio_output_device is not None:
            pyfx_log.debug(f"Setting audio output device to {audio_output_device.name}")
            self.num_output_channels = audio_output_device.max_output_channels

    def set_audio_output_channels(self, channels: list[int]):
        pyfx_log.debug(f"Setting {self.name} channels to {channels}")
        self.channels = channels

    def write(self, data: np.ndarray):
        if data is not None:
            self.queue.put(data)

    def audio_consumer_callback(self, in_data: bytes, frame_count: int, time_info: dict, status: int):  # noqa: ARG002
        try:
            audio_data = self.queue.get_nowait()
        except queue.Empty:
            audio_data = np.zeros((self.num_output_channels, frame_count), dtype=self.data_type)

        num_audio_input_channels = audio_data.shape[0]
        audio_output = np.zeros((self.num_output_channels, frame_count), self.data_type)
        for audio_data_idx, channel in enumerate(self.channels):
            audio_output[channel] = audio_data[audio_data_idx % num_audio_input_channels]

        interleaved_audio = audio_output.T.flatten()
        return (interleaved_audio.tobytes(), pyaudio.paContinue)

    def start_stream(self):
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()

        pyfx_log.debug(f"Starting {self.name} stream")
        self._stream = self.pa.open(
            format=self.data_type_to_pa_format_map[self.data_type],
            channels=self.audio_output_device.max_output_channels,
            rate=self.sample_rate,
            input=False,
            output=True,
            output_device_index=self.audio_output_device.index,
            frames_per_buffer=self.buffer_size,
            output_host_api_specific_stream_info=self.audio_driver.host_api_id,
            stream_callback=self.audio_consumer_callback,
        )

        self._stream.start_stream()

    def stop_stream(self):
        if self._stream is not None:
            pyfx_log.debug(f"Stopping {self.name} stream")
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None
            self.reset_queue()
