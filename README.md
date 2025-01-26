# flpslicer

This tool can be used to slice BMS samples and copy note data from the stems of a song using FL Studio. Mostly as an alternative to woslicer.

Future version may include MIDI-support with some extra steps.

## Innstallation

> :warning: Installation will be simpler in the future using PIP or an optional installer which includes a GUI tool

1. Install python
2. Install ffmpeg and make sure it's accessible from a terminal
3. Clone the repo using git or download and extract the source code and navigate to the folder in a terminal
4. Install packages using pip
   ```
   $ pip install -r requirements
   ```

## How to use

### Preparing the project file (.flp)

1. Export stems for your finished and mixed track by separating every sound that should be keysounded
2. Create a new project and add your stems to each track
   > :warning: You can also create a new arrangement in your song's project file, but the tool might encounter problems when loading it
3. Name every track
   > :warning: The name of a track is currently not used by the tool, but a name is required to discover which tracks are used
4. Use the slice tool to slice every stem
5. Optionally optimise your exported samples by re-using slices for your stems. Use this for repeated patterns/loops and percussion
6. Enable every track you want to include as keysounds
   > 🗣️ You can disable stems that you may want to keep in the background. This is useful if you've exceeded the limit of samples you can use in a BMS file. Simply move them to a disabled track.
7. Save the file

### Slicing the samples with the tool

Run the tool with a path to the FLP:

```
$ python3 -m flpslicer path/to/project.flp
```

The exported stems will be saved to the same folder as the FLP file.

You can copy and paste the note data output into iBMSC-derived editors.

#### Parameters

Add the `--output path/to/folder` parameter to export the files to a different folder:

```
$ python3 -m flpslicer path/to/.flp -o bms-samples
```

Add `--to-file` to save the note data to a file, such as `clipboard.txt`

```
$ python3 -m flpslicer path/to/.flp --to-file clipboard.txt
```

If your samples can't be accessed using their original path (in case you're using WSL like I did), use `--samples-dir` to point to a folder where the original samples are located:

```
$ python3 -m flpslicer path/to/.flp --samples-dir flp-samples
```

For other parameters, use the tool with `--help`

```
$ python3 -m flpslicer --help
```
