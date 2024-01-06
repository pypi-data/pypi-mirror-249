# homekitlink_ffmpeg pypi package

A package that provides pre-compiled FFmpeg binaries for OSX systems.

Usage:  Should be used behind the scenes to enable plugins to download ffmpeg binaries without apple quarantine becoming a major PITA

The package consists of 2 uptodate ffmpeg binaries including HomeKit specific aac features.
get_ffmpeg_binary will return the path to the correct binary for either x86 OSX Mac or ARM MAC

## Installation

To install the package, run:

```python
pip3.11 install homekitlink_ffmpeg
```

## Usage

Here's how you can use the package:

```python
from homekitlink_ffmpeg import get_ffmpeg_binary
import subprocess

binary_path = get_ffmpeg_binary()

print(binary_path)

subprocess.run(binary_path)

# You can now use the path to the binary in your application
```

## License

This project is licensed under the MIT License - see the LICENSE file for details

MIT License

Copyright (c) [2023]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
