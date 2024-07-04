# TesseraTwist

Slicing an image into multiple pieces, randomizing them, and creating a timelaps for multiple randomly sliced images is what this project can do!

## Show case

Assume you have image below as input:

<p align="center">
  <img width="300px" src="https://raw.githubusercontent.com/sepgh/TesseraTwist/main/.showcase/sample.jpg" />
</p>

Tessera Twist can create outputs like below (in video format, not GIF), in different slice/piece counts, framerates and duration:

<p align="center">
  <img width="300px" src="https://raw.githubusercontent.com/sepgh/TesseraTwist/main/.showcase/tt-horizontal.gif" />
  <br>
  Horizontal
</p>

<p align="center">
  <img width="300px" src="https://raw.githubusercontent.com/sepgh/TesseraTwist/main/.showcase/tt-vertical.gif" />
  <br>
  Vertical
</p>

<p align="center">
  <img width="300px" src="https://raw.githubusercontent.com/sepgh/TesseraTwist/main/.showcase/tt-tiles.gif" />
  <br>
  Tiles
</p>

There is also an **[Youtube Video](https://youtu.be/1eAaRvNF0cE)** on how this project is made.

## Requirements

I've used `Python 3.12` to develop and test the project but I dont recall using any syntax specific to versions above `3.6`.
You also need `FFMPEG` binary, either available to `path` or you can pass the binary location to the script. `libx264` is also required which is usually packed with ffmpeg anyways.

## How to use

Install the requirements, and use CLI like below:

```
$ python tessera_twist.py -h

usage: Tessera Twist [-h] -i INPUT -o OUTPUT -g {SV,SH,ST} [-s STORAGE] [-p PIECES] [-w WORKERS] [-d DURATION] [-fb FFMPEG] [-crf CRF] [-fps FPS] [-smoother {1,0}]

Sliced image turns into a timelaps

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input image file
  -o OUTPUT, --output OUTPUT
                        Output timelapse path (including filename ending in mp4)
  -g {SV,SH,ST}, --generator {SV,SH,ST}
                        Image generator type. "SV" for "VerticalSingleSourceImageGenerator", "SH" for "HorizontalSingleSourceImageGenerator", "ST" for
                        "TilingSingleSourceImageGenerator"
  -s STORAGE, --storage STORAGE
                        Storage directory to store timelapse images in. Default would be in temp.
  -p PIECES, --pieces PIECES
                        Pieces / Slices count
  -w WORKERS, --workers WORKERS
                        Number of worker processes
  -d DURATION, --duration DURATION
                        Duration of the clip in seconds
  -fb FFMPEG, --ffmpeg FFMPEG
                        Path to ffmpeg executable
  -crf CRF              Value for crf flag passed to ffmpeg
  -fps FPS              Value for fps flag passed to ffmpeg
  -smoother {1,0}       Smoothing by doing more shifts next to shuffles. This is incomplete.

```

## Examples


Use `sample.jpg` to generate `5` seconds of timelaps where each frame is sliced to `4x4` tiles using `Single Source Tile Image Generator (ST)` with `15` FPS (framerate), use directory called `output` to store timelaps images, and output file name (path) should be `timelaps-tiles.mp4`.

```
python tessera_twist.py -i ./sample.jpg -o ./timelaps-tiles.mp4 -g ST -s ./output -p 4 -d 5 -fps 15
```

Same thing, but with `4` horizontal slices (notice `-g SH`):

```
python tessera_twist.py -i ./sample.jpg -o ./timelaps-horizontal.mp4 -g SH -s ./output -p 4 -d 5 -fps 15
```

You can us `-fb /path/to/ffmpeg` and `-crf 0-23` to change ffmpeg location and `-crf` value. 

FFmpeg configurations are available [in this class](https://github.com/sepgh/TesseraTwist/blob/bfbfb3428f34b0c97f6294436c3456a9e70c893d/video/timelapse_generator.py#L27-L36).


---

## Donations

Coffee has a cost :smile:

Any  sort of small or large donations can be a motivation in maintaining this repository and related repositories.

- **ETH**: `0x5F120228C12e2C6923AfDeb0e811d74160166d90`
- **TRC20**: `TJjw5n26KFBqkJQbs7eKdxkVuk4pvJdFzE`
- **BTC**: `bc1qmtewrl7srjrkl8t4z5vantuqkz086srj4clzh3`



