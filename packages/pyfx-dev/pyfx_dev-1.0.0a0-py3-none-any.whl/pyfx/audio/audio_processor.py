import numpy as np
from numpy.typing import DTypeLike

from pyfx.logger import pyfx_log


class AudioProcessor:
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

    def process_audio(self, data: np.ndarray) -> np.ndarray:
        return data

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
