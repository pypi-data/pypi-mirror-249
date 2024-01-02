from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TagsResponse200ResponseResultItem")


@_attrs_define
class TagsResponse200ResponseResultItem:
    """
    Attributes:
        controller (Union[Unset, str]):
        tag (Union[Unset, str]):
        description (Union[Unset, str]):
    """

    controller: Union[Unset, str] = UNSET
    tag: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        controller = self.controller
        tag = self.tag
        description = self.description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if controller is not UNSET:
            field_dict["controller"] = controller
        if tag is not UNSET:
            field_dict["tag"] = tag
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        controller = d.pop("controller", UNSET)

        tag = d.pop("tag", UNSET)

        description = d.pop("description", UNSET)

        tags_response_200_response_result_item = cls(
            controller=controller,
            tag=tag,
            description=description,
        )

        tags_response_200_response_result_item.additional_properties = d
        return tags_response_200_response_result_item

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
