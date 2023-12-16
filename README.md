# Rheem EziSET Custom Component for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

_Custom Component to integration to integrate [rheem_eziset][rheem_eziset] with Home Assistant._

## Notice
This component is in a very early alpha stage. The main branch has functioning flow, mode, error, status and timeout sensors and a water heater control.

This is very much a work in progress.

## Protocol
My documentation of the protocol is available here: https://illuzn.github.io/Rheem-Eziset-Protocol/

**This integration will set up the following entities.**

Entity | Description
-- | --
entity name prefixes | All entity names will be prefixed with the heaterName read from your device. This defaults to "Rheem" however you can use the app to change it to any 8 character alphanumeric identifier you want.
`water_heater.water_heater` | Controls the water heater. It reads the min, current and max temps from your water heater. It also supports setting the target temperature to your desired value.
`binary_sensor.heater_error` | Will be off for no error and on for an error. The error code will be provided in sensor.error_code (it is not known at this time  what the possible codes are)
`sensor.flow` | The current flow rate of the water heater in L/min as reported by the water heater.
`sensor.status` | The current status of the  water heater. Possible modes are: Idle, Heating, Bath Fill Complete (Off)
`sensor.mode` | The current mode of the water heater. Possible modes are: Idle, Heating Control Mode, Heating (Conventional Mode), Idle (Bath Fill Mode Waiting for Tap), Heating (Bath Fill Mode), Idle (Bath Fill Mode Complete)
`sensor.status_raw` | The raw status code provided by the water heater. Known status codes are 1, 2, 3.
`sensor.mode_raw` | The raw mode code provided by the water heater. Known mode codes are 5, 10, 15, 20, 25, 35.
`sensor.heater_error_raw` | The raw heater error code provided by the water heater. 0 is normal but the other codes are unknown.
`sensor.session_timeout` | The time in seconds until the current user's session times out. This will only apply if there is a communication error with the water heater or if somebody is using the app or a physical device in the house to control the water heater. You are locked out of controls while someone else is in control.

## Installation

### HACS

1. In HACS, go to Integrations and add this repository `https://github.com/illuzn/rheem-eziset` as an Integration.
2. Press Explore & Download Repositories and download Rheem Eziset.

### Manual Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `rheem_eziset`.
1. Download _all_ the files from the `custom_components/rheem_eziset/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Rheem EziSET"

## Configuration is done in the UI

By default the sensors update every 5s. You can change this in the options, but be warned, if you perform too many requests per second your device will assume its under a DoS attack and refuse all connections. If your device has a poor connection i.e. heater and powerline unit are too far apart you may need to reduce this number - a symptom of this will be the ability to initially connect but not getting updated data over time.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

## Credits
[ludeeus](https://github.com/ludeeus) for the amazing [Integration Blueprint](https://github.com/ludeeus/integration_blueprint)

[bajarrr](https://github.com/bajarrr) for his work in deciphering the api.

## Intellectual Property
Rheem and EZiSET are trademarks of Rheem Australia Pty Ltd in Australia and their respective owners worldwide. These trademarks are used on these pages under fair use and no affiliation or association with Rheem Australia Pty Ltd or any of its group companies is intended or to be inferred by the use of these marks.

***

[rheem_eziset]: https://github.com/illuzn/rheem-eziset
[buymecoffee]: https://www.buymeacoffee.com/illuzn
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/illuzn/rheem-eziset.svg?style=for-the-badge
[commits]: https://github.com/illuzn/rheem-eziset/commits/main
[license-shield]: https://img.shields.io/github/license/illuzn/rheem-eziset.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40ludeeus-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/illuzn/rheem-eziset.svg?style=for-the-badge
[releases]: https://github.com/illuzn/rheem-eziset/releases
