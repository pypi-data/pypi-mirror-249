from typing import Callable, Optional
from numpy.typing import ArrayLike
from argparse import ArgumentParser
import soundfile as sf
import sounddevice as sd
import numpy as np
import scipy.signal

arg_parser = ArgumentParser(description="Speed up or slow down your audio.")

ARGUMENTS = {
	"audio_file": {
		"help": "A file containing audio"
	},

	"multiplier": {
		"type": float,
		"help": "Audio speed multiplier"
	},

	"--codec": {
		"help": "The audio codec (and file extension) to write the output file with",
		"default": "mp3",
	},

	"--output-file": {
		"help": "Where to store the sped up audio"
	},

	"--play": {
		"help": "Play the new audio instead of saving it",
		"action": "store_true"
	}
}

for key, value in ARGUMENTS.items():
	arg_parser.add_argument(key, **value)

speedup: Callable[[ArrayLike, float], ArrayLike]
speedup = lambda audio, multiplier: scipy.signal.resample(audio, int(np.size(audio, axis=0) * (1 / multiplier)))

def highest_index(s: str, target: str) -> int:
	for i in range(len(s) - 1, -1, -1):
		if s[i] == target:
			return i
	return -1

def speedup_file(
	input_file: str,
	multiplier: float,
	codec: Optional[str] = "mp3",
	output_file: Optional[str] = None
) -> None:
	if multiplier == 1:
		return
	if codec is None:
		codec = "mp3"

	input_filename = input_file[highest_index(input_file, "/") + 1 : highest_index(input_file, ".")]

	if output_file is None:
		output_file = f"{input_filename}-{multiplier}x.{codec}"

	audio, samplerate = sf.read(input_file)
	spedup_audio = speedup(audio, multiplier)
	sf.write(output_file, spedup_audio, samplerate)

def speedup_play(input_file: str, multiplier: float):
	audio, samplerate = sf.read(input_file)
	sd.play(audio, samplerate * multiplier, blocking=True)

def main() -> None:
	args = arg_parser.parse_args()
	if args.play:
		speedup_play(args.audio_file, args.multiplier)
	speedup_file(args.audio_file, args.multiplier, args.codec, args.output_file)

if __name__ == "__main__":
	main()
