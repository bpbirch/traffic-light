import time
from typing import Any, cast

import click
from pynput import keyboard

import traffic_light.domain.models as models
from traffic_light.service.handlers.traffic_light_handler import TrafficLightHandler

EXIT_PROGRAM = False
EXIT_MESSAGE = "Exiting Traffic Light Simulator"


def on_press(key: Any) -> None:
    global EXIT_PROGRAM
    try:
        if key.char == "q":
            EXIT_PROGRAM = True
    except AttributeError:
        pass


def listen_for_exit() -> keyboard.Listener:
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    return listener


def validate_color_inputs(value: str, param_name: str) -> int:
    try:
        val = int(value)
        if val < 0:
            raise ValueError
    except ValueError:
        raise click.BadParameter(
            click.style(f"{param_name} must be a non-negative integer.", fg="red")
        )
    return val


@click.command(
    help=f"Simulates a traffic light sequence. You can enter non-negative integer durations for green, yellow, and red lights. Total for all times must be greater than zero (so 1, 0, 0 would be a valid input for green, yellow, red, but 0, 0, 0 would not be). If you enter q during color time prompts, then the program will be exited. If you press q during the light display, the program will be exited. Upon exit, '{EXIT_MESSAGE}' will be printed to your terminal. If you enter a non-negative integer that is not q during color time prompting, you will be prompted to re-enter a non-negative integer. \n\nAfter color time prompts, you will be prompted to select whether you want the light display to be displayed indefinitely on repeat. The answer to that prompt defaults to Y/yes, which will cause the display to cycle indefinitley until the user presses q. If the user chooses n, then the light will go through one cycle, and then the program will exit."
)
def run_traffic_light() -> None:  # noqa: C901
    global EXIT_PROGRAM
    click.echo("\nEnter q to exit at any time.\n")
    listen_for_exit()

    green_time = None
    yellow_time = None
    red_time = None
    repeat_indefinitely = True  # Default value

    while True:
        try:
            # Prompt user for input
            # TODO: for extensibility, include prompt for non-standard SupportedLightType at input,
            # which will allow for different kinds of displays to be entered and printed by TrafficLightHandler

            if green_time is None:
                green_time_input = click.prompt(
                    "Enter the number of seconds for the green light", type=str
                )
                if green_time_input.lower() == "q":
                    click.echo(EXIT_MESSAGE)
                    return
                green_time = validate_color_inputs(green_time_input, "Green time")

            if yellow_time is None:
                yellow_time_input = click.prompt(
                    "Enter the number of seconds for the yellow light", type=str
                )
                if yellow_time_input.lower() == "q":
                    click.echo(EXIT_MESSAGE)
                    return
                yellow_time = validate_color_inputs(yellow_time_input, "Yellow time")

            if red_time is None:
                red_time_input = click.prompt(
                    "Enter the number of seconds for the red light", type=str
                )
                if red_time_input.lower() == "q":
                    click.echo(EXIT_MESSAGE)
                    return
                red_time = validate_color_inputs(red_time_input, "Red time")

            _repeat_indefinitely = click.prompt(
                "Do you want the light to display indefinitely, until you exit the program? It will only cycle once if you choose No.",
                type=click.Choice(["Y", "n"], case_sensitive=False),
                default="Y",
            )

            total_time = green_time + yellow_time + red_time
            if total_time <= 0:
                click.echo(
                    click.style(
                        "Total light color times must be greater than zero. Please re-enter your color times.",
                        fg="red",
                    )
                )
                green_time = None
                yellow_time = None
                red_time = None
                continue

            if _repeat_indefinitely.upper() == "Y":
                click.echo("The traffic light will display indefinitely.")
                repeat_indefinitely = True
            else:
                click.echo("The traffic light will cycle only once.")
                repeat_indefinitely = False

            break  # Exit the loop if total_time is valid

        except click.BadParameter as e:
            click.echo(e)

    click.echo(
        f"The configurations for colors are:\n"
        f'{click.style("green: " + str(green_time) + " seconds", fg="green")}\n'
        f'{click.style("yellow: " + str(yellow_time) + " seconds", fg="yellow")}\n'
        f'{click.style("red: " + str(red_time) + " seconds", fg="red")}'
    )

    try:
        traffic_light = models.TrafficLightServiceLayerModel(
            green_time=green_time,
            yellow_time=yellow_time,
            red_time=red_time,
        )
        traffic_light_handler = TrafficLightHandler(traffic_light=traffic_light)

        click.echo(f"traffic_light: {traffic_light}")
        if repeat_indefinitely:
            while True:
                if EXIT_PROGRAM:
                    click.clear()
                    click.echo(EXIT_MESSAGE)
                    return
                click.clear()
                displayed = traffic_light_handler.get_display()
                traffic_light.increment_signal_count()
                click.echo(displayed)
                time.sleep(1)
        else:
            for _ in range(cast(int, traffic_light.total_time)):
                if EXIT_PROGRAM:
                    click.clear()
                    click.echo(EXIT_MESSAGE)
                    return
                click.clear()
                displayed = traffic_light_handler.get_display()
                traffic_light.increment_signal_count()
                click.echo(displayed)
                time.sleep(1)
            click.clear()
            click.echo(EXIT_MESSAGE)

    except Exception as exc:
        click.echo(
            f"An error was encountered. {EXIT_MESSAGE} with exception {str(exc)}"
        )
