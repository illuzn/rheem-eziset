"""All API calls belong here."""
import time
import requests

from homeassistant.components.water_heater import WaterHeaterEntity
from homeassistant.components.number import NumberEntity
from homeassistant.exceptions import ConditionErrorMessage

from .const import LOGGER, DOMAIN


class RheemEziSETApi:
    """Define the Rheem EziSET API."""

    def __init__(self, host: str) -> None:
        """Initialise the basic parameters."""
        self.host = host
        self.base_url = f"http://{host}/"

    def get_data(self) -> dict:
        """Create a session and gather sensor data."""
        session = requests.Session()

        page = "getInfo.cgi"
        data_responses = self.get_responses(session=session, page=page)

        page = "version.cgi"
        data_responses |= self.get_responses(session=session, page=page)

        page = "getParams.cgi"
        data_responses |= self.get_responses(session=session, page=page)

        return data_responses

    def set_temp(self, water_heater: WaterHeaterEntity, temp: int):
        """Set temperature."""
        session = requests.Session()

        # Check for invalid settings
        mintemp = water_heater.min_temp
        maxtemp = water_heater.max_temp

        if temp is None:
            water_heater.rheem_target_temperature = None
            raise ConditionErrorMessage(type="invalid_temperature", message="{DOMAIN} - No temperature was set. Ignoring call to set temperature.")
        elif temp < int(mintemp):
            water_heater.rheem_target_temperature = None
            raise ConditionErrorMessage(
                type="minimum_temperature",
                message=f"""{DOMAIN} - An invalid temperature ({temp}) was attempted to be set.
                This is below the minimum temperature ({mintemp}).""",
            )
        elif temp > int(maxtemp):
            water_heater.rheem_target_temperature = None
            raise ConditionErrorMessage(
                type="maximum_temperature",
                message=f"""{DOMAIN} - An invalid temperature ({temp}) was attempted to be set.
                This is above the maximum temperature ({maxtemp}).""",
            )
        else:
            self.check_control_issues(entity=water_heater, reset_attribute="rheem_current_temperature", session=session)

        self.set_param(session=session, param=f"setTemp={temp}", response_param="reqtemp", response_check=temp)

    def set_session_timer(
        self,
        number: NumberEntity,
        session_timer: float,
    ):
        """Set session timer."""
        session = requests.Session()

        # Check for invalid settings
        if session_timer is None:
            number.rheem_session_timer = None
            raise ConditionErrorMessage(type="invalid_session_timer", message="{DOMAIN} - No session timer was set. Ignoring call to set session timer.")
        elif session_timer < 60:
            number.rheem_session_timer = None
            raise ConditionErrorMessage(
                type="minimum_session_timer",
                message=f"""{DOMAIN} - An invalid session timer ({session_timer}) was attempted to be set.
                This is below the minimum session timer (60).""",
            )
        elif session_timer > 900:
            number.rheem_session_timer = None
            raise ConditionErrorMessage(
                type="maximum_session_timer",
                message=f"""{DOMAIN} - An invalid session timer ({session_timer}) was attempted to be set.
                This is above the maximum temperature ({900}).""",
            )

        self.check_control_issues(entity=number, reset_attribute="rheem_session_timer", session=session)

        self.set_param(session=session, param=f"setSessionTimer={session_timer}", response_param="sessionTimer", response_check=session_timer)

        number.rheem_session_timer = None
        return

    def set_param(self, session: object, param: str, response_param: str, response_check: str):
        """Set parameters on Rheem."""
        # Attempt to take control
        page = "ctrl.cgi?sid=0&heatingCtrl=1"
        sid = 0
        data_response = self.get_responses(session=session, page=page)
        sid = data_response.get("sid")
        result = data_response.get("heatingCtrl")
        if result != 1 or sid == 0 or sid is None:
            # Something wrong happened. Log error and hand back control.
            LOGGER.error("%s - Error when retrieving %s. Result was: %s", DOMAIN, page, data_response)
            page = f"ctrl.cgi?sid={sid}&heatingCtrl=0"
            data_response = self.get_responses(session=session, page=page)
            LOGGER.error("%s - Attempted to release control with request: %s. Result was: %s", DOMAIN, page, data_response)
            return

        # Set param

        page = f"set.cgi?sid={sid}&{param}"
        data_response = self.get_responses(session=session, page=page)

        result = data_response.get(response_param)
        if result != response_check:
            # Something wrong happened. Log error and hand back control.
            LOGGER.error("%s - Error when setting %s by retrieving %s. Result was: %s", DOMAIN, param, page, data_response)
            page = f"ctrl.cgi?sid={sid}&heatingCtrl=0"
            data_response = self.get_responses(session=session, page=page)
            return

        # Per @bajarrr API seems to need a wait. Otherwise the setting doesn't set."
        time.sleep(0.15)

        # Release control
        page = f"ctrl.cgi?sid={sid}&heatingCtrl=0"
        data_response = self.get_responses(session=session, page=page)
        result = data_response.get("sid")
        if int(result) != 0:
            # Something wrong happened. Log error.
            LOGGER.error("%s - Couldn't to release control with request: %s. Result was: %s", DOMAIN, page, data_response)

    def check_control_issues(self, session: object, entity: object, reset_attribute: str):
        """Check for any issues with taking control."""
        page = "getInfo.cgi"
        result = self.get_responses(session=session, page=page)
        if result.get("sTimeout") != 0:
            entity.__dict__[reset_attribute] = None
            raise ConditionErrorMessage(
                type="invalid_sTimeout",
                message=f"""{DOMAIN} - Couldn't take control - it appears another user has control.
                Got this response: {result}""",
            )
        elif result.get("mode") != 5:
            entity.__dict__[reset_attribute] = None
            raise ConditionErrorMessage(
                type="invalid_mode",
                message=f"""{DOMAIN} - Couldn't take control - it appears that the water_heater is in use.
                Got this response: {result}""",
            )
        elif float(result.get("flow")) != 0:
            entity.__dict__[reset_attribute] = None
            raise ConditionErrorMessage(
                type="invalid_flow",
                message=f"""{DOMAIN} - Couldn't take control - it appears that the water_heater is in use.
                Got this response: {result}""",
            )

    def get_responses(
        self,
        session: object,
        page: str,
    ) -> dict:
        """Get page, check for valid json responses then convert to dict format."""
        base_url = self.base_url
        if base_url == "":
            LOGGER.error("%s - api attempted to retrieve an empty base_url.", DOMAIN)
            return None

        elif page == "":
            LOGGER.error("%s - api attempted to retrieve an empty page.", DOMAIN)
            return None

        else:
            url = base_url + page
            response = session.get(url, timeout=6.1)
            LOGGER.debug("%s - %s response: %s", DOMAIN, page, response.text)

            if isinstance(response, object) and response.headers.get("content-type") == "application/json":
                try:
                    data_response: dict = response.json()
                except Exception:  # pylint: disable=broad-except
                    LOGGER.error("%s - couldn't convert response for %s into json. Response was: %s", DOMAIN, url, response.text)
                return data_response
            else:
                LOGGER.error("%s - received response for %s but it doesn't appear to be json. Response: %s", DOMAIN, url, response.text)
