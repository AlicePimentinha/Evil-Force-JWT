"""
Utility module for building HTTP requests with custom headers, proxies, and configurations.
"""

import requests
from typing import Dict, Optional, Any

class RequestBuilder:
    """
    A class to build and configure HTTP requests.
    """
    def __init__(self, base_url: str = '', proxies: Optional[Dict[str, str]] = None, timeout: int = 10):
        self.base_url = base_url
        self.proxies = proxies
        self.timeout = timeout
        self.headers = {
            "User-Agent": "EVIL_JWT_FORCE/1.0",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        if proxies:
            self.session.proxies = proxies
        self.session.timeout = timeout

    def set_headers(self, extra: Dict[str, str]) -> None:
        """
        Update headers with additional values.
        Args:
            extra (dict): Additional headers to include or override defaults.
        """
        self.headers.update(extra)

    def build_payload(self, username: str, password: str) -> Dict[str, Any]:
        """
        Build a payload dictionary for authentication requests.
        Args:
            username (str): Username for authentication.
            password (str): Password for authentication.
        Returns:
            dict: Payload dictionary with username and password.
        """
        return {"username": username, "password": password}

    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """
        Send a GET request to the specified endpoint.
        Args:
            endpoint (str): The endpoint to send the request to.
            params (dict, optional): Query parameters for the request.
        Returns:
            requests.Response: Response object.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.get(url, headers=self.headers, params=params)

    def post(self, endpoint: str, data: Optional[Dict] = None) -> requests.Response:
        """
        Send a POST request to the specified endpoint.
        Args:
            endpoint (str): The endpoint to send the request to.
            data (dict, optional): Data payload for the request.
        Returns:
            requests.Response: Response object.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self.session.post(url, headers=self.headers, json=data)

def build_headers(extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """
    Build a dictionary of HTTP headers with default values and optional extras.
    
    Args:
        extra (dict, optional): Additional headers to include or override defaults.
    
    Returns:
        dict: Combined headers dictionary.
    """
    headers = {
        "User-Agent": "EVIL_JWT_FORCE/1.0",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }
    if extra:
        headers.update(extra)
    return headers

def build_payload(username: str, password: str) -> Dict[str, Any]:
    """
    Build a payload dictionary for authentication requests.
    
    Args:
        username (str): Username for authentication.
        password (str): Password for authentication.
    
    Returns:
        dict: Payload dictionary with username and password.
    """
    return {"username": username, "password": password}

def create_session(proxies: Optional[Dict[str, str]] = None, timeout: int = 10) -> requests.Session:
    """
    Create a configured requests Session object.
    
    Args:
        proxies (dict, optional): Proxy settings for the session.
        timeout (int): Timeout value for requests in seconds.
    
    Returns:
        requests.Session: Configured session object.
    """
    session = requests.Session()
    if proxies:
        session.proxies = proxies
    session.timeout = timeout
    return session 