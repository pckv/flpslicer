
from pathlib import Path
from typing import Generator
from .core import Sample

import ffmpeg


def export_samples(
        samples: list[Sample], 
        output_dir: str | Path = "output", 
        *, 
        fade_in: int = 0,
        fade_out: int = 0,
        dry_run: bool = False
    ) -> Generator[Path, None, None]:
    '''Exports the samples to the output directory.'''
    for sample in samples:
        yield export_sample(sample, output_dir, fade_in=fade_in, fade_out=fade_out, dry_run=dry_run)


def export_sample(
        sample: Sample, 
        output_dir: str | Path = "output", 
        *, 
        fade_in: int = 0,
        fade_out: int = 0,
        dry_run: bool = False
    ) -> Path:
    '''Exports the sample to the output directory.'''
    output_path = Path(output_dir) / f"{sample.id:04d}_{sample.path.stem}.wav"
    if dry_run:
        return output_path

    stream = ffmpeg.input(sample.path)

    if sample.slice is not None:
        duration = (sample.slice[1] - sample.slice[0]) / 1000

        # Apply trim to the slice
        stream = stream \
            .filter("atrim", start=sample.slice[0] / 1000, end=sample.slice[1] / 1000 + fade_out / 1000) \
            .filter("asetpts", "PTS-STARTPTS")

        # Apply fade in/out if specified
        if fade_in > 0:
            stream = stream.filter("afade", t="in", st=0, d=fade_in / 1000)
        if fade_out > 0 and duration > fade_out / 1000:
            # Fade out from the end of the slice to cross-fade with the next slice
            stream = stream.filter("afade", t="out", st=duration, d=fade_out / 1000)

    try:
        stream.output(str(output_path)).run(overwrite_output=True, quiet=True, capture_stderr=True)
    except ffmpeg.Error as e:
        print(f'\nError exporting {sample.path}: {e.stderr}')
        raise e

    return output_path
