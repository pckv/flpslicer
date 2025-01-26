
from pathlib import Path
from typing import Generator
from .core import Sample

import ffmpeg


def export_samples(
        samples: list[Sample], 
        output_dir: str | Path = "output", 
        *, 
        dry_run: bool = False
    ) -> Generator[Path, None, None]:
    '''Exports the samples to the output directory.'''
    for sample in samples:
        yield export_sample(sample, output_dir, dry_run=dry_run)


def export_sample(
        sample: Sample, 
        output_dir: str | Path = "output", 
        *, 
        dry_run: bool = False
    ) -> Path:
    '''Exports the sample to the output directory.'''
    output_path = Path(output_dir) / f"{sample.id:04d}_{sample.path.stem}.wav"
    if dry_run:
        return output_path

    stream = ffmpeg.input(sample.path)

    # Apply trim to the slice
    if sample.slice is not None:
        stream = stream.filter("atrim", start=sample.slice[0] / 1000, end=sample.slice[1] / 1000)

    stream.output(str(output_path)).run(overwrite_output=True, quiet=True)

    return output_path
