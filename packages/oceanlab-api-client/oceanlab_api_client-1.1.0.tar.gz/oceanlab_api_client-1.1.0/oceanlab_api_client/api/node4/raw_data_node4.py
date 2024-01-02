import time
from http import HTTPStatus
from pathlib import Path
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.raw_data_node_4_response_200 import RawDataNode4Response200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    bucket: Union[Unset, None, str] = UNSET,
    range_: Union[Unset, None, str] = UNSET,
    measurement: Union[Unset, None, str] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["bucket"] = bucket

    params["range"] = range_

    params["measurement"] = measurement

    params["filter"] = filter_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/v1/node4/raw-data",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[RawDataNode4Response200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = RawDataNode4Response200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[RawDataNode4Response200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    bucket: Union[Unset, None, str] = UNSET,
    range_: Union[Unset, None, str] = UNSET,
    measurement: Union[Unset, None, str] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
) -> Response[RawDataNode4Response200]:
    """raw-data

    Args:
        bucket (Union[Unset, None, str]):
        range_ (Union[Unset, None, str]):
        measurement (Union[Unset, None, str]):
        filter_ (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RawDataNode4Response200]
    """

    kwargs = _get_kwargs(
        bucket=bucket,
        range_=range_,
        measurement=measurement,
        filter_=filter_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    bucket: Union[Unset, None, str] = UNSET,
    range_: Union[Unset, None, str] = UNSET,
    measurement: Union[Unset, None, str] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
) -> Optional[RawDataNode4Response200]:
    """raw-data

    Args:
        bucket (Union[Unset, None, str]):
        range_ (Union[Unset, None, str]):
        measurement (Union[Unset, None, str]):
        filter_ (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RawDataNode4Response200
    """

    return sync_detailed(
        client=client,
        bucket=bucket,
        range_=range_,
        measurement=measurement,
        filter_=filter_,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    bucket: Union[Unset, None, str] = UNSET,
    range_: Union[Unset, None, str] = UNSET,
    measurement: Union[Unset, None, str] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
) -> Response[RawDataNode4Response200]:
    """raw-data

    Args:
        bucket (Union[Unset, None, str]):
        range_ (Union[Unset, None, str]):
        measurement (Union[Unset, None, str]):
        filter_ (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[RawDataNode4Response200]
    """

    kwargs = _get_kwargs(
        bucket=bucket,
        range_=range_,
        measurement=measurement,
        filter_=filter_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    bucket: Union[Unset, None, str] = UNSET,
    range_: Union[Unset, None, str] = UNSET,
    measurement: Union[Unset, None, str] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
) -> Optional[RawDataNode4Response200]:
    """raw-data

    Args:
        bucket (Union[Unset, None, str]):
        range_ (Union[Unset, None, str]):
        measurement (Union[Unset, None, str]):
        filter_ (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        RawDataNode4Response200
    """

    return (
        await asyncio_detailed(
            client=client,
            bucket=bucket,
            range_=range_,
            measurement=measurement,
            filter_=filter_,
        )
    ).parsed


def sync_to_file(
    *,
    client: Union[AuthenticatedClient, Client],
    bucket: Union[Unset, None, str] = UNSET,
    range_: Union[Unset, None, str] = UNSET,
    measurement: Union[Unset, None, str] = UNSET,
    filter_: Union[Unset, None, str] = UNSET,
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
        bucket=bucket,
        range_=range_,
        measurement=measurement,
        filter_=filter_,
    )

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    full_filename = f"{timestamp}_{filename}.json"
    path = Path(output_directory) / full_filename

    with open(path, "w+") as output_file:
        with client.get_httpx_client().stream(**kwargs) as stream_iterator:
            for text in stream_iterator.iter_text():
                output_file.write(text)

    return full_filename
