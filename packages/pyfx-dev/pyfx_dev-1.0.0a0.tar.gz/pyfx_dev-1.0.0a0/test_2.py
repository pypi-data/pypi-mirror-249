import numpy as np

channel_array = np.array(
    [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [11, 12, 13, 14, 15, 16, 17, 18, 19],
    ]
)

frame_index = 7
num_frames = 3
total_num_frames = channel_array.shape[1]

start_idx = frame_index
stop_idx = start_idx + num_frames
output = channel_array[:, start_idx:stop_idx]

if stop_idx > total_num_frames:
    output = np.hstack([output, channel_array[:, : stop_idx % total_num_frames]])


print(output)


a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], dtype=np.uint8)
b = a.reshape(-1, 3)
num_rows = b.shape[0]
b = np.hstack([np.zeros((num_rows, 1), dtype=np.uint8), b])
byte_array = b.flatten().tobytes()
x = np.frombuffer(byte_array, dtype=np.int16)

print(b)
print(byte_array)
print(x)
