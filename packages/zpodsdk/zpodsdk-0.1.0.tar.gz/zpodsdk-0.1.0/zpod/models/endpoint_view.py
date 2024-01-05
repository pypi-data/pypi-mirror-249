from typing import Any, Dict, Type, TypeVar

import attr

T = TypeVar("T", bound="EndpointView")


@attr.s(auto_attribs=True)
class EndpointView:
    """
    Attributes:
        description (str):  Example: current testing env.
        enabled (bool):  Example: True.
        id (str):  Example: 1.
        name (str):  Example: mylab.
    """

    description: str
    enabled: bool
    id: str
    name: str

    def to_dict(self) -> Dict[str, Any]:
        description = self.description
        enabled = self.enabled
        id = self.id
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "description": description,
                "enabled": enabled,
                "id": id,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        description = d.pop("description")

        enabled = d.pop("enabled")

        id = d.pop("id")

        name = d.pop("name")

        endpoint_view = cls(
            description=description,
            enabled=enabled,
            id=id,
            name=name,
        )

        return endpoint_view
