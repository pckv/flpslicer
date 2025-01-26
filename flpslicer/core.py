from dataclasses import dataclass
from pathlib import Path

TRACK_PPQ = 96

@dataclass
class Sample:
    '''A unique sample in the project with an optional slice.'''

    id: int
    '''Sample ID.'''

    path: Path
    '''Path to the sample.'''

    slice: tuple[int, int] | None
    '''Optional slice of the sample.'''

    def __eq__(self, other):
        return self.path == other.path and self.slice == other.slice


@dataclass
class TrackSample:
    '''A sample in a track.'''

    track: int
    '''The track index based on selected tracks.'''

    position: int
    '''The position in the track in 192 PPQ.'''

    sample: Sample
    '''The sample.'''
