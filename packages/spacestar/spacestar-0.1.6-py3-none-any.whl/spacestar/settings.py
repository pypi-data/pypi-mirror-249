from typing import Optional

from ormspace.space_settings import SpaceSettings


class SpaceStarSettings(SpaceSettings):
    session_secret: Optional[str] = None
    csrf_secret: Optional[str] = None