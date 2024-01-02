import datetime as dt
from typing import Literal, Optional, Union

import pydantic
from pydantic import ConfigDict

from ..utils import File


def to_camel(snake_str: str) -> str:
    first, *others = snake_str.split("_")
    ret = "".join([first.lower(), *map(str.title, others)])
    return ret


class BaseAPIModel(pydantic.BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, alias_generator=to_camel, populate_by_name=True
    )

    def model_dump(self, **kwargs):
        """Returns camelCased version and removes any non specified optional fields"""
        return super().model_dump(by_alias=True, exclude_unset=True)


class PatchAssetInput(BaseAPIModel):
    category: Optional[str] = None
    code: Optional[str] = None
    photo: Union[File, str, None] = None
    make: Optional[str] = None
    model: Optional[str] = None
    size: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    condition: Optional[str] = None
    installation_timestamp: Optional[dt.datetime] = None
    expected_life_years: Optional[dt.datetime] = None


class PatchRemarkInput(BaseAPIModel):
    resolved_timestamp: Optional[dt.datetime] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    resolution: Optional[str] = None


class PatchServiceInput(BaseAPIModel):
    name: Optional[str] = None
    due_date: Optional[dt.date] = None
    performed_timestamp: Optional[dt.datetime] = None
    description: Optional[str] = None
    result: Optional[str] = None


class PatchTenantDocumentInput(BaseAPIModel):
    title: Optional[str] = None


class PushContractorInput(BaseAPIModel):
    name: str
    website: Optional[str] = None
    about_us: Optional[str] = None
    industries: list[
        Literal["FIRE", "SECURITY", "MECHANICAL", "ELECTRICAL", "PLUMBING", "ELEVATORS"]
    ]
    services_provided: list[
        Literal[
            "INSPECTION_AND_TESTING",
            "REPAIRS",
            "MAJOR_WORKS",
            "ESM_AUDITING",
            "ANNUAL_CERTIFICATION",
        ]
    ]
    service_areas: Optional[str] = None
    country: Literal["AU", "NZ", "GB", "CA", "US"]
    business_number: str
    address: str
    email: str
    phone: str
    is_active: Optional[bool] = True
    logo: Optional[File] = None
