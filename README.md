# clap-switch 👏💡

Clap switch for VM-CLAP1 sensor, LIFX bulbs and RaspberryPi.

The script reacts on your claps, turning a bulb ON and OFF.

![My setup](https://i.imgur.com/spnHjBK.jpg)

## Prerequisites

* [VM-CLAP1](https://www.pololu.com/product/2580/specs) clap sensor from Verbal Machines.
  _(Works as a GPIO Button. Performs really well, ignoring all background noises.)_
* LiFX bulb
* RaspberryPi
* Python3 (with pip) and make

## Installation

1. Edit settings `clap-switch.systemd` file to meet your needs.
2. `make`
3. `systemctl start clap-switch`

## Settings

| Name                           | Default       | Description                                                                                                               |
|--------------------------------|---------------|---------------------------------------------------------------------------------------------------------------------------|
| `CLAP_SWITCH_GPIO_BUTTON`      | 2             | GPIO pin the sensor is connected to.                                                                                      |
| `CLAP_SWITCH_LIGHT_NAME`       | 'Main'        | Name of a LiFX bulb you want to switch ON and OFF.                                                                        |
| `CLAP_SWITCH_LIGHT_BRIGHTNESS` | 65535 (100%)  | The bulb will be turned on with this brightness.                                                                          |
| `CLAP_SWITCH_LIGHT_TEMP`       | 4000 (Kelvin) | Color temperature of the bulb.                                                                                            |
| `CLAP_SWITCH_CLAP_COUNT`       | 2             | How many claps in a sequence should the sensor recognize (helps preventing false claps, produced by doors, drawers, etc.) |
| `CLAP_SWITCH_SEQ_ALLOWANCE`    | 3.0 (seconds) | Length of the clapping sequence.                                                                                          |
| `CLAP_SWITCH_RAPID`            | False         | If `True`, the script will wait for an acknowledge from the bulb after each command sent.                                 |
| `CLAP_SWITCH_LOG_LEVEL`        | 'INFO'        | If `DEBUG`, the script will write a clap counter status after each clap.                                                  |
| `CLAP_SWITCH_RETRY_COUNT`      | 2             | How many times should the script retry a command to the bulb if failed.                                                   |

## Links

* https://chicagodist.com/blogs/news/vm-clap1-sensor-gpiozero-on-raspberry-pi
