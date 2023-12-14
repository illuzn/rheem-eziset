# Rheem EziSET Custom Component for Home Assistant

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

_Custom Component to integration to integrate [rheem_eziset][rheem_eziset] with Home Assistant._

## Notice
This component is in a very early alpha stage. The main branch has functioning flow, mode and status sensors.

This is very much a work in progress.

## Protocol
My documentation of the protocol is available here: https://illuzn.github.io/Rheem-Eziset-Protocol/

**This integration will set up the following entities.**

entity | Description
-- | --
`binary_sensor` | Show something `True` or `False`.
`sensor` | Show info from blueprint API.
`switch` | Switch something `True` or `False`.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `integration_blueprint`.
1. Download _all_ the files from the `custom_components/integration_blueprint/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Integration blueprint"

## Configuration is done in the UI

<!---->

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

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
