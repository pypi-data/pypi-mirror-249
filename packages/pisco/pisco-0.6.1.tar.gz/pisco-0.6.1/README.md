# Pisco

Pisco is a keyboard-only controller for Sonos speakers.
While Pisco's graphical interface displays the album art of the track currently playing,
you can control playback using your keyboard.

<p>
   <img
      src="https://raw.githubusercontent.com/christophgietl/pisco/main/images/pisco-on-mac.png"
      style="aspect-ratio: 864/920; height: auto; max-width: 100%; width: 432px;"
      alt="Pisco running on macOS"
      title="Pisco running on macOS"
   />
</p>

Pisco has been tested on Linux and macOS.
It is especially well suited for use with
small displays (e.g. [Pimoroni HyperPixel 4.0 Square](https://shop.pimoroni.com/products/hyperpixel-4-square?variant=30138251477075)) and
media remote controls (e.g. [Satechi Bluetooth Multi-Media Remote](https://satechi.net/products/satechi-bluetooth-multi-media-remote?variant=27129644617)).

<p>
   <img
      src="https://raw.githubusercontent.com/christophgietl/pisco/main/images/pisco-on-pi-zero.jpg"
      style="aspect-ratio: 500/678; height: auto; max-width: 100%; width: 250px;"
      alt="Pisco running on a Raspberry Pi Zero attached to a Pimoroni HyperPixel 4.0 Square surrounded by a Satechi Bluetooth Multi-Media Remote and a Sonos speaker"
      title="Pisco running on a Raspberry Pi Zero attached to a Pimoroni HyperPixel 4.0 Square surrounded by a Satechi Bluetooth Multi-Media Remote and a Sonos speaker"
   />
</p>

## Setup

To set up Pisco on a regular Linux or macOS machine, follow these steps:

1. Make sure you are using Python 3.9 or higher.
2. Create a virtual environment if you do not want to clutter up your default environment.
3. Install Pisco:
    ```shell
    pip3 install pisco
    ```

For a clean and minimalist deployment
on a [Raspberry Pi Zero](https://www.raspberrypi.com/products/raspberry-pi-zero/),
please see
[the directory `deployment`](https://github.com/christophgietl/pisco/tree/main/deployment).


## Usage

When starting Pisco,
you need to specify the name of the Sonos device (i.e. Sonos room) you want to control:

```shell
pisco Leseecke  # Replace 'Leseecke' with the name of your Sonos device.
```

You can use the option `--help` to find additional options:
```text
$ pisco --help
Usage: pisco [OPTIONS] SONOS_DEVICE_NAME

  Control your Sonos device with your keyboard

Options:
  -b, --backlight DIRECTORY    sysfs directory of the backlight that should be
                               deactivated when the device is not playing
  -w, --width INTEGER RANGE    width of the Pisco window  [default: 320; x>=0]
  -h, --height INTEGER RANGE   height of the Pisco window  [default: 320;
                               x>=0]
  -r, --refresh INTEGER RANGE  time in milliseconds after which playback
                               information is updated  [default: 40; x>=1]
  --help                       Show this message and exit.
```

Once Pisco is running, you can use the following keys to control playback:
- ⏯ (or return) to pause or resume playback
- ⏹ to stop playback
- ⏮ and ⏭ (or left and right arrow) to play the previous or next track
- 0️⃣ to 9️⃣ to play the top 10 tracks (or radio stations) of your Sonos favorites
- ➕ and ➖ (or up and down arrow) to increase or decrease volume
- 🔇 to mute or unmute
