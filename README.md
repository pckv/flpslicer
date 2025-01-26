# flpslicer

This tool can be used to slice BMS samples and copy note data from the stems of a song using FL Studio. Mostly as an alternative to [woslicerII](https://github.com/SayakaIsBaka/woslicerII-english).

Future version may include MIDI-support with some extra steps.

## Installation

> :warning: Installation will be simpler in the future using PIP or an optional installer which includes a GUI tool

1. Install python
2. Install ffmpeg and make sure it's accessible from a terminal
3. Clone the repo using git or download and extract the source code and navigate to the folder in a terminal
4. Optionally create and activate a virtual environment
5. Install packages using pip
   ```
   $ pip install -r requirements.txt
   ```

## How to use

### Preparing the project file (.flp)

1. Export stems for your finished and mixed track by separating every sound that should be keysounded
2. Create a new project and add your stems to each track
   > :warning: You can also create a new arrangement in your song's project file, but the tool might encounter problems when loading it. The tool uses the current arrangement used when saving by default
3. Use the slice tool to slice every stem and delete silent parts
   > :warning: The tool currently doesn't support trimming silence, so you're encouraged to do it manually in the project file
4. Optionally optimise your exported samples by re-using slices for your stems. Use this for repeated patterns/loops and percussion
5. Enable every track you want to include as keysounds
   > 🗣️ You can disable tracks for stems that you may want to keep in the background. This is useful if you've exceeded the limit of samples you can use in a BMS file. Simply move them to a disabled track, or disable the track entirely
6. Save the file

Here's what your project file should look like. All stems in this one are enabled and will be exported by default.

![FL64_D0Wb1h1NkK](https://github.com/user-attachments/assets/8d88b86a-1fba-497d-942b-2075453ded3a)

### Slicing samples with the tool

Run the tool with a path to the FLP:

```
$ python3 -m flpslicer path/to/project.flp
```

The exported stems will be saved to the same folder as the FLP file. See [Parameters](#parameters) for alternatives.

You can copy and paste the note data output into iBMSC-derived editors. See [Parameters](#parameters) for alternatives.

#### Parameters

Add the `--output` parameter to export the files to a different folder:

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

For other parameters, use the tool with `--help`:

```
$ python3 -m flpslicer --help
```
