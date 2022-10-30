"""Class for connecting to ForeningLet API and retrieve users"""
from os import environ
import requests


class ForeningLet:
    """
    Interface to the ForeningLet API
    Will take the following from environment variables:
    API_PASSWORD = The password for the ForeningLet API
    API_USERNAME = The username for the ForeningLet API
    API_BASE_URL = Base URL for the ForeningLet API
    API_MEMBERS_API = The endpoint for the ForeningLet Member API
    API_VERSION = The version of the ForeningLet Member API
    """

    api_username = ""
    api_password = ""
    api_base_url = ""
    api_members_path = ""
    api_version = ""
    api_members_url = ""

    def __init__(self) -> None:
        self.api_password = environ.get("API_PASSWORD")
        self.api_username = environ.get("API_USERNAME")
        self.api_base_url = environ.get("API_BASE_URL")
        self.api_members_path = environ.get("API_MEMBERS_API")
        self.api_version = environ.get("API_VERSION")
        self.api_members_url = (
            f"{self.api_base_url}{self.api_members_path}?{self.api_version}"
        )

    def fl_api_get(self, url):
        """
        Retrieves data from an api endpoint
        authenticates with the class api_username and api_password
        """
        resp = requests.get(url, auth=(self.api_username, self.api_password))
        return resp

    def check_api_responds(self):
        """Helper method to check the api endpoint responds"""
        resp = self.fl_api_get(self.api_members_url)
        return resp.status_code

    def get_memberlist(self):
        """Retrieves members from the member API endpoint"""
        resp = self.fl_api_get(self.api_members_url)
        return resp.text
