"""Sensor platform for rheem_eziset."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorStateClass
from homeassistant.const import TIME_MINUTES, VOLUME_LITERS, STATE_UNAVAILABLE

from .const import ICON_TAPON, ICON_TAPOFF, ICON_WATERHEATER, CONST_MODE_MAP, CONST_STATUS_MAP, DOMAIN
from .coordinator import RheemEziSETDataUpdateCoordinator
from .entity import RheemEziSETEntity

async def async_setup_entry(hass, entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    coordinator = hass.data[DOMAIN]

    SENSOR_MAP = [
        #("id",    "description",   "key",      "unit",                             "icon",             "device_class", "state_class",                  "entity_category"),
        ("flow",    "Flow",         "flow",     f"{VOLUME_LITERS}/{TIME_MINUTES}",  ICON_TAPON,        None,           SensorStateClass.MEASUREMENT,   None),
        ("status",  "Status",       "state",    None,                               ICON_WATERHEATER, None,           None,                           None),
        ("mode",    "Mode",         "mode",     None,                               ICON_WATERHEATER, None,           None,                           None),
    ]

    sensors = [
        RheemEziSETSensor(
            coordinator, entry, id, description, key, unit, icon, device_class, state_class, entity_category
        )
        for id, description, key, unit, icon, device_class, state_class, entity_category in SENSOR_MAP
    ]

    async_add_devices(sensors, True)

class RheemEziSETSensor(RheemEziSETEntity):
    """rheem_eziset Sensor class."""

    def __init__(
            self,
            coordinator: RheemEziSETDataUpdateCoordinator,
            entry: ConfigEntry,
            id: str,
            description: str,
            key: str,
            unit: str,
            icon: str,
            device_class: str,
            state_class: str,
            entity_category: str,
        ) -> None:
            """Initialize the sensor."""
            super().__init__(coordinator, entry)
            self._id = id
            self.description = description
            self.key = key
            self.unit = unit
            self._icon = icon
            self._device_class = device_class
            self._state_class = state_class
            self._entity_category = entity_category

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        with self.coordinator.data.get(self.key) as result:
            if self._id == "status":
                if int(result) in CONST_STATUS_MAP:
                    return CONST_STATUS_MAP[int(result)][1]
                return STATE_UNAVAILABLE
            elif self._id == "mode":
                if int(result) in CONST_MODE_MAP:
                    return CONST_MODE_MAP[int(result)][1]
                return STATE_UNAVAILABLE
            elif result is not None:
                return result
            else:
                return STATE_UNAVAILABLE
    @property
    def native_unit_of_measurement(self):
        """Return the native unit of measurement of the sensor."""
        return self.unit

    @property
    def icon(self):
        """Return the icon with processing in the case of some sensors."""
        with self.coordinator.data.get(self.key) as result:
            if self._id == "flow":
                try:
                    if float(result) != 0:
                        return ICON_TAPON
                    else:
                        return ICON_TAPOFF
                except Exception: # pylint: disable=unused-argument
                    return  ICON_TAPOFF
            elif self._id == "status":
                if int(result) in CONST_STATUS_MAP:
                    return CONST_STATUS_MAP[int(result)][2]
                return self._icon
            elif self._id == "mode":
                if int(result) in CONST_MODE_MAP:
                    return CONST_MODE_MAP[int(result)][2]
                return self._icon
            else:
                return self._icon


    @property
    def device_class(self):
        """Return the device class."""
        return self._device_class

    @property
    def name(self):
        """Return the sensor name."""
        return f"{self.description}"

    @property
    def id(self):
        """Return the sensor id."""
        return f"{DOMAIN}_{self._id}"

    @property
    def unique_id(self):
        """Return a unique id."""
        return f"{DOMAIN}-{self._id}-{self.coordinator.api.host}"

    @property
    def state_class(self):
        """Return the sensor state class."""
        return self._state_class

    @property
    def entity_category(self):
        """Return the entity category."""
        return self._entity_category
