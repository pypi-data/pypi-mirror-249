# plugin_gifsicle pypi package

A package that provides pre-compiled Gifsicle binaries for OSX systems.
Yah to:https://github.com/kohler/gifsicle

Usage:  Should be used behind the scenes to enable plugins to download gifsicle binaries without apple quarantine becoming a major PITA

What is Gifsicle:
https://github.com/kohler/gifsicle
Basically it is a binary to create animated gifs with many options and typically producing a excellent, small file as a result

The package consists of 2 1.94 gifscile binaries including newer --lossy options.
get_gifsicle_binary will return the path to the correct binary for either x86 OSX Mac or ARM MAC

## Installation

To install the package, run:

```python
pip3 install plugin_gifsicle
```

## Usage

Here's how you can use the package:

```python
from plugin_gifsicle import get_gifsicle_binary
import subprocess

binary_path = get_gifsicle_binary()
print(binary_path)
# and for good measure below will check can run the binary correctly
# will need options etc. for proper usage
subprocess.run([binary_path,"--help"])

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
