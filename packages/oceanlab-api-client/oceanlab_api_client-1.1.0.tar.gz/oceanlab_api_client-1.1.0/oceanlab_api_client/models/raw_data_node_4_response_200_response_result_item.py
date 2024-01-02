import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RawDataNode4Response200ResponseResultItem")


@_attrs_define
class RawDataNode4Response200ResponseResultItem:
    """
    Attributes:
        datetime_ (Union[Unset, datetime.datetime]):
        value (Union[Unset, str]):
        field (Union[Unset, str]):
    """

    datetime_: Union[Unset, datetime.datetime] = UNSET
    value: Union[Unset, str] = UNSET
    field: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        datetime_: Union[Unset, str] = UNSET
        if not isinstance(self.datetime_, Unset):
            datetime_ = self.datetime_.isoformat()

        value = self.value
        field = self.field

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if datetime_ is not UNSET:
            field_dict["datetime"] = datetime_
        if value is not UNSET:
            field_dict["value"] = value
        if field is not UNSET:
            field_dict["field"] = field

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _datetime_ = d.pop("datetime", UNSET)
        datetime_: Union[Unset, datetime.datetime]
        if isinstance(_datetime_, Unset):
            datetime_ = UNSET
        else:
            datetime_ = isoparse(_datetime_)

        value = d.pop("value", UNSET)

        field = d.pop("field", UNSET)

        raw_data_node_4_response_200_response_result_item = cls(
            datetime_=datetime_,
            value=value,
            field=field,
        )

        raw_data_node_4_response_200_response_result_item.additional_properties = d
        return raw_data_node_4_response_200_response_result_item

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
