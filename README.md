# PARRoT: Precise Audio Recognition and Recap over Transcription
[![Powered by OpenAI](https://img.shields.io/badge/%7F-Powered_by_OpenAI-grey.svg?logo=OpenAI)](https://shields.io/)<br>
<img src="https://github.com/gerlaxrex/parrot/assets/36633875/06859697-8c19-4dc7-a23a-151fd18137ab" width="500" height="500" />

A tool for writing a recap mail or report from a video recording of a call.

### How to use it

PARRoT can be installed by simply doing 

`pip install PARRoT`

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

### Guide for contribution

First of all make sure you have have installed pre-commit and can use it.

`pip install pre-commit`

and

`pre-commit install`

You can't push your code directly in the contrib branch. You should open a branch (feat|fix)/<major-feature>[/<sub-feature>] and then open a PR with reviewers.

Please try sticking to the code style or, for any eventual suggestion for libraries/patterns, discuss it before in a issue.



