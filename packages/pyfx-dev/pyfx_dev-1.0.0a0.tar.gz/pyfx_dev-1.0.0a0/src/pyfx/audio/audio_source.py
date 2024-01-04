import queue
import time
import wave
from abc import ABC, abstractmethod
from enum import Enum
from types import MappingProxyType

import numpy as np
import pyaudio
from numpy.typing import DTypeLike

from pyfx.audio.audio_data_converter import AudioDataConverter
from pyfx.audio.audio_device import AudioDeviceInfo
from pyfx.audio.audio_driver import AudioDriverInfo
from pyfx.logger import pyfx_log


class AudioSourceType(Enum):
    FILE = 1
    INTERFACE = 2
    TEST_TONE = 3


class AudioSource(ABC):
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
        self.data_type: DTypeLike = data_type
        self.streaming = False

    @abstractmethod
    def read(self) -> np.ndarray:
        """Abstract Audio Source Read Method"""

    @property
    @abstractmethod
    def audio_source_type(self) -> AudioSourceType:
        """Abstract Audio Source Type Property"""

    def start_stream(self) -> None:
        """Audio Source Start Stream Method"""
        pyfx_log.debug(f"Starting {self.name} stream")
        self.streaming = True

    def stop_stream(self) -> None:
        """Audio Source Stop Stream Method"""
        pyfx_log.debug(f"Stopping {self.name} stream")
        self.streaming = False

    def set_sample_rate(self, sample_rate: float):
        pyfx_log.debug(f"Setting {self.name} sample rate to {sample_rate}")
        self.sample_rate = sample_rate
        self.sample_period = 1 / sample_rate

    def set_buffer_size(self, buffer_size: int):
        pyfx_log.debug(f"Setting {self.name} buffer size to {buffer_size}")
        self.buffer_size = buffer_size

    def set_data_type(self, data_type: DTypeLike):
        pyfx_log.debug(f"Setting {self.name} data type to {data_type.__name__}")
        self.data_type = data_type


class FileAudioSource(AudioSource):
    audio_source_type = AudioSourceType.FILE

    def __init__(self):
        super().__init__("File Audio Source")
        self.audio_file = None
        self._frame_index = 0
        self._playing = False
        self._looping = False
        self._streaming = False

    def set_audio_file(self, audio_file: str):
        pyfx_log.debug(f"Setting the audio file to {audio_file}")
        with wave.open(audio_file, "rb") as wf:
            params = wf.getparams()
            raw_frames = wf.readframes(params.nframes)

        self.audio_file = audio_file
        self.num_channels = params.nchannels
        self.sample_width = params.sampwidth
        self.sample_rate = params.framerate
        self.num_frames = params.nframes
        self.compression_type = params.comptype
        self.compression_name = params.compname
        if self.sample_width == 4:  # noqa: PLR2004
            interleaved_audio_data = np.frombuffer(raw_frames, np.int32)
        elif self.sample_width == 2:  # noqa: PLR2004
            interleaved_audio_data = np.frombuffer(raw_frames, np.int16)
        elif self.sample_width == 1:
            interleaved_audio_data = np.frombuffer(raw_frames, np.int8)
        elif self.sample_width == 3:  # noqa: PLR2004
            msg = "24 bit audio not supported. TODO: Add support for this"
            raise ValueError(msg)
        else:
            msg = f"Unsupported sample width of {self.sample_width}."
            raise ValueError(msg)
        self.data_type = np.float32
        audio_channels = interleaved_audio_data.reshape(self.num_frames, self.num_channels).T
        self.frames = AudioDataConverter.convert(audio_channels, self.data_type)

        self._frame_index = 0

    def read(self):
        if not self.streaming or not self._playing:
            return None

        start_idx = self._frame_index
        stop_idx = start_idx + self.buffer_size
        audio_frames = self.frames[:, start_idx:stop_idx]
        self._frame_index = stop_idx % self.num_frames
        # If we have played through all the frames
        if stop_idx >= self.num_frames:
            # If we are looping, start appending frames from the beginning
            if self._looping:
                audio_frames = np.hstack([audio_frames, self.frames[:, : stop_idx % self.num_frames]])
            # If we are not looping, append zeros and complete the stream
            else:
                zeroed_audio_frames = np.zeros((self.num_channels, stop_idx % self.num_frames), dtype=self.data_type)
                audio_frames = np.hstack([audio_frames, zeroed_audio_frames])
                self._frame_index = 0
                self._playing = False
        return audio_frames.copy()

    def set_sample_rate(self, sample_rate: float):  # noqa: ARG002
        msg = "You cannot set the sample rate of a FileAudioSource"
        raise RuntimeError(msg)

    def play(self):
        if self.audio_file is not None:
            pyfx_log.debug(f"Playing {self.audio_file}")
            self._playing = True

    def pause(self):
        if self.audio_file is not None:
            pyfx_log.debug(f"Paused {self.audio_file}")
            self._playing = False

    def stop(self):
        if self.audio_file is not None:
            pyfx_log.debug(f"Stopped playing {self.audio_file}")
            self._frame_index = 0
            self._playing = False

    def enable_looping(self):
        if self.audio_file is not None:
            pyfx_log.debug(f"Enable looping of {self.audio_file}")
            self._looping = True

    def disable_looping(self):
        if self.audio_file is not None:
            pyfx_log.debug(f"Disable looping of {self.audio_file}")
            self._looping = False


class InterfaceAudioSource(AudioSource):
    audio_source_type = AudioSourceType.INTERFACE
    data_type_to_pa_format_map = MappingProxyType(
        {
            np.int8: pyaudio.paInt8,
            np.int16: pyaudio.paInt16,
            np.int32: pyaudio.paInt32,
            np.float32: pyaudio.paFloat32,
        }
    )

    def __init__(self, pa: pyaudio.PyAudio):
        super().__init__("Interface Audio Source")
        self.pa = pa
        self.queue = queue.Queue(maxsize=20)
        self._stream: pyaudio.Stream = None
        self.audio_driver: AudioDriverInfo = None
        self.audio_input_device: AudioDeviceInfo = None
        self.channels: list[int] = []

    def reset_queue(self):
        self.queue = queue.Queue(maxsize=20)

    def set_audio_driver(self, audio_driver: AudioDriverInfo):
        self.audio_driver = audio_driver
        if audio_driver is not None:
            pyfx_log.debug(f"Setting {self.name} audio driver to {audio_driver.driver_name}")

    def set_audio_input_device(self, audio_input_device: AudioDeviceInfo):
        self.audio_input_device = audio_input_device
        if audio_input_device is not None:
            pyfx_log.debug(f"Setting audio input device to {audio_input_device.name}")
            self.num_input_channels = audio_input_device.max_input_channels

    def set_audio_input_channels(self, channels: list[int]):
        pyfx_log.debug(f"Setting {self.name} channels to {channels}")
        self.channels = channels

    def read(self):
        if not self.streaming:
            return None
        try:
            return self.queue.get(timeout=0.1)
        except queue.Empty:
            return np.zeros((self.num_input_channels, self.buffer_size), dtype=self.data_type)

    def audio_source_callback(self, in_data: bytes, frame_count: int, time_info: dict, status: int):  # noqa: ARG002
        interleaved_audio_data = np.frombuffer(in_data, dtype=self.data_type)
        audio_channels = np.reshape(interleaved_audio_data, (frame_count, self.num_input_channels)).T
        audio_channels_out = np.vstack([audio_channels[channel] for channel in self.channels])
        self.queue.put(audio_channels_out)
        return (None, pyaudio.paContinue)

    def start_stream(self):
        super().start_stream()
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()

        self._stream = self.pa.open(
            format=self.data_type_to_pa_format_map[self.data_type],
            channels=self.audio_input_device.max_input_channels,
            rate=self.sample_rate,
            input=True,
            output=False,
            input_device_index=self.audio_input_device.index,
            frames_per_buffer=self.buffer_size,
            input_host_api_specific_stream_info=self.audio_driver.host_api_id,
            stream_callback=self.audio_source_callback,
        )

        self._stream.start_stream()

    def stop_stream(self):
        super().stop_stream()
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None
            self.reset_queue()


class TestToneAudioSource(AudioSource):
    audio_source_type = AudioSourceType.TEST_TONE

    def __init__(self):
        super().__init__("Test Tone Audio Source")
        self.frequency = 440
        self.volume_db = 0
        self.simulated_cpu_usage = 0
        self.theta = 0

    def read(self):
        if not self.streaming:
            return None

        duration = self.buffer_size * self.sample_period
        t = np.arange(start=0, stop=duration, step=self.sample_period, dtype=np.float32)
        tone = 10 ** (self.volume_db / 20) * np.sin(self.frequency * t * 2 * np.pi + self.theta, dtype=np.float32)
        self.theta += 2 * np.pi * self.frequency * duration
        self.theta = self.theta % (2 * np.pi)

        # Simulate CPU load
        time.sleep(duration * self.simulated_cpu_usage)

        return np.vstack([tone, tone])

    def set_frequency(self, frequency: int):
        pyfx_log.debug(f"Setting test tone frequency to {frequency}")
        self.frequency = frequency

    def set_volume_db(self, volume_db: int):
        pyfx_log.debug(f"Setting test tone volume to {volume_db} dB")
        self.volume_db = volume_db

    def set_simulated_cpu_usage(self, simulated_cpu_usage: float):
        if 0 > simulated_cpu_usage > 1:
            msg = f"Simulated CPU usage must be in the range [0,1], but it is currently set to {simulated_cpu_usage}"
            raise ValueError(msg)
        pyfx_log.debug(f"Setting test tone simulated CPU usage to {simulated_cpu_usage * 100} %")
        self.simulated_cpu_usage = simulated_cpu_usage
