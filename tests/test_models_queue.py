"""Tests for sonarr.models.queue."""
import json
from datetime import datetime, timezone, timedelta

import sonarr.models as models

from . import load_fixture

QUEUE = json.loads(load_fixture("queue.json"))
UTC = timezone.utc


def test_queue_item() -> None:
    """Test the QueueItem model."""
    item = models.QueueItem.from_dict(QUEUE[0])
    # Tested in test_model_series.test_series()
    assert isinstance(item.series, models.Series)
    # Tested in test_model_episode.test_episode()
    assert isinstance(item.episode, models.Episode)
    # Tested in test_model_quality.test_qulity_revision()
    assert isinstance(item.quality, models.QualityRevision)
    assert item.size == 4472186820
    assert item.title == "The.Andy.Griffith.Show.S01E01.x264-GROUP"
    assert item.sizeleft == 0
    assert item.timeleft == timedelta(0)
    assert item.estimatedCompletionTime == datetime(2016, 2, 5, 22, 46, 52, 440104, tzinfo=UTC)
    assert item.status == "Downloading"
    assert item.trackedDownloadStatus == "Ok"
    assert item.statusMessages == ()
    assert item.downloadId == "SABnzbd_nzo_Mq2f_b"
    assert item.protocol == "usenet"
    assert item.id == 1503378561
