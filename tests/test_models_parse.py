"""Tests for sonarr.models.parse."""
import json

import sonarr.models as models

from . import load_fixture

PARSE = json.loads(load_fixture("parse.json"))


def test_series_title_info() -> None:
    """Test the SeriesTitleInfo model."""
    # instance returned by /parse
    parsed = models.ParseResult.from_dict(PARSE)
    info = parsed.parsedEpisodeInfo.seriesTitleInfo
    assert info.title == "Series Title"
    assert info.titleWithoutYear == "Series Title"
    assert info.year == 0


def test_parsed_episode_info() -> None:
    """Test the ParsedEpisodeInfo model."""
    # instance returned by /parse
    parsed = models.ParseResult.from_dict(PARSE)
    info = parsed.parsedEpisodeInfo
    assert info.releaseTitle == "Series.Title.S01E01.720p.HDTV-Sonarr"
    assert info.seriesTitle == "Series Title"
    # tested in test_models_quality.test_quality_revision()
    assert isinstance(info.quality, models.QualityRevision)
    assert info.seasonNumber == 1
    assert info.episodeNumbers == (1, )
    assert info.absoluteEpisodeNumbers == ()
    assert info.language == "english"
    assert info.fullSeason is False
    assert info.special is False
    assert info.releaseGroup == "Sonarr"
    assert info.releaseHash == ""
    assert info.isDaily is False
    assert info.isAbsoluteNumbering is False
    assert info.isPossibleSpecialEpisode is False


def test_parse_result() -> None:
    """Test the ParseResult model."""
    # instance returned by /parse
    parsed = models.ParseResult.from_dict(PARSE)
    assert parsed.title == "Series.Title.S01E01.720p.HDTV-Sonarr"
    assert parsed.series is None
    assert parsed.episodes == ()
