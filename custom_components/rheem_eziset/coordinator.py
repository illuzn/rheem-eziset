"""DataUpdateCoordinator for rheem_eziset."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import RheemEziSETApi
from .const import DOMAIN, LOGGER


class RheemEziSETDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    def __init__(self, hass: HomeAssistant, api: RheemEziSETApi, update_interval: int) -> None:
        """Initialize."""
        self.api = api
        self.platforms = []

        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=update_interval),
        )

    async def _async_update_data(self):
        """Update basic data via client."""
        try:
            result = await self.hass.async_add_executor_job(self.api.get_data)
            LOGGER.info("%s - Final getInfo_data result: %s", DOMAIN, result)
            return result
        except Exception as exception:
            raise UpdateFailed() from exception
