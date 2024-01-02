from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RawDataCountResponse200ResponseResultItem")


@_attrs_define
class RawDataCountResponse200ResponseResultItem:
    """
    Attributes:
        start_time (Union[Unset, str]):
        stop_time (Union[Unset, str]):
        count (Union[Unset, str]):
    """

    start_time: Union[Unset, str] = UNSET
    stop_time: Union[Unset, str] = UNSET
    count: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        start_time = self.start_time
        stop_time = self.stop_time
        count = self.count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if start_time is not UNSET:
            field_dict["startTime"] = start_time
        if stop_time is not UNSET:
            field_dict["stopTime"] = stop_time
        if count is not UNSET:
            field_dict["count"] = count

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        start_time = d.pop("startTime", UNSET)

        stop_time = d.pop("stopTime", UNSET)

        count = d.pop("count", UNSET)

        raw_data_count_response_200_response_result_item = cls(
            start_time=start_time,
            stop_time=stop_time,
            count=count,
        )

        raw_data_count_response_200_response_result_item.additional_properties = d
        return raw_data_count_response_200_response_result_item

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
