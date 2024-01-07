import pyaudio

from pyfx.audio.audio_device import AudioDeviceInfo
from pyfx.audio.audio_driver import AudioDriverInfo
from pyfx.logger import pyfx_log


class AudioInterfaceInfo:
    def __init__(self, pa: pyaudio.PyAudio):
        self.pa = pa
        self.audio_devices: list[AudioDeviceInfo] = self._get_audio_devices()
        self.audio_input_devices: list[AudioDeviceInfo] = self._get_audio_input_devices()
        self.audio_output_devices: list[AudioDeviceInfo] = self._get_audio_output_devices()
        self.audio_drivers: list[AudioDriverInfo] = self._get_audio_drivers()

    def _get_audio_devices(self) -> list[AudioDeviceInfo]:
        """List all available audio devices."""
        info = self.pa.get_host_api_info_by_index(0)
        num_devices = info.get("deviceCount")
        devices = []
        for device_id in range(num_devices):
            device_info = self.pa.get_device_info_by_host_api_device_index(0, device_id)
            devices.append(
                AudioDeviceInfo(
                    name=device_info["name"],
                    index=device_info["index"],
                    struct_version=device_info["structVersion"],
                    host_api=device_info["hostApi"],
                    max_input_channels=device_info["maxInputChannels"],
                    max_output_channels=device_info["maxOutputChannels"],
                    default_low_input_latency=device_info["defaultLowInputLatency"],
                    default_low_output_latency=device_info["defaultLowOutputLatency"],
                    default_high_input_latency=device_info["defaultHighInputLatency"],
                    default_high_output_latency=device_info["defaultHighOutputLatency"],
                    default_sample_rate=device_info["defaultSampleRate"],
                )
            )
        return devices

    def _get_audio_input_devices(self) -> list[AudioDeviceInfo]:
        return [device for device in self.audio_devices if device.is_input]

    def _get_audio_output_devices(self) -> list[AudioDeviceInfo]:
        return [device for device in self.audio_devices if device.is_output]

    def _get_audio_drivers(self) -> list[AudioDriverInfo]:
        host_api_count = self.pa.get_host_api_count()
        audio_drivers = []
        for host_api_id in range(host_api_count):
            api_info = self.pa.get_host_api_info_by_index(host_api_id)
            audio_drivers.append(
                AudioDriverInfo(
                    driver_name=api_info["name"],
                    host_api_id=host_api_id,
                )
            )
        return audio_drivers
