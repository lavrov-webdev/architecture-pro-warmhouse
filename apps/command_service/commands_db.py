from __future__ import annotations
from typing import Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from models import (
    CommandAccepted,
    CommandRequest,
    TimedCommand,
    TimedCommandCreate,
    TimedMode,
)


class CommandsDb:
    def __init__(self) -> None:
        self.idempotency_key_to_command: Dict[str, CommandAccepted] = {}
        self.commands_by_id: Dict[UUID, CommandRequest] = {}
        self.timed_commands: List[TimedCommand] = []

    # Commands
    def add_command(
        self, *, command: CommandRequest, idempotency_key: Optional[str] = None
    ) -> Tuple[Optional[CommandAccepted], bool]:
        if idempotency_key:
            existing = self.idempotency_key_to_command.get(idempotency_key)
            if existing is not None:
                return existing, True

        command_id = uuid4()
        accepted = CommandAccepted(
            commandId=command_id, correlationId=command.correlationId
        )
        self.commands_by_id[command_id] = command
        if idempotency_key:
            self.idempotency_key_to_command[idempotency_key] = accepted
        return accepted, False

    # Timed commands
    def add_timed_command(self, *, request: TimedCommandCreate) -> TimedCommand:
        timed_id = uuid4()

        next_run_at: Optional[str] = None
        if request.mode == TimedMode.ONCE and request.runAt:
            next_run_at = request.runAt

        timed = TimedCommand(
            id=timed_id,
            mode=request.mode,
            runAt=request.runAt,
            cron=request.cron,
            timezone=request.timezone,
            enabled=request.enabled,
            nextRunAt=next_run_at,
            command=request.command,
        )
        self.timed_commands.append(timed)
        return timed

    def list_timed_commands(
        self,
        *,
        mode: Optional[TimedMode] = None,
        enabled: Optional[bool] = None,
        page: int = 1,
        size: int = 50,
    ) -> Dict[str, object]:
        filtered = self.timed_commands
        if mode is not None:
            filtered = [c for c in filtered if c.mode == mode]
        if enabled is not None:
            filtered = [c for c in filtered if c.enabled == enabled]

        total = len(filtered)
        start = (page - 1) * size
        end = start + size
        items = filtered[start:end]

        return {
            "items": items,
            "page": page,
            "size": size,
            "total": total,
        }
