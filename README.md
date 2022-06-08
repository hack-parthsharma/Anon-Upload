# anonfiles-script
An upload script for anonfiles.com made in python. Supports multiple files.

 [![PyPI version](https://badge.fury.io/py/anonupload.svg)](https://pypi.org/project/anonupload/)
 ![Python 3.6](https://img.shields.io/badge/python-3.6-yellow.svg)


## Features
- Progress bar
- upload urls will save in a file.
- You can change file name before upload on anonfile server


## Installation

```sh
pip3 install anonupload
```

## Usage 
```sh
anon up {path-to-file_1} {path-to-file _2} ...  # upload file to anonfile server
anon d {url1} {url2} ...              # download file 
```

# API

The anonfile-upload client is also usable through an API (for test integration, automation, etc)

### anonupload.upload([file1, file2])

```py
from anonupload import upload

upload([file1, file2])
```

### anonupload.download([file1, file2])

```py
from anonupload import download

download([url1, url2])
```
