"""Tests for Sonarr Models."""
import json
from datetime import datetime, timezone

from radarr.models import QueueItem, Movie, MovieFile
from tests import load_fixture

CALENDAR = json.loads(load_fixture("radarr/calendar.json"))
QUEUE = json.loads(load_fixture("radarr/queue.json"))
MOVIES = json.loads(load_fixture("radarr/movies.json"))


def test_queue_item() -> None:
    """Test the QueueItem model."""
    item = QueueItem.from_dict(QUEUE['records'][0])

    assert item.queue_id == 1065103901
    assert item.download_id == "9ab937f649974510b36245d1d29b67e8"
    assert item.download_status == "ok"
    assert item.status == "downloading"
    assert item.title == "Army.of.Thieves.2021.1080p.WEB-DL.AAC.2.0.x264-Telly"
    assert item.protocol == "usenet"
    assert item.size == 9599909429
    assert item.size_remaining == 8478892583
    assert item.eta == datetime(2021, 12, 15, 12, 0, 39, tzinfo=timezone.utc)
    assert item.time_remaining == "00:08:11"
    assert item.movie_id == 2008
