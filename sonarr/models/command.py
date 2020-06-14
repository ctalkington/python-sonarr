"""
https://github.com/Sonarr/Sonarr/wiki/Command
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .base import Base


@dataclass(frozen=True)
class CommandStatusBody(Base):
    """Attribute of CommandStatus."""
    isNewSeries: bool
    sendUpdatesToClient: bool
    updateScheduledTask: bool
    completionMessage: str
    requiresDiskAccess: bool
    isExclusive: bool
    name: str
    trigger: str
    suppressMessages: bool


@dataclass(frozen=True)
class CommandStatus(Base):
    """Sonarr command status.

    Returned by /command.
    """
    name: str
    state: str
    startedOn: datetime
    stateChangeTime: datetime
    sendUpdatesToClient: bool
    id: int
    message: Optional[str] = None
    body: Optional[CommandStatusBody] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    queued: Optional[datetime] = None
    started: Optional[datetime] = None
    trigger: Optional[str] = None
    manual: Optional[bool] = None
    updateScheduledTask: Optional[bool] = None
