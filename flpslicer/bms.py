from .core import TrackSample, TRACK_PPQ


BMS_PPQ = 48  # 192 / 4


def get_note_ibmsc_clipboard_data(track_samples: list[TrackSample]):
    '''Returns note clipboard data for iBMSC.'''
    output = 'iBMSC Clipboard Data xNT\n'
    for track_sample in track_samples:
        position = track_sample.position * BMS_PPQ / TRACK_PPQ
        # convert to int if it's a whole number
        if position.is_integer():
            position = int(position)

        output += f'{track_sample.track + 27} {position} {track_sample.sample.id + 1}0000 0 0 0\n'
    
    return output
