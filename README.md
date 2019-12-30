# pyopsman
# Copyright 2019, Hal Moroff
# Licensed under the GNU General Purpose License.

Python library for accessing _opsman_.

**This is a work-in-progress.**

Class objects are instantiated which access the API as methods, masking the
REST interface.

Architecture is borrowed from cloudianapi by Romero Galiza Jr.

## Usage

Sample use:
`
from pyopsman.client import PyOpsmanClient

client = PyOpsmanClient("http://foo/bar", "me", "passwd", port=42)

try:
    client.uaa.expiration()
except Exception as exn:
    print("uaa expiration request exception: {}".format(exn))
`
