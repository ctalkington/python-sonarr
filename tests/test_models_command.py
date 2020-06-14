"""Tests for sonarr.models.command."""
import json
from datetime import datetime, timezone

import sonarr.models as models

from . import load_fixture

COMMAND = json.loads(load_fixture("command.json"))
UTC = timezone.utc


def test_command_status_body() -> None:
    """Test the CommandStatusBody model."""
    item0 = models.CommandStatus.from_dict(COMMAND[0])
    body0 = item0.body
    assert body0.isNewSeries is False
    assert body0.sendUpdatesToClient is True
    assert body0.updateScheduledTask is True
    assert body0.completionMessage == "Completed"
    assert body0.requiresDiskAccess is False
    assert body0.isExclusive is False
    assert body0.name == "RefreshSeries"
    assert body0.trigger == "manual"
    assert body0.suppressMessages is False


def test_command_status() -> None:
    """Test the CommandStatus model."""
    item0 = models.CommandStatus.from_dict(COMMAND[0])
    assert item0
    assert item0.name == "RefreshSeries"
    assert isinstance(item0.body, models.CommandStatusBody)  # tested in test_command_status_body()
    assert item0.priority == "normal"
    assert item0.status == "started"
    assert item0.queued == datetime(2020, 4, 6, 16, 54, 6, 419450, tzinfo=UTC)
    assert item0.started == datetime(2020, 4, 6, 16, 54, 6, 421322, tzinfo=UTC)
    assert item0.trigger == "manual"
    assert item0.state == "started"
    assert item0.manual is True
    assert item0.startedOn == datetime(2020, 4, 6, 16, 54, 6, 419450, tzinfo=UTC)
    assert item0.stateChangeTime == datetime(2020, 4, 6, 16, 54, 6, 421322, tzinfo=UTC)
    assert item0.sendUpdatesToClient is True
    assert item0.updateScheduledTask is True
    assert item0.id == 368621

    item1 = models.CommandStatus.from_dict(COMMAND[1])
    assert item1
    assert item1.name == "RefreshSeries"
    assert item1.body is None
    assert item1.priority is None
    assert item1.status is None
    assert item1.queued is None
    assert item1.started is None
    assert item1.trigger is None
    assert item1.state == "started"
    assert item1.manual is None
    assert item1.startedOn == datetime(2020, 4, 6, 16, 57, 51, 406504, tzinfo=UTC)
    assert item1.stateChangeTime == datetime(2020, 4, 6, 16, 57, 51, 417931, tzinfo=UTC)
    assert item1.sendUpdatesToClient is True
    assert item1.updateScheduledTask is None
    assert item1.id == 368629
