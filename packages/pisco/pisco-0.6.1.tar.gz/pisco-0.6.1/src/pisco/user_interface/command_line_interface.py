"""Command line interface for pisco."""

from __future__ import annotations

import logging
import pathlib

import click

from pisco import application

logger = logging.getLogger(__name__)

_backlight_directory_option = click.Option(
    help="""
        sysfs directory of the backlight that should be deactivated
        when the device is not playing
    """,
    param_decls=("-b", "--backlight", "backlight_directory"),
    type=click.Path(exists=True, file_okay=False, path_type=pathlib.Path),
)

_sonos_device_name_argument = click.Argument(param_decls=("sonos_device_name",))


@click.command(
    params=(
        _sonos_device_name_argument,
        _backlight_directory_option,
        click.Option(
            default=320,
            help="width of the Pisco window",
            param_decls=("-w", "--width", "window_width"),
            show_default=True,
            type=click.IntRange(min=0),
        ),
        click.Option(
            default=320,
            help="height of the Pisco window",
            param_decls=("-h", "--height", "window_height"),
            show_default=True,
            type=click.IntRange(min=0),
        ),
        click.Option(
            default=40,
            help="time in milliseconds after which playback information is updated",
            param_decls=("-r", "--refresh", "playback_information_refresh_interval"),
            show_default=True,
            type=click.IntRange(min=1),
        ),
    )
)
def run(
    sonos_device_name: str,
    backlight_directory: pathlib.Path | None,
    window_width: int,
    window_height: int,
    playback_information_refresh_interval: int,
) -> None:
    """Control your Sonos device with your keyboard."""
    try:
        application.run(
            sonos_device_name,
            backlight_directory,
            window_width,
            window_height,
            playback_information_refresh_interval,
        )
    except application.SysfsBacklightFileAccessError as e:
        raise click.BadParameter(
            message=f"Cannot {e.mode} file {e.path}.",
            param=_backlight_directory_option,
        ) from e
    except application.SonosDeviceNotFoundError as e:
        raise click.BadParameter(
            message=f"Cannot find Sonos device '{e.name}'.",
            param=_sonos_device_name_argument,
        ) from e
    except Exception:
        logger.exception("Exception has not been handled.")
        raise
