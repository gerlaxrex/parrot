# PARRoT: Precise Audio Recognition and Recap over Transcription

[![powered by OpenAI](https://img.shields.io/badge/%7F-powered_by_OpenAI-grey.svg?logo=OpenAI)](https://shields.io/)<br>

<img src="https://github.com/gerlaxrex/parrot/blob/dbf60ce0d294d31afcebd811c5d89239623fa9d7/assets/images/parrot-logo.png?raw=true" width="500" height="500" />

A tool for writing a recap mail or report from a video recording of a call.

## installation

PARRoT can be installed from pyPI by simply doing:

```shell
python -m pip install parrot1
```

with the following extras:

`faster-whisper` -> to install faster-whisper dependencies</br>
`llama-cpp` -> to install llama-cpp dependencies</br>
`os-models` -> to install both the previous ones</br>
`docx` -> to use external transcription</br>
`all` -> install everything</br>

For instance:
```shell
python -m pip install parrot1[os-models]
```

**NOTE:** PARRoT requires [FFmpeg](https://ffmpeg.org/) available and visible in the system! 

## usage

You can find all the information needed for using the tool by doing 

`parrot --help`

At the moment, there are two commands:

`parrot mail <video_path>`
and
`parrot recap <video_path>`

Options:

`--transcript (-t) <PATH>`: path to the transcript with speakers (Optional).

`--output_filepath (-o) <PATH>`: path to the final result (Optional, by default it creates the file in the current working directory).

`--faster-whisper (-fw)`: If set, it uses faster whisper instead of hosted OpenAI Whisper.

`--llama-cpp (-lc)`: If set, it uses llama-cpp instead of the hosted OpenAI GPT model.

## contributing

First of all make sure you have installed pre-commit and can use it.

`pip install pre-commit`

and

`pre-commit install`

You can't push your code directly in the contrib branch. You should open a branch (feat|fix)/<major-feature>[/<sub-feature>] and then open a PR with reviewers.

Please try sticking to the code style or, for any eventual suggestion for libraries/patterns, discuss it before in a issue.
