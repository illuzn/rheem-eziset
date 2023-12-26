"""
Custom integration to integrate rheem_eziset with Home Assistant.

For more details about this integration, please refer to
https://github.com/illuzn/rheem-eziset/
"""

from __future__ import annotations

import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST

from .api import RheemEziSETApi
from .const import DOMAIN, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, LOGGER, PLATFORMS
from .coordinator import RheemEziSETDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    LOGGER.debug(
        "Setting up entry for device: %s",
        entry.title,
    )

    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    host = entry.data.get(CONF_HOST)
    api = RheemEziSETApi(host=host)
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    coordinator = RheemEziSETDataUpdateCoordinator(hass, api=api, update_interval=scan_interval)

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN] = coordinator

    for platform in PLATFORMS:
        if entry.options.get(platform, True):
            coordinator.platforms.append(platform)
            hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, platform))

    entry.add_update_listener(async_reload_entry)  # Reload the entry on configuration changes.

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN]
    unloaded = all(await asyncio.gather(*[hass.config_entries.async_forward_entry_unload(entry, platform) for platform in PLATFORMS if platform in coordinator.platforms]))
    if unloaded:
        hass.data[DOMAIN] = []

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
