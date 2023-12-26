"""Water heater platform for rheem_eziset."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.components.water_heater import WaterHeaterEntity, WaterHeaterEntityFeature, STATE_GAS, STATE_OFF
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature, CONF_HOST, PRECISION_WHOLE

from .api import RheemEziSETApi
from .const import DOMAIN
from .coordinator import RheemEziSETDataUpdateCoordinator
from .entity import RheemEziSETEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Add water heater for passed config_entry in HA."""
    coordinator = hass.data[DOMAIN]

    water_heater = [RheemEziSETWaterHeater(coordinator, entry)]

    async_add_devices(water_heater, True)


class RheemEziSETWaterHeater(RheemEziSETEntity, WaterHeaterEntity):
    """rheem_eziset Water Heater class."""

    def __init__(
        self,
        coordinator: RheemEziSETDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, entry)
        self._attr_current_operation = STATE_OFF
        self._attr_operation_list: [STATE_GAS, STATE_OFF]
        self._attr_precision = PRECISION_WHOLE
        self._attr_supported_features = WaterHeaterEntityFeature.TARGET_TEMPERATURE
        self._attr_target_temperature = self.coordinator.data.get("tempMin")
        self._attr_current_temperature = None
        self._attr_has_entity_name = True
        self.rheem_target_temperature = self.coordinator.data.get("temp")
        self.rheem_current_temperature = self.coordinator.data.get("temp")
        self.entry = entry

    @property
    def name(self):
        """Return a name."""
        return "Water Heater"

    @property
    def unique_id(self):
        """Return a unique id."""
        return f"{self.entry.entry_id}-water-heater"

    @property
    def extra_state_attributes(self):
        """Return the optional entity specific state attributes."""
        data = {"target_temp_step": PRECISION_WHOLE}
        return data

    @property
    def precision(self) -> float:
        """Return the precision of the system."""
        return PRECISION_WHOLE

    @property
    def temperature_unit(self) -> str:
        """Return the unit of measurement used by the platform."""
        return UnitOfTemperature.CELSIUS

    @property
    def current_operation(self):
        """Return the state of the sensor."""
        mode = self.coordinator.data.get("mode")
        if mode == 15 or mode == 25:
            return STATE_GAS
        else:
            return STATE_OFF

    @property
    def supported_features(self):
        """Return the Supported features of the water heater."""
        return self._attr_supported_features

    @property
    def min_temp(self):
        """Return the minimum temperature that can be set."""
        return self.coordinator.data.get("tempMin")

    @property
    def max_temp(self):
        """Return the maximum temperature that can be set."""
        return self.coordinator.data.get("tempMax")

    @property
    def current_temperature(self):
        """Return the current temperature ."""
        result = self.coordinator.data.get("temp")
        self.rheem_current_temperature = result
        return self.coordinator.data.get("temp")

    @property
    def target_temperature(self):
        """Return the target temperature or the current temperature if there is no target."""
        if self.rheem_current_temperature is not None:
            return self.rheem_current_temperature
        else:
            return self.current_temperature

    def set_temperature(self, **kwargs):
        """Set the target temperature of the water heater."""
        api = RheemEziSETApi(host=self.entry.data.get(CONF_HOST))
        temp = kwargs.get(ATTR_TEMPERATURE)
        self.rheem_target_temperature = temp
        api.set_temp(water_heater=self, temp=temp)
        self.rheem_current_temperature = None
