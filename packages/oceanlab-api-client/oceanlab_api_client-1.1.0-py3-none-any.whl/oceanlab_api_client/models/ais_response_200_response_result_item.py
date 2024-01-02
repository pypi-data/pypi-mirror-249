import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="AisResponse200ResponseResultItem")


@_attrs_define
class AisResponse200ResponseResultItem:
    """
    Attributes:
        index (Union[Unset, int]):
        mmsi (Union[Unset, int]):
        imo (Union[Unset, int]):
        length (Union[Unset, int]):
        ts (Union[Unset, datetime.datetime]):
        longitude (Union[Unset, float]):
        latitude (Union[Unset, float]):
        sog (Union[Unset, float]):
        cog (Union[Unset, float]):
        true_heading (Union[Unset, int]):
        nav_status (Union[Unset, int]):
        message_nr (Union[Unset, int]):
        point_geom (Union[Unset, str]):
    """

    index: Union[Unset, int] = UNSET
    mmsi: Union[Unset, int] = UNSET
    imo: Union[Unset, int] = UNSET
    length: Union[Unset, int] = UNSET
    ts: Union[Unset, datetime.datetime] = UNSET
    longitude: Union[Unset, float] = UNSET
    latitude: Union[Unset, float] = UNSET
    sog: Union[Unset, float] = UNSET
    cog: Union[Unset, float] = UNSET
    true_heading: Union[Unset, int] = UNSET
    nav_status: Union[Unset, int] = UNSET
    message_nr: Union[Unset, int] = UNSET
    point_geom: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        index = self.index
        mmsi = self.mmsi
        imo = self.imo
        length = self.length
        ts: Union[Unset, str] = UNSET
        if not isinstance(self.ts, Unset):
            ts = self.ts.isoformat()

        longitude = self.longitude
        latitude = self.latitude
        sog = self.sog
        cog = self.cog
        true_heading = self.true_heading
        nav_status = self.nav_status
        message_nr = self.message_nr
        point_geom = self.point_geom

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if index is not UNSET:
            field_dict["index"] = index
        if mmsi is not UNSET:
            field_dict["mmsi"] = mmsi
        if imo is not UNSET:
            field_dict["imo"] = imo
        if length is not UNSET:
            field_dict["length"] = length
        if ts is not UNSET:
            field_dict["ts"] = ts
        if longitude is not UNSET:
            field_dict["longitude"] = longitude
        if latitude is not UNSET:
            field_dict["latitude"] = latitude
        if sog is not UNSET:
            field_dict["sog"] = sog
        if cog is not UNSET:
            field_dict["cog"] = cog
        if true_heading is not UNSET:
            field_dict["true_heading"] = true_heading
        if nav_status is not UNSET:
            field_dict["nav_status"] = nav_status
        if message_nr is not UNSET:
            field_dict["message_nr"] = message_nr
        if point_geom is not UNSET:
            field_dict["point_geom"] = point_geom

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        index = d.pop("index", UNSET)

        mmsi = d.pop("mmsi", UNSET)

        imo = d.pop("imo", UNSET)

        length = d.pop("length", UNSET)

        _ts = d.pop("ts", UNSET)
        ts: Union[Unset, datetime.datetime]
        if isinstance(_ts, Unset):
            ts = UNSET
        else:
            ts = isoparse(_ts)

        longitude = d.pop("longitude", UNSET)

        latitude = d.pop("latitude", UNSET)

        sog = d.pop("sog", UNSET)

        cog = d.pop("cog", UNSET)

        true_heading = d.pop("true_heading", UNSET)

        nav_status = d.pop("nav_status", UNSET)

        message_nr = d.pop("message_nr", UNSET)

        point_geom = d.pop("point_geom", UNSET)

        ais_response_200_response_result_item = cls(
            index=index,
            mmsi=mmsi,
            imo=imo,
            length=length,
            ts=ts,
            longitude=longitude,
            latitude=latitude,
            sog=sog,
            cog=cog,
            true_heading=true_heading,
            nav_status=nav_status,
            message_nr=message_nr,
            point_geom=point_geom,
        )

        ais_response_200_response_result_item.additional_properties = d
        return ais_response_200_response_result_item

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
