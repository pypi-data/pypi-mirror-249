"""matatika module"""

import abc
import json
from dataclasses import asdict
from typing import Dict


class Resource(abc.ABC):
    """Base class for resource objects"""

    @property
    def version(self) -> str:
        """Resource version identifier"""

    @classmethod
    @property
    @abc.abstractmethod
    def attr_translations(cls) -> Dict[str, str]:
        """Attribution translations to perform when converting a resource to/from a Python object"""

    def to_dict(self, filter_none=True, apply_translations=True):
        """Converts the resource object to a dictionary"""
        dict_repr = asdict(self)

        if apply_translations:
            for attr, translation in self.attr_translations.items():
                dict_repr = {
                    attr if k == translation else k: v for k, v in dict_repr.items()
                }

        if filter_none:
            dict_repr = {k: v for k, v in dict_repr.items() if v is not None}

        return dict_repr

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, resource_dict: dict):
        """Resolves a resource object from a dictionary"""
        resource = cls()

        # apply attribute translations
        resource_dict = {
            cls.attr_translations.get(k, k): v for k, v in resource_dict.items()
        }

        # set version if not delared by the resource object type
        if not cls.version:
            resource.version = resource_dict.get("version")

        return resource, resource_dict

    def to_json_str(self, filter_none=True):
        """Converts the resource object to a JSON string"""
        return json.dumps(self.to_dict(filter_none))
