import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RawDataAllResponse200ResponseResultItem")


@_attrs_define
class RawDataAllResponse200ResponseResultItem:
    """
    Attributes:
        datetime_ (Union[Unset, datetime.datetime]):
        measurement (Union[Unset, str]):
        field (Union[Unset, str]):
        approved (Union[Unset, str]):
        data_level (Union[Unset, str]):
        edge_device (Union[Unset, str]):
        platform (Union[Unset, str]):
        sensor (Union[Unset, str]):
        serial (Union[Unset, str]):
        unit (Union[Unset, str]):
    """

    datetime_: Union[Unset, datetime.datetime] = UNSET
    measurement: Union[Unset, str] = UNSET
    field: Union[Unset, str] = UNSET
    approved: Union[Unset, str] = UNSET
    data_level: Union[Unset, str] = UNSET
    edge_device: Union[Unset, str] = UNSET
    platform: Union[Unset, str] = UNSET
    sensor: Union[Unset, str] = UNSET
    serial: Union[Unset, str] = UNSET
    unit: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        datetime_: Union[Unset, str] = UNSET
        if not isinstance(self.datetime_, Unset):
            datetime_ = self.datetime_.isoformat()

        measurement = self.measurement
        field = self.field
        approved = self.approved
        data_level = self.data_level
        edge_device = self.edge_device
        platform = self.platform
        sensor = self.sensor
        serial = self.serial
        unit = self.unit

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if datetime_ is not UNSET:
            field_dict["datetime"] = datetime_
        if measurement is not UNSET:
            field_dict["measurement"] = measurement
        if field is not UNSET:
            field_dict["field"] = field
        if approved is not UNSET:
            field_dict["approved"] = approved
        if data_level is not UNSET:
            field_dict["data_level"] = data_level
        if edge_device is not UNSET:
            field_dict["edge_device"] = edge_device
        if platform is not UNSET:
            field_dict["platform"] = platform
        if sensor is not UNSET:
            field_dict["sensor"] = sensor
        if serial is not UNSET:
            field_dict["serial"] = serial
        if unit is not UNSET:
            field_dict["unit"] = unit

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

        measurement = d.pop("measurement", UNSET)

        field = d.pop("field", UNSET)

        approved = d.pop("approved", UNSET)

        data_level = d.pop("data_level", UNSET)

        edge_device = d.pop("edge_device", UNSET)

        platform = d.pop("platform", UNSET)

        sensor = d.pop("sensor", UNSET)

        serial = d.pop("serial", UNSET)

        unit = d.pop("unit", UNSET)

        raw_data_all_response_200_response_result_item = cls(
            datetime_=datetime_,
            measurement=measurement,
            field=field,
            approved=approved,
            data_level=data_level,
            edge_device=edge_device,
            platform=platform,
            sensor=sensor,
            serial=serial,
            unit=unit,
        )

        raw_data_all_response_200_response_result_item.additional_properties = d
        return raw_data_all_response_200_response_result_item

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
