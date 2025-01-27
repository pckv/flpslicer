from .core import TRACK_CLIP_POSITION_PPQ, TrackClip


BMS_PPQ = 48
FIRST_TRACK = 27


def get_note_ibmsc_clipboard_data(track_samples: list[TrackClip], *, sample_id_offset: int = 1) -> str:
    '''Returns note clipboard data for iBMSC.'''
    output = 'iBMSC Clipboard Data xNT\n'
    for track_sample in track_samples:
        position = track_sample.position * BMS_PPQ / TRACK_CLIP_POSITION_PPQ
        # convert to int if it's a whole number
        if position.is_integer():
            position = int(position)

        output += f'{track_sample.track + FIRST_TRACK} {position} {track_sample.sample.id + sample_id_offset}0000 0 0 0\n'
    
    return output


def get_sample_id_from_bms_label(label: str) -> int:
    '''Returns the sample ID from a BMS WAV label definition.'''
    sample_id = int(label, 36)

    if sample_id > int('ZZ', 36):
        raise ValueError(f'Invalid sample ID: {label}')

    return sample_id
