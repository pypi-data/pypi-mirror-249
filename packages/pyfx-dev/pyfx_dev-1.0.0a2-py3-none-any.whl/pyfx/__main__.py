import click

from pyfx.pedal_builder.pedal_builder_app import pedal_builder_app


@click.group()
def cli():
    pass


@click.command()
@click.argument("pedal_folder", required=False)
def pedal_builder(pedal_folder):
    if not pedal_folder:
        pedal_folder = "./pedals"

    pedal_builder_app(pedal_folder)


cli.add_command(pedal_builder)

if __name__ == "__main__":
    cli()
