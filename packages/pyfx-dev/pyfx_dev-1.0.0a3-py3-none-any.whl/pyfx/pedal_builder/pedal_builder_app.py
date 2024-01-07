import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import QApplication

from pyfx.audio.audio_controller import PyFxAudioController
from pyfx.logger import pyfx_log
from pyfx.pedal_builder.pedal_builder import PedalBuilder
from pyfx.widgets.pedal_builder_main_window import PedalBuilderMainWindow


def load_stylesheet(filepath):
    with open(filepath) as file:
        return file.read()


def pedal_builder_app(pedal_folder: Path | str, with_examples: bool):  # noqa: FBT001
    pyfx_log.debug(f"pedal_folder in app {pedal_folder}")
    if not isinstance(pedal_folder, Path):
        pedal_folder = Path(pedal_folder)
    pedal_folder.mkdir(exist_ok=True)

    if with_examples:
        example_pedal_folder = Path(os.environ.get("PYFX_EXAMPLE_PEDALS"))
        example_pedal_folder_startup_cfg = example_pedal_folder / "startup.cfg"
        pedal_folder_startup_cfg = pedal_folder / "startup.cfg"
        if not pedal_folder_startup_cfg.exists():
            shutil.copyfile(example_pedal_folder_startup_cfg, pedal_folder_startup_cfg)

        for pedal_subfolder in example_pedal_folder.iterdir():
            source_subfolder = example_pedal_folder / pedal_subfolder.stem
            destination_subfolder = pedal_folder / pedal_subfolder.stem

            if source_subfolder.is_dir():
                if not destination_subfolder.exists():
                    shutil.copytree(source_subfolder, destination_subfolder)
                else:
                    pyfx_log.debug(
                        f"Skipping {pedal_subfolder} pedal since it already exists in {pedal_folder.as_posix()}"
                    )

    pyfx_log.info(f'Pedal Builder Opened: {datetime.now().strftime("%b-%d-%Y %H:%M:%S")}')  # noqa: DTZ005

    app = QApplication(sys.argv)

    current_folder = Path(__file__).parent
    stylesheet_file = current_folder / "pedal_builder_app_stylesheet.qss"
    stylesheet = load_stylesheet(stylesheet_file)
    app.setStyleSheet(stylesheet)

    audio_controller = PyFxAudioController()
    pedal_builder = PedalBuilder(root_pedal_folder=pedal_folder)
    window = PedalBuilderMainWindow(
        pedal_builder=pedal_builder,
        audio_controller=audio_controller,
    )

    window.show()

    ret = app.exec()

    pyfx_log.info(f'Pedal Builder Closed: {datetime.now().strftime("%b-%d-%Y %H:%M:%S")}\n')  # noqa: DTZ005

    sys.exit(ret)


if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Run Pedal Builder App.")
    parser.add_argument("-p", "--pedal_folder", default="./pedals", help="Specify the pedal folder path.")
    args = parser.parse_args()

    pedal_folder = Path(args.pedal_folder)
    # if pedal_folder.exists():
    #     shutil.rmtree(pedal_folder)
    pedal_builder_app(pedal_folder, with_examples=True)
