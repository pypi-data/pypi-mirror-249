from dataclasses import dataclass


@dataclass
class AudioDeviceInfo:
    name: str
    index: int
    struct_version: int
    host_api: int
    max_input_channels: int
    max_output_channels: int
    default_low_input_latency: float
    default_low_output_latency: float
    default_high_input_latency: float
    default_high_output_latency: float
    default_sample_rate: int

    def __repr__(self):
        return "\n".join(
            [
                self.name,
                f"    index: {self.index}",
                f"    struct_version: {self.struct_version}",
                f"    host_api: {self.host_api}",
                f"    max_input_channels: {self.max_input_channels}",
                f"    max_output_channels: {self.max_output_channels}",
                f"    default_low_input_latency: {self.default_low_input_latency}",
                f"    default_low_output_latency: {self.default_low_output_latency}",
                f"    default_high_input_latency: {self.default_high_input_latency}",
                f"    default_high_output_latency: {self.default_high_output_latency}",
                f"    default_sample_rate: {self.default_sample_rate}",
            ]
        )

    @property
    def is_input(self):
        return self.max_input_channels > 0

    @property
    def is_output(self):
        return self.max_output_channels > 0
