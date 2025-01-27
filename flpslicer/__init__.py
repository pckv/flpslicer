'''bmsslicer - Convert sample-based arrangements with slices to BMS notes.'''

from .core import (
    TRACK_CLIP_POSITION_PPQ,
    Sample, 
    TrackClip,
)
from .flp import (
    FlpArrangement,
    FlpTrack,
    FlpSlicerResult,
    get_flp_slices,
)
from .audio import (
    export_sample,
    export_samples,
)
from .bms import (
    BMS_PPQ,
    get_note_ibmsc_clipboard_data,
    get_sample_id_from_bms_label,
)

__version__ = '0.1.0'
__author__ = 'pckv'
