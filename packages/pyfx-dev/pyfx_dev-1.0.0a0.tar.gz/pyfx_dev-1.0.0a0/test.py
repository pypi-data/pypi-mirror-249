import contextlib
import queue
import time

import numpy as np
import pyaudio

from pyfx.logger import pyfx_log

audio_queue = queue.Queue()


def input_callback(in_data: None, frame_count: int, time_info: dict, status: int):
    audio_queue.put(in_data)
    pyfx_log.debug(audio_queue.qsize())
    return (None, pyaudio.paContinue)


def output_callback(in_data: None, frame_count: int, time_info: dict, status: int):
    output_data = np.zeros((4, frame_count), dtype=np.float32)
    with contextlib.suppress(queue.Empty):
        queued_data: np.ndarray = audio_queue.get_nowait()
        queued_data_array = np.frombuffer(queued_data, np.float32)
        output_data[1] = queued_data_array

        # pyfx_log.debug(audio_queue.qsize())
    return (output_data.T.flatten().tobytes(), pyaudio.paContinue)


host_api = 3

pa = pyaudio.PyAudio()
input_stream = pa.open(
    format=pyaudio.paFloat32,
    channels=1,
    rate=48000,
    input=True,
    output=False,
    input_device_index=1,
    frames_per_buffer=128,
    input_host_api_specific_stream_info=host_api,
    stream_callback=input_callback,
)

output_stream = pa.open(
    format=pyaudio.paFloat32,
    channels=4,
    rate=48000,
    input=False,
    output=True,
    output_device_index=4,
    frames_per_buffer=128,
    output_host_api_specific_stream_info=host_api,
    stream_callback=output_callback,
)

output_stream.start_stream()
time.sleep(1)
input_stream.start_stream()


for _ in range(1):
    time.sleep(1)
    pyfx_log.debug(f"Input CPU: {input_stream.get_cpu_load()}")
    pyfx_log.debug(f"Output CPU: {output_stream.get_cpu_load()}")

output_stream.stop_stream()
input_stream.stop_stream()
