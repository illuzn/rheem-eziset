"""Water heater platform for rheem_eziset."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.number import (
    NumberEntity,
)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.const import UnitOfTime, CONF_HOST

from .api import RheemEziSETApi
from .const import DOMAIN, ICON_TIMER
from .coordinator import RheemEziSETDataUpdateCoordinator
from .entity import RheemEziSETEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Add water heater for passed config_entry in HA."""
    coordinator = hass.data[DOMAIN]

    number = [RheemEziSETNumber(coordinator, entry)]

    async_add_devices(number, True)


class RheemEziSETNumber(RheemEziSETEntity, NumberEntity):
    """rheem_eziset Number class."""

    def __init__(
        self,
        coordinator: RheemEziSETDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the number."""
        super().__init__(coordinator, entry)
        self._attr_has_entity_name = True
        self._attr_native_min_value = 60
        self._attr_native_max_value = 900
        self._attr_native_step = 1
        self._attr_native_unit_of_measurement = UnitOfTime.SECONDS
        self._attr_icon = ICON_TIMER
        self._attr_name = "Session Timeout"
        self._attr_unique_id = f"{self.entry.entry_id}-number"
        self.entry = entry
        self._attr_entity_category = EntityCategory.CONFIG
        self.rheem_session_timer: float = None

    @property
    def native_value(self):
        """Return the session timer or the current session timer if there is no target."""
        if self.rheem_session_timer is not None:
            return self.rheem_session_timer
        else:
            return self.coordinator.data.get("sessionTimer")

    def set_native_value(self, value: float) -> None:
        """Set the session timer of the water heater."""
        api = RheemEziSETApi(host=self.entry.data.get(CONF_HOST))
        session_timer = self.rheem_session_timer = value
        api.set_session_timer(number=self, session_timer=session_timer)
