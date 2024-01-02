from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.measurement_columns_response_200_response import MeasurementColumnsResponse200Response


T = TypeVar("T", bound="MeasurementColumnsResponse200")


@_attrs_define
class MeasurementColumnsResponse200:
    """
    Attributes:
        response (Union[Unset, MeasurementColumnsResponse200Response]):
    """

    response: Union[Unset, "MeasurementColumnsResponse200Response"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        response: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.response, Unset):
            response = self.response.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if response is not UNSET:
            field_dict["response"] = response

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.measurement_columns_response_200_response import MeasurementColumnsResponse200Response

        d = src_dict.copy()
        _response = d.pop("response", UNSET)
        response: Union[Unset, MeasurementColumnsResponse200Response]
        if isinstance(_response, Unset):
            response = UNSET
        else:
            response = MeasurementColumnsResponse200Response.from_dict(_response)

        measurement_columns_response_200 = cls(
            response=response,
        )

        measurement_columns_response_200.additional_properties = d
        return measurement_columns_response_200

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
