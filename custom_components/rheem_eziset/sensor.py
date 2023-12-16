"""Sensor platform for rheem_eziset."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.helpers.entity import EntityCategory
from homeassistant.const import UnitOfTime, UnitOfVolume, STATE_UNAVAILABLE

from .const import (
    ICON_RAW,
    ICON_TAPON,
    ICON_TAPOFF,
    ICON_TIMER,
    ICON_WATERHEATER,
    CONST_MODE_MAP,
    CONST_STATUS_MAP,
    DOMAIN,
    LOGGER
)
from .coordinator import RheemEziSETDataUpdateCoordinator
from .entity import RheemEziSETEntity

TIME_MINUTES = UnitOfTime.MINUTES
TIME_SECONDS = UnitOfTime.SECONDS
VOLUME_LITERS = UnitOfVolume.LITERS

SENSOR_MAP = [
#("description", "key", "unit", "icon", "device_class", "state_class", "entity_category"), # pylint: disable=line-too-long
("Flow", "flow", f"{VOLUME_LITERS}/{TIME_MINUTES}", ICON_TAPON, None, SensorStateClass.MEASUREMENT, None), # pylint: disable=line-too-long
("Status", "state", None, ICON_WATERHEATER, None, None, None), # pylint: disable=line-too-long
("Mode", "mode", None, ICON_WATERHEATER, None, None, None), # pylint: disable=line-too-long
("Status raw", "state", None, ICON_RAW, None, SensorStateClass.MEASUREMENT, EntityCategory.DIAGNOSTIC), # pylint: disable=line-too-long
("Mode raw", "mode", None, ICON_RAW, None, SensorStateClass.MEASUREMENT, EntityCategory.DIAGNOSTIC), # pylint: disable=line-too-long
("Heater error raw", "appErrCode", None, ICON_RAW, None, SensorStateClass.MEASUREMENT, EntityCategory.DIAGNOSTIC), # pylint: disable=line-too-long
("Session timeout", "sTimeout", TIME_SECONDS, ICON_TIMER, SensorDeviceClass.DURATION, SensorStateClass.MEASUREMENT, EntityCategory.DIAGNOSTIC), # pylint: disable=line-too-long

]

async def async_setup_entry(hass, entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""
    coordinator = hass.data[DOMAIN]





    sensors = [
        RheemEziSETSensor(
            coordinator,
            entry,
            description,
            key,
            unit,
            icon,
            device_class,
            state_class,
            entity_category
        )
        for description, key, unit, icon, device_class, state_class, entity_category in SENSOR_MAP
    ]

    async_add_devices(sensors, True)

class RheemEziSETSensor(RheemEziSETEntity):
    """rheem_eziset Sensor class."""

    def __init__(
            self,
            coordinator: RheemEziSETDataUpdateCoordinator,
            entry: ConfigEntry,
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
        self.description = description
        self.key = key
        self.unit = unit
        self._icon = icon
        self._device_class = device_class
        self._state_class = state_class
        self._entity_category = entity_category
        self._attr_has_entity_name = True

    @property
    def state(self):
        """Return the state of the sensor."""
        result = self.coordinator.data.get(self.key, STATE_UNAVAILABLE)
        if self.description == "Status":
            try:
                result = int(result)
                if int(result) in CONST_STATUS_MAP:
                    return CONST_STATUS_MAP[int(result)][0]
                return STATE_UNAVAILABLE
            except Exception: # pylint: disable=broad-except
                LOGGER.error(
                    "%s -  Unexpected result for status, result was %s",
                    DOMAIN,
                    result
                    )
                return STATE_UNAVAILABLE
        elif self.description == "Mode":
            try:
                result = int(result)
                if int(result) in CONST_MODE_MAP:
                    return CONST_MODE_MAP[int(result)][0]
                return STATE_UNAVAILABLE
            except Exception: # pylint: disable=broad-except
                LOGGER.error(
                    "%s -  Unexpected result for mode, result was %s",
                    DOMAIN,
                    result
                    )
        else:
            return result

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of the sensor."""
        return self.unit

    @property
    def icon(self):
        """Return the icon with processing in the case of some sensors."""
        result = self.coordinator.data.get(self.key, STATE_UNAVAILABLE)
        if self.description == "Flow":
            try:
                if float(result) != 0:
                    return ICON_TAPON
                else:
                    return ICON_TAPOFF
            except Exception: # pylint: disable=broad-except
                return  ICON_TAPOFF
        elif self.description == "Status":
            if int(result) in CONST_STATUS_MAP:
                return CONST_STATUS_MAP[int(result)][1]
            return self._icon
        elif self.description == "Mode":
            if int(result) in CONST_MODE_MAP:
                return CONST_MODE_MAP[int(result)][1]
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
        return self.description

    @property
    def unique_id(self):
        """Return a unique id."""
        return f"{self.entry.entry_id}-{self.description}"

    @property
    def state_class(self):
        """Return the sensor state class."""
        return self._state_class

    @property
    def entity_category(self):
        """Return the entity category."""
        return self._entity_category
