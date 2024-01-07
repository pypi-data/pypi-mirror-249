# SPDX-FileCopyrightText: 2023-present Keaton Scheible <thatdspguy@gmail.com>
#
# SPDX-License-Identifier: MIT
import os

os.environ["PYFX_ROOT"] = os.path.dirname(os.path.abspath(__file__))
os.environ["ASSETS_FOLDER"] = os.path.join(os.environ["PYFX_ROOT"], "assets")
os.environ["AUDIO_ASSETS_FOLDER"] = os.path.join(os.environ["ASSETS_FOLDER"], "audio")
os.environ["PYFX_LOGO"] = os.path.join(os.environ["ASSETS_FOLDER"], "pyfx_logo.png")
os.environ["PYFX_EXAMPLE_PEDALS"] = os.path.join(os.environ["ASSETS_FOLDER"], "pedals")
