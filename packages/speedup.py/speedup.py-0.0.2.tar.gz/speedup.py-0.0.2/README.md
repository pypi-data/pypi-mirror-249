# speedup.py
A simple script to speed up (or slow down) your music/audio.

## Installation
To install `speedup.py` on either your system or a Python virtual environment, run:
```
pip install speedup.py
```

## Usage
You can speed up (or slow down) your audio using either the commandline or calling our functions in Python.

### CLI example usage
To speed up `audio.mp3` by a factor of `1.5`, run:
```
speedup audio.mp3 1.5
```
By default the sped up audio is saved as a WAV file. To save it as an MP3, run:
```
speedup audio.mp3 1.5 --codec mp3
```

### Python API example usage
The function `speedup.speedup_file` acts exactly like the CLI. To speed up `audio.mp3` by a factor of `1.5`:
```py
from speedup import speedup_file
speedup_file("audio.mp3", 1.5)
```

To save the sped up audio as an MP3 file:
```py
speedup_file("audio.mp3", 1.5, codec="mp3")
```

By default the sped up audio is saved in `audio-1.5x.{codec}`. This can be manually set using the `output_file` keyword argument. Note that it <u>takes priority over `codec`</u>, so the file extension you write will be passed to `soundfile.write`, encoding your sped up audio as intended.
```py
speedup_file("audio.mp3", 1.5, output_file="audio-dt.mp3")
```

If you already have your audio in a NumPy array, pass it to `speedup.speedup` instead:
```py
from speedup import speedup
from soundfile import read
audio, _ = read("audio.mp3")
spedup_audio = speedup(audio, 1.5)
```
It will return the sped up audio as a NumPy array.

## Build from source
To build the project from source, run the below commands in your terminal:
```
git clone https://github.com/trustytrojan/speedup.py
cd speedup.py
sh devsetup.sh
python -m build
```
