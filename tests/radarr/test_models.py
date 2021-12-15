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
    item = QueueItem.from_dict(QUEUE[0])

    assert item.queue_id == 1503378561
    assert item.download_id == "SABnzbd_nzo_Mq2f_b"
    assert item.download_status == "Ok"
    assert item.status == "Downloading"
    assert item.title == "The.Andy.Griffith.Show.S01E01.x264-GROUP"
    assert item.protocol == "usenet"
    assert item.size == 4472186820
    assert item.size_remaining == 0
    assert item.eta == datetime(2016, 2, 5, 22, 46, 52, 440000, tzinfo=timezone.utc)
    assert item.time_remaining == "00:00:00"

    assert item.movie
    assert isinstance(item.movie, Movie)
