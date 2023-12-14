"""Adds config flow for Rheem EziSET."""
from __future__ import annotations

import voluptuous as vol
import traceback

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_HOST

from .const import DOMAIN, LOGGER, CONF_SYNC_INTERVAL, DEFAULT_SYNC_INTERVAL
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

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            # Test connectivity
            valid = await self._test_host(user_input[CONF_HOST])

            if valid:
                return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)
            else:
                self._errors["base"] = "connection"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input): # pylint: disable=unused-argument
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_HOST): str}
            ),
            errors=self._errors,
        )

    async def _test_host(self, host: str) -> None:
        """Validate host."""
        try:
            api = RheemEziSETApi(host=host)
            await self.hass.async_add_executor_job(api.getInfo_data)
            return True
        except Exception as ex: # pylint: disable=broad-except
            LOGGER.error(
                f"{DOMAIN} Exception in connection: $s - trackback: %s",
                ex,
                traceback.format_exc(),
            )
        return False

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Allow the options to be configured."""
        return OptionsFlow(config_entry)

class OptionsFlow(config_entries.OptionsFlow):
    """Options flow for Rheem EziSET."""

    def __init__(self, config_entry):
        """Initialise the options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_int(self, user_input=None): # pylint: disable=unused-argument
        """Handle flow."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle flow initiated by user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SYNC_INTERVAL,
                        default=self.options.get(
                            CONF_SYNC_INTERVAL, DEFAULT_SYNC_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int))
                }
            )
        )

    async def _update_options(self):
        """Process options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_SYNC_INTERVAL), data=self.options
        )
