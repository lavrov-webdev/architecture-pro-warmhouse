from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CommandRequest(BaseModel):
    deviceId: UUID
    action: str
    parameters: Dict[str, Any] | None = None
    correlationId: UUID


class CommandAccepted(BaseModel):
    commandId: UUID
    correlationId: UUID
    status: Literal["ACCEPTED"] = "ACCEPTED"


class TimedMode(str, Enum):
    ONCE = "ONCE"
    CRON = "CRON"


class TimedCommandCreate(BaseModel):
    mode: TimedMode
    runAt: Optional[str] = None
    cron: Optional[str] = None
    timezone: Optional[str] = Field(default=None, examples=["Europe/Moscow"])
    enabled: bool = True
    command: CommandRequest


class TimedCommand(BaseModel):
    id: UUID
    mode: TimedMode
    runAt: Optional[str] = None
    cron: Optional[str] = None
    timezone: Optional[str] = None
    enabled: bool
    nextRunAt: Optional[str] = None
    command: CommandRequest


class TimedCommandList(BaseModel):
    items: List[TimedCommand]
    page: int
    size: int
    total: int
