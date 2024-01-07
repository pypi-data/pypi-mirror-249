from collections import deque

import numpy as np
from autogen.delay_pedal_variant_base import DelayPedalVariantBase


class DefaultDelayPedal(DelayPedalVariantBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.delay_buffer_index = 0  # Current position in the buffer

    def set_sample_rate(self, sample_rate: float):
        super().set_sample_rate(sample_rate)
        self.delay_buffer_size = int(self.time_max * self.sample_rate)
        self.delay_buffer = np.zeros(self.delay_buffer_size)
        self.delay_buffer_index = 0  # Current position in the buffer

    def process_audio(self, data: np.ndarray):
        """Default Delay Pedal Processing"""
        if self.on_off:
            num_samples = len(data[0])

            # Calculate the current delay time in samples
            current_delay_samples = int(self.time * self.sample_rate)
            read_indices = (
                np.arange(num_samples) + self.delay_buffer_index - current_delay_samples
            ) % self.delay_buffer_size

            # Read the delayed samples
            delayed_samples = self.delay_buffer[read_indices]

            # Write the new samples to the buffer with feedback
            write_indices = (np.arange(num_samples) + self.delay_buffer_index) % self.delay_buffer_size
            self.delay_buffer[write_indices] = data[0] + self.feedback * delayed_samples

            # Mix the dry and wet signals
            data[0] = (1 - self.dry_wet) * data[0] + self.dry_wet * delayed_samples

            # Update the buffer index
            self.delay_buffer_index = (self.delay_buffer_index + num_samples) % self.delay_buffer_size

            data[0] = data[0] * 1.4

        data[0] = data[0] * self.output

        return data
