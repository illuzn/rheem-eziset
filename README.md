# Rheem EziSET Custom Component for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

_Custom Component to integration to integrate [rheem_eziset][rheem_eziset] with Home Assistant._

## Notice

This component is in a release candidate stage. The released package has been tested by at least the author. The main branch should be considered beta branch. The dev branch is experimental and may break at any time.

## Protocol

My documentation of the protocol is available here: https://illuzn.github.io/Rheem-Eziset-Protocol/

## Warning

While this integration does not allow you to do anything which the app lets you do. Using this integration makes it easier to set your hot water temperature (and also inadvertently set it incorrectly). While 50C meets Australian Standards for hot water, you should be aware of the following:

- Hot water temperature will vary depending on how close/ far the outlet you are using is. Your installer should have tested the temperature at the closest outlet to the heater (but my installer didn't do this).
- There are internal dip switches inside your water heater that offset the read temperature by +/-3C. This means that a setting of 50C may actually be 53C (which is outside the guidelines). The installer manual is available online.
- I strongly recommend setting up an automation to restore your water heater to a default low setting to avoid the risk of inadvertent burns/scalding. Remember, not everyone in your house knows that you have set the hot water to piping hot (and this may especially be an issue with young children or the elderly).

**This integration will set up the following entities.**

| Entity                                | Enabled by Default | Description                                                                                                                                                                                                                                                                                                     |
| ------------------------------------- | ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| entity name prefixes                  |                    | All entity names will be prefixed with the heaterName read from your device. This defaults to "Rheem" however you can use the app to change it to any 8 character alphanumeric identifier you want.                                                                                                             |
| `water_heater.water_heater`           | True               | Controls the water heater. It reads the min, current and max temps from your water heater. It also supports setting the target temperature to your desired value.                                                                                                                                               |
| `binary_sensor.heater_error`          | True               | Will be off for no error and on for an error. The error code will be provided in sensor.error_code (it is not known at this time what the possible codes are)                                                                                                                                                   |
| `binary_sensory.connectivity_problem` | True               | Because of the noisy nature of powerline comms, connectivity between the unit and powerline adapter can be easily degraded. For best results, ensure that the heater and powerline unit are plugged into the same power circuit. A connectivity problem is only raised in the event 5 successive requests fail. |
| `sensor.flow`                         | True               | The current flow rate of the water heater in L/min as reported by the water heater.                                                                                                                                                                                                                             |
| `sensor.status`                       | True               | The current status of the water heater. Possible modes are: Idle, Heating, Bath Fill Complete (Off)                                                                                                                                                                                                             |
| `sensor.mode`                         | True               | The current mode of the water heater. Possible modes are: Idle, Heating Control Mode, Heating (Conventional Mode), Idle (Bath Fill Mode Waiting for Tap), Heating (Bath Fill Mode), Idle (Bath Fill Mode Complete)                                                                                              |
| `sensor.session_timeout`              | True               | The time in seconds until the current user's session times out. This will only apply if there is a communication error with the water heater or if somebody is using the app or a physical device in the house to control the water heater. You are locked out of controls while someone else is in control.    |
| `number.session_timeout`              | True               | Configures the default session timeout. It is recommended to set the session time out to the lowest permitted value of 60. In the future, this will be used to attempt to maintain a persistent control session (and enable changing temperature while the heater is active).                                   |
| `sensor.status_raw`                   | False              | The raw status code provided by the water heater. Known status codes are 1, 2, 3.                                                                                                                                                                                                                               |
| `sensor.mode_raw`                     | False              | The raw mode code provided by the water heater. Known mode codes are 5, 10, 15, 20, 25, 35.                                                                                                                                                                                                                     |
| `sensor.heater_error_raw`             | False              | The raw heater error code provided by the water heater. 0 is normal but the other codes are unknown.                                                                                                                                                                                                            |
| `sensor.current_temperature`          | False              | Useful for setting up a safety automation.                                                                                                                                                                                                                                                                      |
| `sensor.heater_model`                 | False              | Reports the heater model. The only known model at this stage is "1".                                                                                                                                                                                                                                            |
| `sensor.heater_name`                  | False              | Reports the internal heater name (configurable via the app).                                                                                                                                                                                                                                                    |

## Installation

### HACS

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=illuzn&repository=rheem-eziset&category=integration)

### Manual Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `rheem_eziset`.
1. Download _all_ the files from the `custom_components/rheem_eziset/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Rheem EziSET"

## Configuration is done in the UI

By default the sensors update every 5s. You can change this in the options, but be warned, if you perform too many requests per second your device will assume its under a DoS attack and refuse all connections. If your device has a poor connection (i.e. heater and powerline unit aren't on the same power circuit) you may need to reduce this number - a symptom of this will be the ability to initially connect but not getting updated data over time.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits

[ludeeus](https://github.com/ludeeus) for the amazing [Integration Blueprint](https://github.com/ludeeus/integration_blueprint)

[bajarrr](https://github.com/bajarrr) for his work in deciphering the api.

[dymondj](https://github.com/dymondj) for correcting my erroneous knowledge regarding how the powerline unit works.

## Intellectual Property

Rheem and EZiSET are trademarks of Rheem Australia Pty Ltd in Australia and their respective owners worldwide. These trademarks are used on these pages under fair use and no affiliation or association with Rheem Australia Pty Ltd or any of its group companies is intended or to be inferred by the use of these marks.

---

[rheem_eziset]: https://github.com/illuzn/rheem-eziset
[buymecoffee]: https://www.buymeacoffee.com/illuzn
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/illuzn/rheem-eziset.svg?style=for-the-badge
[commits]: https://github.com/illuzn/rheem-eziset/commits/main
[license-shield]: https://img.shields.io/github/license/illuzn/rheem-eziset.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40illuzn-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/illuzn/rheem-eziset.svg?style=for-the-badge
[releases]: https://github.com/illuzn/rheem-eziset/releases
