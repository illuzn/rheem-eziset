"""All API calls belong here."""
import requests

from .const import LOGGER, DOMAIN

class RheemEziSETApi:
    """This class defines the Rheem EziSET API."""

    def __init__(self, host: str) -> None:
        """Initialise the basic parameters."""
        self.host = host
        self.base_url = "http://" + self.host + "/"

    def getInfo_data(self) -> dict:
        """Create a session and get getInfo.cgi."""
        url = self.base_url + "getInfo.cgi"
        session = requests.Session()
        response = session.get(url, verify=False)
        LOGGER.debug(f"{DOMAIN} - getInfo.cgi response {response.text}")
        if response.headers.get('content-type') == 'application/json':
            try:
                data_response: dict = response.json()
            except Exception:
                LOGGER.error(f"{DOMAIN} - couldn't convert response for {url} into json. Response was: {response}")
            return data_response
        else:
            LOGGER.error(f"{DOMAIN} - received response for {url} but it doesn't appear to be json.")

    def get_XXXdata(self) -> dict:
        """Unused example."""
        url = self.base_url + "users/login"
        session = requests.Session()
        response = session.get(url, verify=False)

        # login with password
        url = self.base_url + "users/login"
        data = {"_method": "POST", "STLoginPWField": "", "function": "save"}
        response = session.post(url, headers=self.headers, data=data, verify=False)
        LOGGER.debug(f"{DOMAIN} - login response {response.text}")

        # actualize data request
        url = self.base_url + "home/actualizedata"
        response = session.post(url, headers=self.headers, verify=False)
        LOGGER.debug(f"{DOMAIN} - actualizedata response {response.text}")
        data_response: dict = response.json()

        # actualize signals request
        url = self.base_url + "home/actualizesignals"
        response = session.post(url, headers=self.headers, verify=False)
        LOGGER.debug(f"{DOMAIN} - actualizesignals response {response.text}")
        signal_response: dict = response.json()

        # logout
        url = self.base_url + "users/logout"
        response = session.get(url, verify=False)

        merged_response = data_response | signal_response
        LOGGER.debug(f"{DOMAIN} - merged_response {merged_response}")
        return merged_response


