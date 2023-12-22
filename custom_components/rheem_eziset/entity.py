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
        self.counter_update_fails = 0
        self.coordinator.problem_flag = False

    @property
    def device_info(self):
        """Defines the device information."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.api.host)},
            "name": self.coordinator.data.get("heaterName", NAME),
            "manufacturer": MANUFACTURER,
            "sw_version": self.coordinator.data.get("FWversion"),
        }

    @property
    def available(self) -> bool:
        """Returns the availability of the device."""
        test = self.coordinator.last_update_success

        # Unavailable if 5 successive requests failed
        if self.counter_update_fails >= 4 and test is False:
            self.coordinator.problem_flag = True
            return test
        # If successful reset the counter and mark available
        if test is True:
            self.counter_update_fails = 0
            self.coordinator.problem_flag = False
            return test
        # Otherwise increment counter and try again on next scheduled update
        else:
            self.counter_update_fails += 1
            return True

    @property
    def should_poll(self) -> bool:
        """Device should not poll because this is handled by async requests in the api."""
        return False
