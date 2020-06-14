"""Tests for sonarr.models.release."""
import json
from datetime import datetime, timezone

import sonarr.models as models

from . import load_fixture

RELEASE = json.loads(load_fixture("release.json"))
UTC = timezone.utc


def test_release() -> None:
    """Test the Release model."""
    # instance returned by /release
    rel = models.Release.from_dict(RELEASE[0])
    assert rel.guid == "a5a4a6a7-f7c9-4ff0-b3c4-b8dea9ed965b"
    # tested in test_models_quality.test_quality_proper()
    assert isinstance(rel.quality, models.QualityProper)
    assert rel.age == 0
    assert rel.size == 0
    assert rel.indexerId == 5
    assert rel.indexer == "Wombles"
    assert rel.releaseGroup == "YesTV"
    assert rel.title == "The.Devils.Ride.S03E01.720p.HDTV.x264-YesTV"
    assert rel.fullSeason is False
    assert rel.sceneSource is False
    assert rel.seasonNumber == 3
    assert rel.language == "english"
    assert rel.seriesTitle == "devilsride"
    assert rel.episodeNumbers == (1, )
    assert rel.approved is False
    assert rel.tvRageId == 0
    assert rel.rejections == ("Unknown Series", )
    assert rel.publishDate == datetime(2014, 2, 10, tzinfo=UTC)
    assert rel.downloadUrl == (
        "http://www.newshost.co.za/nzb/5a6/"
        "The.Devils.Ride.S03E01.720p.HDTV.x264-YesTV.nzb"
    )
    assert rel.downloadAllowed is True
