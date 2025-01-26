'''CLI tool for slicing FLP files into BMS note data.'''



from argparse import ArgumentParser
from pathlib import Path

from tqdm import tqdm

from . import __version__
from .flp import get_flp_slices, FlpSlicerResult
from .audio import export_samples
from .bms import get_note_ibmsc_clipboard_data


cli_description = '''
Slices FLP files into BMS note data.

The tool reads FLP files and extracts samples from tracks in the current arrangement. 
The samples are then converted into BMS note data for iBMSC-related BMS editors.
'''


def _print_arrangements(flp_result: FlpSlicerResult, selected_arrangement: int | None = None):
    print(f'Arrangements:')
    for arrangement in flp_result.arrangements:
        print(f'  {arrangement.iid}: {arrangement.name}{" (selected)" if arrangement.iid == selected_arrangement else ""}')


def _print_tracks(flp_result: FlpSlicerResult, selected_tracks: list[int] | None = None):
    print(f'Tracks:')
    for track in flp_result.arrangement_tracks:
        print(f'  {track.iid}: {track.name}{" (selected)" if selected_tracks and track.iid in selected_tracks else ""}')


def main():
    parser = ArgumentParser(description=cli_description.strip(), prog='flpslicer')
    parser.add_argument('input', help='FLP file path')
    parser.add_argument('-o', '--output', help='Directory for sliced samples', default=None)
    parser.add_argument('--to-file', help='Export note data to a file', default=None)
    parser.add_argument('--samples-dir', help='Optional directory for samples used in the FLP', default=None)
    parser.add_argument('-a', '--arrangement', help='Arrangement index to use', type=int, default=None)
    parser.add_argument('--list-arrangements', help='List all arrangements in the FLP', action='store_true')
    parser.add_argument('-t', '--tracks', help='Track indexes to use', nargs="+", type=int, default=None)
    parser.add_argument('--list-tracks', help='List all tracks in the FLP for the selected arrangement', action='store_true')
    parser.add_argument('-q', '--quiet', help='Do not print any output', action='store_true')
    parser.add_argument('-v', '--verbose', help='Print more output', action='store_true')
    parser.add_argument('--dry-run', help='Do not write any files', action='store_true')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    args = parser.parse_args()

    output_dir = Path(args.output) if args.output else Path(args.input).parent
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    # Analyse FLP file
    flp_result = get_flp_slices(
        args.input,
        samples_dir=args.samples_dir,
        arrangement=args.arrangement,
        tracks=args.tracks,
    )

    if args.list_arrangements:
        _print_arrangements(flp_result, selected_arrangement=flp_result.selected_arrangement)
        return

    if args.list_tracks:
        _print_tracks(flp_result, selected_tracks=flp_result.selected_tracks)
        return

    if not args.quiet:
        print(f'Opened {args.input}')
        _print_arrangements(flp_result, selected_arrangement=flp_result.selected_arrangement)
        _print_tracks(flp_result, selected_tracks=flp_result.selected_tracks)

    # Export track samples
    export_task = export_samples(flp_result.samples, output_dir, dry_run=args.dry_run)
    for sample in (tqdm(export_task, desc='Exporting samples') if not args.quiet else export_task):
        if args.verbose:
            print(f'Exported {sample}')
    
    if not args.quiet:
        print(f'Exported {len(flp_result.samples)} samples to {output_dir}\n')

    # Export note data
    note_data = get_note_ibmsc_clipboard_data(flp_result.track_samples)
    if args.to_file:
        with open(args.to_file, 'w') as f:
            f.write(note_data)
        if not args.quiet:
            print(f'Exported note data to {args.to_file}')
    else:
        print(note_data)


if __name__ == '__main__':
    main()
