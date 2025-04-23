from datetime import datetime
from enum import Enum
from typing import (
    List,
    Optional,
)
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class PagingSettings(BaseModel):
    posts_per_page: Optional[int] = Field(None, alias='postsPerPage')
    comments_per_page: Optional[int] = Field(None, alias='commentsPerPage')
    topics_per_page: Optional[int] = Field(None, alias='topicsPerPage')
    messages_per_page: Optional[int] = Field(None, alias='messagesPerPage')
    entities_per_page: Optional[int] = Field(None, alias='entitiesPerPage')


class ColorSchema(str, Enum):
    MODERN = "Modern"
    PALE = "Pale"
    CLASSIC = "Classic"
    CLASSIC_PALE = "ClassicPale"
    NIGHT = "Night"


class UserSettings(BaseModel):
    color_schema: ColorSchema = Field(None)
    nanny_greetings_message: str = Field(None, alias='nannyGreetingsMessage')
    paging: PagingSettings


class UserRole(str, Enum):
    GUEST = "Guest"
    PLAYER = "Player"
    ADMINISTRATOR = "Administrator"
    NANNY_MODERATOR = "NannyModerator"
    REGULAR_MODERATOR = "RegularModerator"
    SENIOR_MODERATOR = "SeniorModerator"


class UserDetails(BaseModel):
    login: str
    roles: List[UserRole]
    medium_picture_url: str = Field(None, alias='mediumPictureUrl')
    small_picture_url: str = Field(None, alias='smallPictureUrl')
    status: str = Field(None)
    rating: Rating
    online: datetime = Field(None)
    name: str = Field(None)
    location: str = Field(None)
    registration: datetime = Field(None)
    icq: str = Field(None)
    skype: str = Field(None)
    original_picture_url: str = Field(None, alias='originalPictureUrl')
    info: str = Field(None)
    settings: UserSettings = Field(None)


class UserDetailsEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    resource: Optional[UserDetails] = None
    metadata: Optional[str] = None
