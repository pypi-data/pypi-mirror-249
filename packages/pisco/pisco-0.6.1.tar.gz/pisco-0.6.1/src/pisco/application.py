"""Central application logic of pisco."""


from __future__ import annotations

from typing import TYPE_CHECKING

from pisco.input_output import backlight, sonos_device
from pisco.user_interface import graphical_user_interface

if TYPE_CHECKING:
    import pathlib

SonosDeviceNotFoundError = sonos_device.SonosDeviceNotFoundError
SysfsBacklightFileAccessError = backlight.SysfsBacklightFileAccessError


def run(
    sonos_device_name: str,
    backlight_directory: pathlib.Path | None,
    window_width: int,
    window_height: int,
    playback_information_refresh_interval_in_ms: int,
) -> None:
    """Manages a Sonos device and an optional backlight and runs the user interface.

    Args:
        sonos_device_name: Name of the Sonos device to be controlled.
        backlight_directory: Sysfs directory of the backlight to be controlled.
        window_width: Width of the graphical user interface.
        window_height: Height of the graphical user interface.
        playback_information_refresh_interval_in_ms:
            Time in milliseconds after which the playback information is updated
            according to playback information from `sonos_device_name`.

    Raises:
        SonosDeviceNotFoundError:
            Found no device named `sonos_device_name`.
        SysfsBacklightFileAccessError:
            When the expected sysfs files in `backlight_directory`
            cannot be read or write.
    """
    with (
        sonos_device.SonosDevice(sonos_device_name) as sonos_device_,
        backlight.get_backlight(backlight_directory) as backlight_,
    ):
        graphical_user_interface.run(
            sonos_device_,
            backlight_,
            window_width,
            window_height,
            playback_information_refresh_interval_in_ms,
        )
