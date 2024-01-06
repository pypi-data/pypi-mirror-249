"""Helper functions for pytedee_async."""
from http import HTTPStatus
from typing import Any, Mapping

import aiohttp

from .const import API_URL_DEVICE, TIMEOUT
from .exception import TedeeAuthException, TedeeClientException, TedeeRateLimitException


async def is_personal_key_valid(
    personal_key: str,
    session: aiohttp.ClientSession,
    timeout: int = TIMEOUT,
) -> bool:
    """Check if personal key is valid."""

    try:
        response = await session.get(
            API_URL_DEVICE,
            headers={
                "Content-Type": "application/json",
                "Authorization": "PersonalKey " + personal_key,
            },
            timeout=timeout,
        )
    except (aiohttp.ClientError, aiohttp.ServerConnectionError, TimeoutError):
        return False

    if response.status in (
        HTTPStatus.OK,
        HTTPStatus.CREATED,
        HTTPStatus.ACCEPTED,
    ):
        return True
    return False


async def http_request(
    url: str,
    http_method: str,
    headers: Mapping[str, str] | None,
    session: aiohttp.ClientSession,
    timeout: int = TIMEOUT,
    json_data: Any = None,
) -> Any:
    """HTTP request wrapper."""
    if http_method == "GET":
        method = session.get
    elif http_method == "POST":
        method = session.post
    elif http_method == "PUT":
        method = session.put
    elif http_method == "DELETE":
        method = session.delete
    else:
        raise ValueError(f"Unsupported HTTP method: {http_method}")

    try:
        response = await method(
            url,
            headers=headers,
            json=json_data,
            timeout=timeout,
        )
    except (
        aiohttp.ServerConnectionError,
        aiohttp.ClientError,
        TimeoutError,
    ) as exc:
        raise TedeeClientException(f"Error during http call: {exc}") from exc

    status_code = response.status
    if response.status in (
        HTTPStatus.OK,
        HTTPStatus.CREATED,
        HTTPStatus.ACCEPTED,
    ):
        return await response.json()
    if status_code == HTTPStatus.UNAUTHORIZED:
        raise TedeeAuthException("Authentication failed.")
    if status_code == HTTPStatus.TOO_MANY_REQUESTS:
        raise TedeeRateLimitException("Tedee API Rate Limit.")

    raise TedeeClientException(f"Error during HTTP request. Status code {status_code}")
