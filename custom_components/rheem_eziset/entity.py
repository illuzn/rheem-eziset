"""Sets up the basic entity template."""
from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NAME, MANUFACTURER
from .coordinator import RheemEziSETDataUpdateCoordinator

class RheemEziSETEntity(CoordinatorEntity):
    """Basic entity definition used by all entities."""

    def __init__(self, coordinator: RheemEziSETDataUpdateCoordinator, entry):
        """Initialise the entity."""
        super().__init__(coordinator)
        self.entry = entry

    @property
    def device_info(self):
        """Defines the device information."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.api.host)},
            "name": self.coordinator.data.get("heaterName", NAME),
            "manufacturer": MANUFACTURER,
            "sw_version": self.coordinator.data.get("FWversion")
        }

    @property
    def available(self) -> bool:
        """Returns the availability of the device. Assume True if there is data."""
        return not not self.coordinator.data

    @property
    def should_poll(self) -> bool:
        """Device should not poll because this is handled by async requests in the api."""
        return False
