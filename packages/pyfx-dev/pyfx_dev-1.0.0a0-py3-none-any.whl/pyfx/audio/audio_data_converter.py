import numpy as np
from numpy.typing import DTypeLike


class AudioDataConverter:
    @staticmethod
    def convert(data: np.ndarray, new_dtype: DTypeLike):
        """Converts data from its current type to the specified type"""

        def int8_to_int16(data: np.ndarray):
            return (data.astype(np.int16)) << 8

        def int8_to_int32(data: np.ndarray):
            return (data.astype(np.int32)) << 24

        def int16_to_int32(data: np.ndarray):
            return (data.astype(np.int32)) << 16

        def int32_to_int16(data: np.ndarray):
            return (data >> 16).astype(np.int16)

        def int32_to_int8(data: np.ndarray):
            return (data >> 24).astype(np.int8)

        def int16_to_int8(data: np.ndarray):
            return (data >> 8).astype(np.int8)

        def int_to_float32(data: np.ndarray, current_dtype: DTypeLike):
            return data.astype(np.float32) / abs(np.iinfo(current_dtype).min)

        def float32_to_int(data: np.ndarray, new_dtype: DTypeLike):
            return (data * np.iinfo(new_dtype).max).astype(new_dtype)

        conversion_map = {
            ("int8", "int16"): int8_to_int16,
            ("int8", "int32"): int8_to_int32,
            ("int16", "int32"): int16_to_int32,
            ("int32", "int16"): int32_to_int16,
            ("int32", "int8"): int32_to_int8,
            ("int16", "int8"): int16_to_int8,
            ("int8", "float32"): lambda data: int_to_float32(data, np.int8),
            ("int16", "float32"): lambda data: int_to_float32(data, np.int16),
            ("int32", "float32"): lambda data: int_to_float32(data, np.int32),
            ("float32", "int8"): lambda data: float32_to_int(data, np.int8),
            ("float32", "int16"): lambda data: float32_to_int(data, np.int16),
            ("float32", "int32"): lambda data: float32_to_int(data, np.int32),
        }

        current_dtype_name = np.dtype(data.dtype).name
        new_dtype_name = np.dtype(new_dtype).name
        conversion_function = conversion_map.get((current_dtype_name, new_dtype_name))

        if conversion_function:
            return conversion_function(data)
        else:
            msg = f"Unsupported conversion from {current_dtype_name} to {new_dtype_name}"
            raise ValueError(msg)
