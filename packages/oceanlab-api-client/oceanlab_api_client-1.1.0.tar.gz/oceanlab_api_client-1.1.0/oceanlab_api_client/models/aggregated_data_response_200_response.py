from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.aggregated_data_response_200_response_result_item import AggregatedDataResponse200ResponseResultItem
    from ..models.aggregated_data_response_200_response_status_item import AggregatedDataResponse200ResponseStatusItem


T = TypeVar("T", bound="AggregatedDataResponse200Response")


@_attrs_define
class AggregatedDataResponse200Response:
    """
    Attributes:
        status (Union[Unset, List['AggregatedDataResponse200ResponseStatusItem']]):
        result (Union[Unset, List['AggregatedDataResponse200ResponseResultItem']]):
    """

    status: Union[Unset, List["AggregatedDataResponse200ResponseStatusItem"]] = UNSET
    result: Union[Unset, List["AggregatedDataResponse200ResponseResultItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.status, Unset):
            status = []
            for status_item_data in self.status:
                status_item = status_item_data.to_dict()

                status.append(status_item)

        result: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.result, Unset):
            result = []
            for result_item_data in self.result:
                result_item = result_item_data.to_dict()

                result.append(result_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status
        if result is not UNSET:
            field_dict["result"] = result

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.aggregated_data_response_200_response_result_item import (
            AggregatedDataResponse200ResponseResultItem,
        )
        from ..models.aggregated_data_response_200_response_status_item import (
            AggregatedDataResponse200ResponseStatusItem,
        )

        d = src_dict.copy()
        status = []
        _status = d.pop("status", UNSET)
        for status_item_data in _status or []:
            status_item = AggregatedDataResponse200ResponseStatusItem.from_dict(status_item_data)

            status.append(status_item)

        result = []
        _result = d.pop("result", UNSET)
        for result_item_data in _result or []:
            result_item = AggregatedDataResponse200ResponseResultItem.from_dict(result_item_data)

            result.append(result_item)

        aggregated_data_response_200_response = cls(
            status=status,
            result=result,
        )

        aggregated_data_response_200_response.additional_properties = d
        return aggregated_data_response_200_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
