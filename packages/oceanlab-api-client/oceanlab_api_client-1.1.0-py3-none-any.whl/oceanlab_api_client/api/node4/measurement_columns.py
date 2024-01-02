import time
from http import HTTPStatus
from pathlib import Path
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.measurement_columns_response_200 import MeasurementColumnsResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    bucket: Union[Unset, None, str] = UNSET,
    measurement: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["bucket"] = bucket

    params["measurement"] = measurement

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/v1/node4/measurement-columns",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[MeasurementColumnsResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = MeasurementColumnsResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[MeasurementColumnsResponse200]:
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
    measurement: Union[Unset, None, str] = UNSET,
) -> Response[MeasurementColumnsResponse200]:
    """measurement-columns

    Args:
        bucket (Union[Unset, None, str]):
        measurement (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MeasurementColumnsResponse200]
    """

    kwargs = _get_kwargs(
        bucket=bucket,
        measurement=measurement,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    bucket: Union[Unset, None, str] = UNSET,
    measurement: Union[Unset, None, str] = UNSET,
) -> Optional[MeasurementColumnsResponse200]:
    """measurement-columns

    Args:
        bucket (Union[Unset, None, str]):
        measurement (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MeasurementColumnsResponse200
    """

    return sync_detailed(
        client=client,
        bucket=bucket,
        measurement=measurement,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    bucket: Union[Unset, None, str] = UNSET,
    measurement: Union[Unset, None, str] = UNSET,
) -> Response[MeasurementColumnsResponse200]:
    """measurement-columns

    Args:
        bucket (Union[Unset, None, str]):
        measurement (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MeasurementColumnsResponse200]
    """

    kwargs = _get_kwargs(
        bucket=bucket,
        measurement=measurement,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    bucket: Union[Unset, None, str] = UNSET,
    measurement: Union[Unset, None, str] = UNSET,
) -> Optional[MeasurementColumnsResponse200]:
    """measurement-columns

    Args:
        bucket (Union[Unset, None, str]):
        measurement (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MeasurementColumnsResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            bucket=bucket,
            measurement=measurement,
        )
    ).parsed


def sync_to_file(
    *,
    client: Union[AuthenticatedClient, Client],
    bucket: Union[Unset, None, str] = UNSET,
    measurement: Union[Unset, None, str] = UNSET,
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
        measurement=measurement,
    )

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    full_filename = f"{timestamp}_{filename}.json"
    path = Path(output_directory) / full_filename

    with open(path, "w+") as output_file:
        with client.get_httpx_client().stream(**kwargs) as stream_iterator:
            for text in stream_iterator.iter_text():
                output_file.write(text)

    return full_filename
