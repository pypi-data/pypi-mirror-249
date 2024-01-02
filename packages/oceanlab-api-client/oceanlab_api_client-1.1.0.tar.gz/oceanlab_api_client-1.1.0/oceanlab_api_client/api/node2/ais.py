import time
from http import HTTPStatus
from pathlib import Path
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.ais_response_200 import AisResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    from_: Union[Unset, None, str] = UNSET,
    to: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["from"] = from_

    params["to"] = to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/v1/node2/ais",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[AisResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = AisResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AisResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    from_: Union[Unset, None, str] = UNSET,
    to: Union[Unset, None, str] = UNSET,
) -> Response[AisResponse200]:
    """ais

    Args:
        from_ (Union[Unset, None, str]):
        to (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AisResponse200]
    """

    kwargs = _get_kwargs(
        from_=from_,
        to=to,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    from_: Union[Unset, None, str] = UNSET,
    to: Union[Unset, None, str] = UNSET,
) -> Optional[AisResponse200]:
    """ais

    Args:
        from_ (Union[Unset, None, str]):
        to (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AisResponse200
    """

    return sync_detailed(
        client=client,
        from_=from_,
        to=to,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    from_: Union[Unset, None, str] = UNSET,
    to: Union[Unset, None, str] = UNSET,
) -> Response[AisResponse200]:
    """ais

    Args:
        from_ (Union[Unset, None, str]):
        to (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AisResponse200]
    """

    kwargs = _get_kwargs(
        from_=from_,
        to=to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    from_: Union[Unset, None, str] = UNSET,
    to: Union[Unset, None, str] = UNSET,
) -> Optional[AisResponse200]:
    """ais

    Args:
        from_ (Union[Unset, None, str]):
        to (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AisResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            from_=from_,
            to=to,
        )
    ).parsed


def sync_to_file(
    *,
    client: Union[AuthenticatedClient, Client],
    from_: Union[Unset, None, str] = UNSET,
    to: Union[Unset, None, str] = UNSET,
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

    kwargs = _get_kwargs(
        from_=from_,
        to=to,
    )

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    full_filename = f"{timestamp}_{filename}.json"
    path = Path(output_directory) / full_filename

    with open(path, "w+") as output_file:
        with client.get_httpx_client().stream(**kwargs) as stream_iterator:
            for text in stream_iterator.iter_text():
                output_file.write(text)

    return full_filename
