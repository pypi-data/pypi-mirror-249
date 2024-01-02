import re
import ssl
import time
from typing import Any, Dict, Optional, Union

import httpx
import msal
from attrs import define, evolve, field


def to_valid_filename(s):
    """Converts a string to a safe filename.

    Replaces spaces with underscores, and the regex removes any
    characters from the string that are not word characters, hyphens,
    or periods.
    """

    s = str(s).strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", s)


class AuthenticationFailed(Exception):
    pass


@define
class Client:
    """A class for keeping track of data related to the API

    The following are accepted as keyword arguments and will be used to construct httpx Clients internally:

        ``base_url``: The base URL for the API, all requests are made to a relative path to this URL

        ``cookies``: A dictionary of cookies to be sent with every request

        ``headers``: A dictionary of headers to be sent with every request

        ``timeout``: The maximum amount of a time a request can take. API functions will raise
        httpx.TimeoutException if this is exceeded.

        ``verify_ssl``: Whether or not to verify the SSL certificate of the API server. This should be True in production,
        but can be set to False for testing purposes.

        ``follow_redirects``: Whether or not to follow redirects. Default value is False.

        ``httpx_args``: A dictionary of additional arguments to be passed to the ``httpx.Client`` and ``httpx.AsyncClient`` constructor.


    Attributes:
        raise_on_unexpected_status: Whether or not to raise an errors.UnexpectedStatus if the API returns a
            status code that was not documented in the source OpenAPI document. Can also be provided as a keyword
            argument to the constructor.
    """

    raise_on_unexpected_status: bool = field(default=False, kw_only=True)
    _base_url: str
    _cookies: Dict[str, str] = field(factory=dict, kw_only=True)
    _headers: Dict[str, str] = field(factory=dict, kw_only=True)
    _timeout: Optional[httpx.Timeout] = field(default=None, kw_only=True)
    _verify_ssl: Union[str, bool, ssl.SSLContext] = field(default=True, kw_only=True)
    _follow_redirects: bool = field(default=False, kw_only=True)
    _httpx_args: Dict[str, Any] = field(factory=dict, kw_only=True)
    _client: Optional[httpx.Client] = field(default=None, init=False)
    _async_client: Optional[httpx.AsyncClient] = field(default=None, init=False)
    _ms_client: msal.PublicClientApplication = None
    _auth: dict = None

    def with_headers(self, headers: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional headers"""
        if self._client is not None:
            self._client.headers.update(headers)
        if self._async_client is not None:
            self._async_client.headers.update(headers)
        return evolve(self, headers={**self._headers, **headers})

    def with_cookies(self, cookies: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional cookies"""
        if self._client is not None:
            self._client.cookies.update(cookies)
        if self._async_client is not None:
            self._async_client.cookies.update(cookies)
        return evolve(self, cookies={**self._cookies, **cookies})

    def with_timeout(self, timeout: httpx.Timeout) -> "Client":
        """Get a new client matching this one with a new timeout (in seconds)"""
        if self._client is not None:
            self._client.timeout = timeout
        if self._async_client is not None:
            self._async_client.timeout = timeout
        return evolve(self, timeout=timeout)

    def set_httpx_client(self, client: httpx.Client) -> "Client":
        """Manually the underlying httpx.Client

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._client = client
        return self

    def get_httpx_client(self) -> httpx.Client:
        """Get the underlying httpx.Client, constructing a new one if not previously set"""
        self.refresh_access_token()
        if self._client is None:
            self._client = httpx.Client(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )
        return self._client

    def __enter__(self) -> "Client":
        """Enter a context manager for self.client—you cannot enter twice (see httpx docs)"""
        self.get_httpx_client().__enter__()
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        """Exit a context manager for internal httpx.Client (see httpx docs)"""
        self.get_httpx_client().__exit__(*args, **kwargs)

    def set_async_httpx_client(self, async_client: httpx.AsyncClient) -> "Client":
        """Manually the underlying httpx.AsyncClient

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._async_client = async_client
        return self

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        """Get the underlying httpx.AsyncClient, constructing a new one if not previously set"""
        self.refresh_access_token()
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )
        return self._async_client

    def is_token_expired(self):
        """Check if the existing token is expired"""
        current_time = int(time.time())
        return self._auth["id_token_claims"]["exp"] < current_time

    def refresh_access_token(self):
        """If existing token is expired then fetch a new access token using the refresh token"""
        if self._auth and self.is_token_expired():
            scopes = self._auth["scope"]
            self._auth = self._ms_client.acquire_token_by_refresh_token(
                refresh_token=self._auth["refresh_token"], scopes=scopes
            )
            if "access_token" in self._auth:
                self.token = self._auth["access_token"]
                self._auth["scope"] = scopes
                print("Access token refreshed.")
            elif self._auth["id_token_claims"]["idp"] == "google.com":
                self.token = self._auth["id_token"]
                self._auth["scope"] = scopes
                print("Access token refreshed.")
            else:
                print("Invalid Token / Token expired you need to login again")

    async def __aenter__(self) -> "Client":
        """Enter a context manager for underlying httpx.AsyncClient—you cannot enter twice (see httpx docs)"""
        await self.get_async_httpx_client().__aenter__()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        """Exit a context manager for underlying httpx.AsyncClient (see httpx docs)"""
        await self.get_async_httpx_client().__aexit__(*args, **kwargs)


@define
class AuthenticatedClient:
    """A Client which has been authenticated for use on secured endpoints

    The following are accepted as keyword arguments and will be used to construct httpx Clients internally:

        ``base_url``: The base URL for the API, all requests are made to a relative path to this URL

        ``cookies``: A dictionary of cookies to be sent with every request

        ``headers``: A dictionary of headers to be sent with every request

        ``timeout``: The maximum amount of a time a request can take. API functions will raise
        httpx.TimeoutException if this is exceeded.

        ``verify_ssl``: Whether or not to verify the SSL certificate of the API server. This should be True in production,
        but can be set to False for testing purposes.

        ``follow_redirects``: Whether or not to follow redirects. Default value is False.

        ``httpx_args``: A dictionary of additional arguments to be passed to the ``httpx.Client`` and ``httpx.AsyncClient`` constructor.


    Attributes:
        raise_on_unexpected_status: Whether or not to raise an errors.UnexpectedStatus if the API returns a
            status code that was not documented in the source OpenAPI document. Can also be provided as a keyword
            argument to the constructor.
        token: The token to use for authentication
        prefix: The prefix to use for the Authorization header
        auth_header_name: The name of the Authorization header
    """

    raise_on_unexpected_status: bool = field(default=False, kw_only=True)
    _base_url: str
    _cookies: Dict[str, str] = field(factory=dict, kw_only=True)
    _headers: Dict[str, str] = field(factory=dict, kw_only=True)
    _timeout: Optional[httpx.Timeout] = field(default=None, kw_only=True)
    _verify_ssl: Union[str, bool, ssl.SSLContext] = field(default=True, kw_only=True)
    _follow_redirects: bool = field(default=False, kw_only=True)
    _httpx_args: Dict[str, Any] = field(factory=dict, kw_only=True)
    _client: Optional[httpx.Client] = field(default=None, init=False)
    _async_client: Optional[httpx.AsyncClient] = field(default=None, init=False)
    _ms_client: msal.PublicClientApplication = None
    _auth: dict = None

    token: str = None
    prefix: str = "Bearer"
    auth_header_name: str = "Authorization"

    def with_headers(self, headers: Dict[str, str]) -> "AuthenticatedClient":
        """Get a new client matching this one with additional headers"""
        if self._client is not None:
            self._client.headers.update(headers)
        if self._async_client is not None:
            self._async_client.headers.update(headers)
        return evolve(self, headers={**self._headers, **headers})

    def with_cookies(self, cookies: Dict[str, str]) -> "AuthenticatedClient":
        """Get a new client matching this one with additional cookies"""
        if self._client is not None:
            self._client.cookies.update(cookies)
        if self._async_client is not None:
            self._async_client.cookies.update(cookies)
        return evolve(self, cookies={**self._cookies, **cookies})

    def with_timeout(self, timeout: httpx.Timeout) -> "AuthenticatedClient":
        """Get a new client matching this one with a new timeout (in seconds)"""
        if self._client is not None:
            self._client.timeout = timeout
        if self._async_client is not None:
            self._async_client.timeout = timeout
        return evolve(self, timeout=timeout)

    def login(self) -> None:
        """Get access token from SINTEF AD."""
        sintef_ad_client_id = (
            "b454696a-def0-4481-825f-fed836d600e3"  # "api-dev.oceanlab.sintef.no", registered in SINTEF Tenant
        )
        sintef_ad_authority = "https://login.microsoftonline.com/e1f00f39-6041-45b0-b309-e0210d8b32af"
        self._ms_client = msal.PublicClientApplication(client_id=sintef_ad_client_id, authority=sintef_ad_authority)
        scopes = [f"{sintef_ad_client_id}/.default"]
        flow = self._ms_client.initiate_device_flow(scopes=scopes)
        print(flow["message"])
        self._auth = self._ms_client.acquire_token_by_device_flow(flow)
        self.token = self._auth["access_token"]
        self._auth["scope"] = scopes
        print("You are now authenticated.")

    def login_external(self) -> None:
        """Get ID token from B2C."""
        dsn_b2c_client_id = (
            "3e7d58ba-7a4e-4f67-957d-931cc60ed4b4"  # Registered in datasintefdev.onmicrosoft.com B2C Tenant
        )
        dsn_b2c_authority = "https://datasintefdev.b2clogin.com/7272a89b-4f78-4aaa-82b6-c49329164dcc/b2c_1_susi_local"
        self._ms_client = msal.PublicClientApplication(client_id=dsn_b2c_client_id, authority=dsn_b2c_authority)
        scopes = ["https://datasintefdev.onmicrosoft.com/b2capp2/.default"]
        print("A browser window with a login screen should open, select 'Google' as the login option.")
        self._auth = self._ms_client.acquire_token_interactive(scopes=scopes)
        if self._auth["id_token_claims"]["idp"] == "google.com":
            self.token = self._auth["id_token"]
            self._auth["scope"] = scopes
            print("You are now authenticated.")
        else:  # User selected the unsupported SINTEF AD login option
            raise AuthenticationFailed(
                "You have not been authenticated. Logging in with SINTEF AD using \
                `login_external()` is currently not supported. \n\nSelect 'Google' \
                when logging in as an external user. (Clear browser cookies to be \
                presented with the 'Google' option again.)"
            )

    def set_httpx_client(self, client: httpx.Client) -> "AuthenticatedClient":
        """Manually the underlying httpx.Client

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._client = client
        return self

    def get_httpx_client(self) -> httpx.Client:
        """Get the underlying httpx.Client, constructing a new one if not previously set"""
        self.refresh_access_token()
        if self._client is None:
            self._headers[self.auth_header_name] = f"{self.prefix} {self.token}" if self.prefix else self.token
            self._client = httpx.Client(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )
        return self._client

    def __enter__(self) -> "AuthenticatedClient":
        """Enter a context manager for self.client—you cannot enter twice (see httpx docs)"""
        self.get_httpx_client().__enter__()
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        """Exit a context manager for internal httpx.Client (see httpx docs)"""
        self.get_httpx_client().__exit__(*args, **kwargs)

    def set_async_httpx_client(self, async_client: httpx.AsyncClient) -> "AuthenticatedClient":
        """Manually the underlying httpx.AsyncClient

        **NOTE**: This will override any other settings on the client, including cookies, headers, and timeout.
        """
        self._async_client = async_client
        return self

    def get_async_httpx_client(self) -> httpx.AsyncClient:
        """Get the underlying httpx.AsyncClient, constructing a new one if not previously set"""
        self.refresh_access_token()
        if self._async_client is None:
            self._headers[self.auth_header_name] = f"{self.prefix} {self.token}" if self.prefix else self.token
            self._async_client = httpx.AsyncClient(
                base_url=self._base_url,
                cookies=self._cookies,
                headers=self._headers,
                timeout=self._timeout,
                verify=self._verify_ssl,
                follow_redirects=self._follow_redirects,
                **self._httpx_args,
            )
        return self._async_client

    def is_token_expired(self):
        """Check if the existing token is expired"""
        current_time = int(time.time())
        return self._auth["id_token_claims"]["exp"] < current_time

    def refresh_access_token(self):
        """If existing token is expired then fetch a new access token using the refresh token"""
        if self._auth and self.is_token_expired():
            scopes = self._auth["scope"]
            self._auth = self._ms_client.acquire_token_by_refresh_token(
                refresh_token=self._auth["refresh_token"], scopes=scopes
            )
            if "access_token" in self._auth:
                self.token = self._auth["access_token"]
                self._auth["scope"] = scopes
                print("Access token refreshed.")
            elif self._auth["id_token_claims"]["idp"] == "google.com":
                self.token = self._auth["id_token"]
                self._auth["scope"] = scopes
                print("Access token refreshed.")
            else:
                print("Invalid Token / Token expired you need to login again")

    async def __aenter__(self) -> "AuthenticatedClient":
        """Enter a context manager for underlying httpx.AsyncClient—you cannot enter twice (see httpx docs)"""
        await self.get_async_httpx_client().__aenter__()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        """Exit a context manager for underlying httpx.AsyncClient (see httpx docs)"""
        await self.get_async_httpx_client().__aexit__(*args, **kwargs)
