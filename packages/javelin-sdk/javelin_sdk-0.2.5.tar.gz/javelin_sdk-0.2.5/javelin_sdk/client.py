from enum import Enum, auto
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx

from javelin_sdk.exceptions import (
    InternalServerError,
    NetworkError,
    RateLimitExceededError,
    RouteAlreadyExistsError,
    RouteNotFoundError,
    UnauthorizedError,
    BadRequest,
)
from javelin_sdk.models import QueryResponse, Route, Routes

API_BASEURL = "https://api.javelin.live"
API_BASE_PATH = "/v1"
API_TIMEOUT = 10


def log_request(request):
    print(f"Request URL: {request.url}")
    print(f"Request Method: {request.method}")
    print(f"Request Headers: {request.headers}")
    if request.content:
        print(f"Request Body: {request.content.decode()}")


def log_response(response):
    # Ensure the response content is read for streaming responses
    if hasattr(response, 'is_stream_consumed') and not response.is_stream_consumed:
        response.read()

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    if response.content:
        print(f"Response Body: {response.content.decode()}")

class HttpMethod(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()


class JavelinClient:
    def __init__(
        self,
        javelin_api_key: str,
        base_url: str = API_BASEURL,
        javelin_virtualapikey: Optional[str] = None,
        llm_api_key: Optional[str] = None,
    ) -> None:
        """
        Initialize the JavelinClient.

        :param base_url: Base URL for the Javelin API.
        :param api_key: API key for authorization (if required).
        """
        headers = {}
        if not javelin_api_key or javelin_api_key == "":
            raise UnauthorizedError(
                response=None, message=
                "Please provide a valid Javelin API Key. "
                + "When you sign into Javelin, you can find your API Key in the "
                + "Account->Developer settings"
            )

        headers["x-api-key"] = javelin_api_key

        if javelin_virtualapikey:
            headers["x-javelin-virtualapikey"] = javelin_virtualapikey

        if llm_api_key:
            headers["Authorization"] = f"Bearer {llm_api_key}"

        self.base_url = urljoin(base_url, API_BASE_PATH)
        self._headers = headers
        self._client = None
        self._aclient = None

    @property
    def client(self):
        if self._client is None:
            self._client = httpx.Client(
                #               base_url=self.base_url, headers=self._headers, timeout=API_TIMEOUT,
                # event_hooks={"request": [log_request], "response": [log_response]},
                base_url=self.base_url,
                headers=self._headers,
                timeout=API_TIMEOUT,
            )
        return self._client

    @property
    def aclient(self):
        if self._aclient is None:
            self._aclient = httpx.AsyncClient(
                base_url=self.base_url, headers=self._headers, timeout=API_TIMEOUT
            )
        return self._aclient

    async def __aenter__(self) -> "JavelinClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.aclose()

    def __enter__(self) -> "JavelinClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    async def aclose(self):
        if self._aclient:
            await self._aclient.aclose()

    def close(self):
        if self._client:
            self._client.close()

    def _send_request_sync(
        self,
        method: HttpMethod,
        route_name: Optional[str] = "",
        is_query: bool = False,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """
        Send a request to the Javelin API.

        :param method: HTTP method to use.
        :param route_name: Name of the route to send the request to.
        :param is_query: Whether the route is a query route.
        :param data: Data to send with the request.
        :param headers: Additional headers to send with the request.
        :return: Response from the Javelin API.

        :raises ValueError: If an unsupported HTTP method is used.
        :raises NetworkError: If a network error occurs.

        :raises InternalServerError: If the Javelin API returns a 500 error.
        :raises RateLimitExceededError: If the Javelin API returns a 429 error.
        :raises RouteAlreadyExistsError: If the Javelin API returns a 409 error.
        :raises RouteNotFoundError: If the Javelin API returns a 404 error.
        :raises UnauthorizedError: If the Javelin API returns a 401 error.

        """
        url = self._construct_url(route_name, query=is_query)
        client = self.client

        # Merging additional headers with default headers
        request_headers = {**self._headers, **(headers or {})}
        if is_query and route_name:
            request_headers["x-javelin-route"] = route_name

        try:
            if method == HttpMethod.GET:
                response = client.get(url, headers=request_headers)
            elif method == HttpMethod.POST:
                response = client.post(url, json=data, headers=request_headers)
            elif method == HttpMethod.PUT:
                response = client.put(url, json=data, headers=request_headers)
            elif method == HttpMethod.DELETE:
                response = client.delete(url, headers=request_headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            return response
        except httpx.NetworkError as e:
            raise NetworkError(message=str(e))

    async def _send_request_async(
        self,
        method: HttpMethod,
        route_name: Optional[str] = "",
        is_query: bool = False,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        """
        Send a request asynchronously to the Javelin API.

        :param method: HTTP method to use.
        :param route_name: Name of the route to send the request to.
        :param is_query: Whether the route is a query route.
        :param data: Data to send with the request.
        :param headers: Additional headers to send with the request.
        :return: Response from the Javelin API.

        :raises ValueError: If an unsupported HTTP method is used.
        :raises NetworkError: If a network error occurs.

        :raises InternalServerError: If the Javelin API returns a 500 error.
        :raises RateLimitExceededError: If the Javelin API returns a 429 error.
        :raises RouteAlreadyExistsError: If the Javelin API returns a 409 error.
        :raises RouteNotFoundError: If the Javelin API returns a 404 error.
        :raises UnauthorizedError: If the Javelin API returns a 401 error.

        """
        url = self._construct_url(route_name, query=is_query)
        aclient = self.aclient

        # Merging additional headers with default headers
        request_headers = {**self._headers, **(headers or {})}
        if is_query and route_name:
            request_headers["x-javelin-route"] = route_name

        try:
            if method == HttpMethod.GET:
                response = await aclient.get(url, headers=request_headers)
            elif method == HttpMethod.POST:
                response = await aclient.post(url, json=data, headers=request_headers)
            elif method == HttpMethod.PUT:
                response = await aclient.put(url, json=data, headers=request_headers)
            elif method == HttpMethod.DELETE:
                response = await aclient.delete(url, headers=request_headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            return response
        except httpx.NetworkError as e:
            raise NetworkError(message=str(e))

    def _process_response_ok(self, response: httpx.Response) -> str:
        """
        Process a successful response from the Javelin API.
        """
        self._handle_response(response)
        return response.text

    def _process_response_json(self, response: httpx.Response) -> QueryResponse:
        """
        Process a successful response from the Javelin API.
        Parse body into a QueryResponse object and return it.
        This is for Query() requests.
        """
        self._handle_response(response)
        return QueryResponse(**response.json())

    def _process_response_route(self, response: httpx.Response) -> Route:
        """
        Process a successful response from the Javelin API.
        Parse body into a Route object and return it.
        This is for Get() requests.
        """
        self._handle_response(response)
        return Route(**response.json())

    def _handle_response(self, response: httpx.Response) -> None:
        """
        Handle the API response by raising appropriate exceptions based on the
        response status code.

        :param response: The API response to handle.
        """
        if response.status_code == 400:
            raise BadRequest(response=response)
        elif response.status_code == 409:
            raise RouteAlreadyExistsError(response=response)
        elif response.status_code == 401:
            raise UnauthorizedError(response=response)
        elif response.status_code == 403:
            raise UnauthorizedError(response=response)
        elif response.status_code == 404:
            raise RouteNotFoundError(response=response)
        elif response.status_code == 409:
            raise RouteAlreadyExistsError(response=response)
        elif response.status_code == 429:
            raise RateLimitExceededError(response=response)
        elif response.status_code != 200:
            raise InternalServerError(response=response)

    def _construct_url(
        self, route_name: Optional[str] = "", query: bool = False
    ) -> str:
        """
        Construct the complete URL for a given route name and action.

        :param route_name: Name of the route.
        :param query: If True, add "query" to the end of the URL.
        :return: Constructed URL.
        """
        url_parts = [self.base_url]
        if query:
            url_parts.append("query")
            if route_name is not None:  # Check if route_name is not None
                url_parts.append(route_name)
        elif route_name:
            url_parts.append("admin")
            url_parts.append("routes")
            url_parts.append(route_name)
        else:
            url_parts.append("admin")
            url_parts.append("routes")
        return "/".join(url_parts)

    def get_route(self, route_name: str) -> Route:
        """
        Retrieve details of a specific route.

        :param route_name: Name of the route to retrieve.
        :return: Response object containing route details.
        """
        self._validate_route_name(route_name)
        response = self._send_request_sync(HttpMethod.GET, route_name)
        return self._process_response_route(response)

    async def aget_route(self, route_name: str) -> Route:
        """
        Asynchronously retrieve details of a specific route.

        :param route_name: Name of the route to retrieve.
        :return: Response object containing route details.
        """
        self._validate_route_name(route_name)
        response = await self._send_request_async(HttpMethod.GET, route_name)
        return self._process_response_route(response)

    # create a route
    def create_route(self, route: Route) -> str:
        """
        Create a new route.

        :param route: Route object containing route details.
        :return: Response text indicating the success status (e.g., "OK").
        """
        self._validate_route_name(route.name)
        response = self._send_request_sync(
            HttpMethod.POST, route.name, data=route.dict()
        )
        return self._process_response_ok(response)

    # async create a route
    async def acreate_route(self, route: Route) -> str:
        """
        Asynchronously create a new route.

        :param route: Route object containing route details.
        :return: Response text indicating the success status (e.g., "OK").
        """
        self._validate_route_name(route.name)
        response = await self._send_request_async(
            HttpMethod.POST, route.name, data=route.dict()
        )
        return self._process_response_ok(response)

    # update a route
    def update_route(self, route: Route) -> str:
        """
        Update an existing route.

        :param route_name: Name of the route to update.
        :param route: Route object containing updated route details.
        :return: Response text indicating the success status (e.g., "OK").
        """
        self._validate_route_name(route.name)
        response = self._send_request_sync(
            HttpMethod.PUT, route.name, data=route.dict()
        )
        return self._process_response_ok(response)

    # async update a route
    async def aupdate_route(self, route: Route) -> str:
        """
        Asynchronously update an existing route.

        :param route_name: Name of the route to update.
        :param route: Route object containing updated route details.
        :return: Response text indicating the success status (e.g., "OK").
        """
        self._validate_route_name(route.name)
        response = await self._send_request_async(
            HttpMethod.PUT, route.name, data=route.dict()
        )
        return self._process_response_ok(response)

    # list routes
    def list_routes(self) -> Routes:
        """
        Retrieve a list of all routes.

        :return: Routes object containing a list of all routes.
        """
        response = self._send_request_sync(HttpMethod.GET, "")
        return Routes(routes=response.json())

    # async list routes
    async def alist_routes(self) -> Routes:
        """
        Asynchronously retrieve a list of all routes.

        :return: Routes object containing a list of all routes.
        """
        response = await self._send_request_async(HttpMethod.GET, "")
        return Routes(routes=response.json())

    # query an LLM through a route
    def query_route(
        self,
        route_name: str,
        query_body: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> QueryResponse:
        """
        Query an LLM through a specific route.

        :param route_name: Name of the route to query.
        :param query_body: QueryBody object containing the query details.
        :param headers: Additional headers to send with the request.
        :return: Response object containing query results.
        """
        self._validate_route_name(route_name)
        response = self._send_request_sync(
            HttpMethod.POST, route_name, is_query=True, data=query_body, headers=headers
        )
        return self._process_response_json(response)

    # async query an LLM through a route
    async def aquery_route(
        self,
        route_name: str,
        query_body: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> QueryResponse:
        """
        Asynchronously query an LLM through a specific route.

        :param route_name: Name of the route to query.
        :param query_body: QueryBody object containing the query details.
        :param headers: Additional headers to send with the request.
        :return: Response object containing query results.
        """
        self._validate_route_name(route_name)
        response = await self._send_request_async(
            HttpMethod.POST, route_name, is_query=True, data=query_body, headers=headers
        )
        return self._process_response_json(response)

    # delete a route
    def delete_route(self, route_name: str) -> str:
        """
        Delete a specific route.

        :param route_name: Name of the route to delete.
        :return: Response text indicating the success status (e.g., "OK").
        """
        self._validate_route_name(route_name)
        response = self._send_request_sync(HttpMethod.DELETE, route_name)
        return self._process_response_ok(response)

    # async delete a route
    async def adelete_route(self, route_name: str) -> str:
        """
        Asynchronously delete a specific route.

        :param route_name: Name of the route to delete.
        :return: Response text indicating the success status (e.g., "OK").
        """
        self._validate_route_name(route_name)
        response = await self._send_request_async(HttpMethod.DELETE, route_name)
        return self._process_response_ok(response)

    @staticmethod
    def _validate_route_name(route_name: str):
        """
        Validate the route name. Raises a ValueError if the route name is empty.

        :param route_name: Name of the route to validate.
        """
        if not route_name:
            raise ValueError("Route name cannot be empty.")

    @staticmethod
    def _validate_body(body: Optional[Dict[str, Any]]):
        """
        Validate the request body. Raises a ValueError if the body is empty.

        :param body: Request body to validate.
        """
        if not body:
            raise ValueError("Body cannot be empty.")
