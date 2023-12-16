"""All API calls belong here."""
import time
import requests

from .const import LOGGER, DOMAIN

class RheemEziSETApi:
    """This class defines the Rheem EziSET API."""

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
        data_responses |=  self.get_responses(session=session, page=page)

        return data_responses

    def set_temp(
            self,
            temp: int
            ):
        """Set temperature."""
        session = requests.Session()

        # Attempt to take control
        page = "ctrl.cgi?sid=0&heatingCtrl=1"

        sid = 0
        loops = 0

        data_response = self.get_responses(session=session,page=page)
        sid = data_response.get("sid", 0)
        loops += 1

        result = data_response.get("heatingCtrl")
        if result != 1:
            # Something wrong happened. Log error and hand back control.
            LOGGER.error(
                "%s - Error when retrieving %s. Result was: %s",
                DOMAIN,
                page,
                data_response
                )
            page = f"ctrl.cgi?sid={sid}&heatingCtrl=0"
            data_response = self.get_responses(session=session,page=page)
            return

        # Set temperature

        page = f"set.cgi?sid={sid}&setTemp={temp}"
        data_response = self.get_responses(session=session,page=page)

        result = data_response.get("reqtemp")
        if int(result) != temp:
            # Something wrong happened. Log error and hand back control.
            LOGGER.error(
                "%s - Error when retrieving %s. Result was: %s",
                DOMAIN,
                page,
                data_response)
            page = f"ctrl.cgi?sid={sid}&heatingCtrl=0"
            data_response = self.get_responses(session=session,page=page)
            return

        # Per @bajarrr API seems to need a wait. Otherwise the temperature doesn't set."
        time.sleep(0.15)

        # Release control
        page = f"ctrl.cgi?sid={sid}&heatingCtrl=0"
        data_response = self.get_responses(session=session,page=page)
        result = data_response.get("sid")
        if int(result) != 0:
            # Something wrong happened. Log error.
            LOGGER.error(
                "%s - Error when retrieving %s. Result was: %s",
                DOMAIN,
                page,
                data_response
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

            if (
                isinstance(response, object) and
                response.headers.get('content-type') == "application/json"
            ):
                try:
                    data_response:  dict = response.json()
                except Exception: # pylint: disable=broad-except
                    LOGGER.error(
                        "%s - couldn't convert response for %s into json. Response was: %s",
                        DOMAIN,
                        url,
                        response.text
                        )
                return data_response
            else:
                LOGGER.error(
                    "%s - received response for %s but it doesn't appear to be json. Response: %s",
                    DOMAIN,
                    url,
                    response.text
                    )
