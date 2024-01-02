import time
from http import HTTPStatus
from pathlib import Path
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.tags_response_200 import TagsResponse200
from ...types import Response


def _get_kwargs() -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/v1/node3/tags",
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[TagsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = TagsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[TagsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[TagsResponse200]:
    """tags

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TagsResponse200]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[TagsResponse200]:
    """tags

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TagsResponse200
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[TagsResponse200]:
    """tags

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TagsResponse200]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[TagsResponse200]:
    """tags

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TagsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed


def sync_to_file(
    *,
    client: Union[AuthenticatedClient, Client],
    output_directory: Union[Path, str],
    filename: Union[Path, str],
) -> str:
    """Sync results to file.

    This is a custom method for the OceanLab API Python Client.

    Additional args:
        filename (str): A valid filename
        output_directory (Path): The directory to write the output file to

    Returns:
        str: The resulting filename (<timestamp>_<filename>.json)
    """

    kwargs = _get_kwargs()

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    full_filename = f"{timestamp}_{filename}.json"
    path = Path(output_directory) / full_filename

    with open(path, "w+") as output_file:
        with client.get_httpx_client().stream(**kwargs) as stream_iterator:
            for text in stream_iterator.iter_text():
                output_file.write(text)

    return full_filename
