"""Adds config flow for Rheem EziSET."""
from __future__ import annotations

import traceback
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_HOST

from .const import DOMAIN, LOGGER, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
from .api import RheemEziSETApi


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for rheem_eziset."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialise the flow with no errors."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            # Don't allow duplicates
            current_entries = self._async_current_entries()
            for entry in current_entries:
                if user_input[CONF_HOST] == entry.title:
                    return self.async_abort(reason="host_already_exists")

            # Test connectivity
            valid = await self._test_host(user_input[CONF_HOST])

            if valid:
                return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)
            else:
                self._errors["base"] = "connection"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=self._errors,
        )

    async def _test_host(self, host: str) -> None:
        """Validate host."""
        try:
            api = RheemEziSETApi(host=host)
            await self.hass.async_add_executor_job(api.get_data)
            return True
        except Exception as ex:  # pylint: disable=broad-except
            LOGGER.error(
                f"{DOMAIN} Exception in connection: $s - trackback: %s",
                ex,
                traceback.format_exc(),
            )
        return False

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntries) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Options flow for Rheem EziSET."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialise the options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input):
        """Handle an option flow."""
        config = {**self.config_entry.data, **self.config_entry.options}

        if user_input is not None:
            config = {**config, **user_input}
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_SCAN_INTERVAL, description={"suggested_value": DEFAULT_SCAN_INTERVAL}): vol.All(vol.Coerce(int)),
                }
            ),
        )
