from dataclasses import dataclass
from pathlib import Path

TRACK_CLIP_POSITION_PPQ = 960

@dataclass
class Sample:
    '''A unique sample in the project with an optional slice.'''

    id: int
    '''Sample ID.'''

    path: Path
    '''Path to the sample.'''

    slice: tuple[float, float] | None
    '''Optional slice of the sample.'''

    def __eq__(self, other):
        return self.path == other.path and self.slice == other.slice


@dataclass
class TrackClip:
    '''An audio clip in a track.'''

    track: int
    '''The track index based on selected tracks.'''

    position: int
    '''The position in the track in 960 PPQ.'''

    sample: Sample
    '''The sample used in the audio clip.'''
