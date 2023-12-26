"""Binary Sensor platform for rheem_eziset."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.helpers.entity import EntityCategory

from .const import DOMAIN, IDPREFIX
from .coordinator import RheemEziSETDataUpdateCoordinator
from .entity import RheemEziSETEntity

BINARY_SENSOR_MAP = [
    # ("description", "key", "icon", "device_class", "entity_category"),
    ("Heater error", "appErrCode", None, BinarySensorDeviceClass.PROBLEM, EntityCategory.DIAGNOSTIC),  # pylint: disable=line-too-long
]


async def async_setup_entry(hass, entry, async_add_devices):
    """Add binary sensors for passed config_entry in HA."""
    coordinator = hass.data[DOMAIN]

    binary_sensors = [RheemEziSETBinarySensor(coordinator, entry, description, key, icon, device_class, entity_category) for description, key, icon, device_class, entity_category in BINARY_SENSOR_MAP]
    binary_sensors.append(RheemEziSETProblemBinarySensor(coordinator, entry))

    async_add_devices(binary_sensors, True)


class RheemEziSETBinarySensor(RheemEziSETEntity):
    """rheem_eziset Binary Sensor class."""

    def __init__(
        self,
        coordinator: RheemEziSETDataUpdateCoordinator,
        entry: ConfigEntry,
        description: str,
        key: str,
        icon: str,
        device_class: str,
        entity_category: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._id = f"{IDPREFIX}{id}"
        self.description = description
        self.key = key
        self._icon = icon
        self._device_class = device_class
        self._entity_category = entity_category
        self._attr_has_entity_name = True

    @property
    def state(self):
        """Return the state of the binary sensor."""
        result = self.coordinator.data[self.key]
        if self.key == "appErrCode":
            if int(result) == 0:
                return "off"
            return "on"
        else:
            return "off"

    @property
    def icon(self):
        """Return the icon with processing in the case of some sensors."""
        return self._icon

    @property
    def device_class(self):
        """Return the device class."""
        return self._device_class

    @property
    def name(self):
        """Return the sensor name."""
        return self.description

    @property
    def unique_id(self):
        """Return a unique id."""
        return f"{self.entry.entry_id}-{self.description}"

    @property
    def entity_category(self):
        """Return the entity category."""
        return self._entity_category


class RheemEziSETProblemBinarySensor(RheemEziSETEntity):
    """rheem_eziset Binary Sensor class."""

    def __init__(
        self,
        coordinator: RheemEziSETDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._id = f"{IDPREFIX}{id}"
        self.description = "Connectivity Problem"
        self._device_class = BinarySensorDeviceClass.CONNECTIVITY
        self._entity_category = EntityCategory.DIAGNOSTIC
        self._attr_has_entity_name = True

    @property
    def state(self) -> bool:
        """Return the state of the binary sensor."""
        if self.coordinator.problem_flag is False:
            return "on"
        else:
            return "off"

    @property
    def available(self) -> bool:
        """Override availability, this one should always be available."""
        return True

    @property
    def device_class(self):
        """Return the device class."""
        return BinarySensorDeviceClass.CONNECTIVITY

    @property
    def name(self):
        """Return the sensor name."""
        return "Connectivity Problem"

    @property
    def unique_id(self):
        """Return a unique id."""
        return f"{self.entry.entry_id}-connectivity-problem"

    @property
    def entity_category(self):
        """Return the entity category."""
        return EntityCategory.DIAGNOSTIC
