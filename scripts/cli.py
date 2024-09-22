import click
from traffic_light.service.traffic_light_cli import run_traffic_light


@click.group()
def cli() -> None:
    pass


cli.add_command(run_traffic_light, name="run-traffic-light")

if __name__ == "__main__":
    cli()
