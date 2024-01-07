import os

import click

from pyfx.logger import pyfx_log
from pyfx.pedal_builder.pedal_builder_app import pedal_builder_app


@click.group()
def cli():
    pass


@click.command()
@click.argument("pedal_folder", required=False)
@click.option("--with-examples", is_flag=True, help="Add examples to pedal folder")
def pedal_builder(pedal_folder: str, with_examples: bool):  # noqa: FBT001
    if not pedal_folder:
        pedal_folder = os.path.join(os.getcwd(), "pedals")

    pedal_builder_app(pedal_folder, with_examples=with_examples)


cli.add_command(pedal_builder)

if __name__ == "__main__":
    cli()
