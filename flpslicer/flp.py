from dataclasses import dataclass
from pathlib import Path, PosixPath

import pyflp
from pyflp.project import Project
from pyflp.arrangement import ChannelPLItem, Arrangement
from pyflp.channel import Sampler

from .core import TRACK_CLIP_POSITION_PPQ, Sample, TrackClip


@dataclass
class FlpArrangement:
    '''Represents an arrangement in an FL Studio project file.'''
    iid: int
    name: str


@dataclass
class FlpTrack:
    '''Represents a track in an arrangement in an FL Studio project file.'''
    iid: int
    name: str


@dataclass
class FlpSlicerResult:
    '''The result of slicing an FL Studio project file.'''

    arrangements: list[FlpArrangement]
    '''All arrangements in the project.'''

    selected_arrangement: int
    '''The index of the selected arrangement.'''

    arrangement_tracks: list[FlpTrack]
    '''All tracks in the selected arrangement.'''

    selected_tracks: list[int]
    '''The indices of the selected tracks.'''

    samples: list[Sample]
    '''All unique samples in the selected tracks.'''

    track_clips: list[TrackClip]
    '''All audio clips in the selected tracks. Each clip references a sample.'''


def get_flp_slices(
        flp_path: str | Path, 
        *, 
        samples_dir: str | Path | None = None,
        selected_arrangement: int | None = None,
        selected_tracks: list[int] | None = None,
    ) -> FlpSlicerResult:
    '''Finds all used audio clips and their sliced samples in the selected tracks of 
    an FL Studio project file.
    '''
    project = pyflp.parse(flp_path)
    selected_arrangement = _get_arrangement(project, arrangement=selected_arrangement)
    selected_tracks = _get_tracks(selected_arrangement, selected_tracks=selected_tracks, only_enabled=True)

    samples: list[Sample] = []
    track_clips: list[TrackClip] = []

    # Keep unique indices of samples and used tracks
    sample_index = 0
    track_index = 0

    for track in selected_tracks:
        for item in track:
            if isinstance(item, ChannelPLItem) and isinstance(item.channel, Sampler) and item.channel.sample_path is not None:
                sample_path = _get_sample_path(item.channel.sample_path, samples_dir)
                sample = Sample(sample_index, sample_path, _get_slice(item.offsets))

                if sample in samples:
                    sample = next(s for s in samples if s == sample)
                else:
                    samples.append(sample)
                    sample_index += 1
                
                track_clips.append(TrackClip(
                    track=track_index,
                    position=item.position * TRACK_CLIP_POSITION_PPQ // project.ppq,
                    sample=sample,
                ))
        track_index += 1

    return FlpSlicerResult(
        arrangements=[FlpArrangement(arrangement.iid, arrangement.name) for arrangement in project.arrangements],
        selected_arrangement=selected_arrangement.iid,
        arrangement_tracks=[FlpTrack(track.iid, track.name or f'Track {track.iid}') for track in _get_tracks(selected_arrangement)],
        selected_tracks=[track.iid for track in selected_tracks],
        samples=samples, 
        track_clips=track_clips)


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


def _get_arrangement(project: Project, *, arrangement: int | None = None):
    '''Returns the arrangement with the given index or the current arrangement.'''
    if arrangement is None:
        return project.arrangements.current
    
    return next(a for a in project.arrangements if a.iid == arrangement)


def _get_tracks(
        arrangement: Arrangement, 
        *,
        selected_tracks: list[int] | None = None, 
        only_enabled: bool = False):
    '''Returns the tracks with the given indices or all tracks.'''
    if selected_tracks is not None:
        return list(track for track in arrangement.tracks if track.iid in selected_tracks)
    
    return list(track for track in arrangement.tracks if len(track) and (not only_enabled or track.enabled))


def _get_slice(offsets: tuple[float, float]):
    '''Returns the slice of the sample or None if the slice is invalid.'''
    if offsets[0] >= 0 and offsets[1] >= 0:
        return offsets

    return None
