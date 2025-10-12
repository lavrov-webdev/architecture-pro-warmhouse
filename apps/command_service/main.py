from typing import Optional
from fastapi import FastAPI, Header, HTTPException, Response, status
from commands_db import CommandsDb
from models import (
    CommandAccepted,
    CommandRequest,
    TimedCommand,
    TimedCommandCreate,
    TimedCommandList,
    TimedMode,
)

app = FastAPI()
db = CommandsDb()


@app.post(
    "/commands",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=CommandAccepted,
)
def create_command(
    command: CommandRequest,
    response: Response,
    idempotency_key: Optional[str] = Header(default=None, alias="Idempotency-Key"),
):
    accepted, duplicate = db.add_command(command=command, idempotency_key=idempotency_key)
    if duplicate:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Duplicate request")
    response.headers["Location"] = f"/commands/{accepted.commandId}"
    return accepted


@app.post(
    "/timed-commands",
    status_code=status.HTTP_201_CREATED,
    response_model=TimedCommand,
)
def create_timed_command(request: TimedCommandCreate, response: Response):
    created = db.add_timed_command(request=request)
    response.headers["Location"] = f"/timed-commands/{created.id}"
    return created


@app.get(
    "/timed-commands",
    response_model=TimedCommandList,
)
def list_timed_commands(
    mode: Optional[TimedMode] = None,
    enabled: Optional[bool] = None,
    page: int = 1,
    size: int = 50,
):
    return db.list_timed_commands(mode=mode, enabled=enabled, page=page, size=size)
