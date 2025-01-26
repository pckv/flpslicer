from dataclasses import dataclass
from pathlib import Path, PosixPath

import pyflp
from pyflp.project import Project
from pyflp.arrangement import ChannelPLItem, Arrangement
from pyflp.channel import Sampler

from .core import Sample, TrackSample


@dataclass
class FlpArrangement:
    iid: int
    name: str


@dataclass
class FlpTrack:
    iid: int
    name: str


@dataclass
class FlpSlicerResult:
    arrangements: list[FlpArrangement]
    selected_arrangement: int
    arrangement_tracks: list[FlpTrack]
    selected_tracks: list[int]
    samples: list[Sample]
    track_samples: list[TrackSample]


def get_flp_slices(
        flp_path: str | Path, 
        *, 
        samples_dir: str | Path | None = None,
        arrangement: int | None = None,
        tracks: list[int] | None = None,
    ) -> FlpSlicerResult:
    project = pyflp.parse(flp_path)
    arrangement = _get_arrangement(project, arrangement)
    tracks = _get_tracks(arrangement, tracks)

    sample_index = 0
    samples: list[Sample] = []
    track_samples: list[TrackSample] = []

    for track in tracks:
        for item in track:
            if isinstance(item, ChannelPLItem) and isinstance(item.channel, Sampler) and item.channel.sample_path is not None:
                sample_path = _get_sample_path(item.channel.sample_path, samples_dir)
                sample = Sample(sample_index, sample_path, item.offsets)

                if sample in samples:
                    sample = next(s for s in samples if s == sample)
                else:
                    samples.append(sample)
                    sample_index += 1
                
                track_samples.append(TrackSample(
                    track=track.iid,
                    position=item.position,
                    sample=sample,
                ))

    return FlpSlicerResult(
        arrangements=[FlpArrangement(arrangement.iid, arrangement.name) for arrangement in project.arrangements],
        selected_arrangement=arrangement.iid,
        arrangement_tracks=[FlpTrack(track.iid, track.name or f'Track {track.iid}') for track in _get_tracks(arrangement)],
        selected_tracks=[track.iid for track in tracks],
        samples=samples, 
        track_samples=track_samples)


def _get_sample_path(sample_path: PosixPath, sample_dir: str | Path | None = None):
    '''Returns the sample path itself or a path to a sample in a 
    samples directory if provided and the file exists.
    '''
    if sample_dir is None:
        return sample_path

    filename = Path(str(sample_path).replace("\\", "/").split("/")[-1])
    samples_dir_path = PosixPath(sample_dir) / filename

    if samples_dir_path.exists():
        return samples_dir_path
    
    return sample_path


def _get_arrangement(project: Project, arrangement: int | None = None):
    '''Returns the arrangement with the given index or the current arrangement.'''
    if arrangement is None:
        return project.arrangements.current
    
    return next(a for a in project.arrangements if a.iid == arrangement)


def _get_tracks(arrangement: Arrangement, tracks: list[int] | None = None):
    '''Returns the tracks with the given indices or all tracks.'''
    if tracks is None:
        return list(track for track in arrangement.tracks if len(track) and track.enabled)
    
    return list(track for track in arrangement.tracks if track.iid in tracks)
