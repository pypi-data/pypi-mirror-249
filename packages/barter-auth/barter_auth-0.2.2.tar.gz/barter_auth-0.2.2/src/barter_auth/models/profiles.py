from dataclasses import asdict, dataclass, field
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ..constants import Role


class Advertiser(BaseModel):
    class Config:
        # pydantic.config.BaseConfig
        frozen = True

    uuid: UUID
    id: int
    profile_id: int
    profile_uuid: UUID


    moderate: int
    premoderate_booking: bool

    created_at: datetime
    updated_at: datetime

    company_name: str | None = ''
    name: str | None = ''
    email: str | None = ''
    phone: str | None = ''
    whatsapp: str | None = ''
    telegram: str | None = ''
    note: str | None = ''
    weblink: str | None = ''
    instagram: str | None = ''

    balance_reach: int | None = None
    balance_reach_all: int | None = None
    description: str | None = ''
    group_payer_id: int | None = None


class Category(BaseModel):
    class Config:
        frozen = True

    id: int
    type: int
    name: str
    parent_id: int | None = None



class Instagram(BaseModel):
    class Config:
        frozen = True

    uuid: UUID
    id: int
    profile_id: int
    profile_uuid: UUID

    created_at: datetime
    updated_at: datetime

    is_private: bool | None = False
    is_verified: bool | None = False
    checked_at: datetime | None = None

    reach: int | None = None
    followers: int | None = 0
    username: str | None = ''
    post_reach: int | None = None
    booking_limit: int | None = None
    picture: str | None = ''
    pkid: str | None = ''
    categories: list[Category] = []

    count_media: int | None = 0
    full_name: str | None = ''
    external_url: str | None = ''
    phone: str | None = ''

    firstname: str | None = ''
    age: int | None = None
    city: str | None = None


class TestM(BaseModel):
    class Config:
        frozen = True

    id: int
    categories: list[Category] = []

class AnonymousProfile(BaseModel):
    class Config:
        frozen = True

    uuid: UUID = None
    user_id: int | None = None
    role: int = Role.ANONYMOUS
    advertiser: Advertiser | None = None
    instagram: Instagram | None = None

    def __str__(self):
        return "AnonymousProfile"

    def is_blogger(self):
        return False

    def is_advertiser(self):
        return False

class Profile(BaseModel):
    class Config:
        frozen = True

    id: int
    uuid: UUID
    user_id: int

    role: int

    advertiser: Advertiser | None = None
    instagram: Instagram | None = None

    def __post_init__(self):
        if self.role == Role.ADVERTISER and not self.advertiser:
            raise ValueError('Advertiser must be set')
        elif self.role == Role.INSTAGRAM and not self.instagram:
            raise ValueError('Instagram must be set')

    def is_blogger(self):
        return self.role == Role.INSTAGRAM

    def is_advertiser(self):
        return self.role == Role.ADVERTISER


__all__ = [
    'Profile', 'AnonymousProfile',
]