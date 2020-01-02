# pyopsman
# Copyright 2019, Hal Moroff
# Licensed under the GNU General Purpose License.

Python library for accessing _opsman_.

Class objects are instantiated which access the API as methods, masking the
REST interface.

Architecture heavily borrows from cloudianapi by Romero Galiza Jr.

For *opsman* API documentation: https://docs.pivotal.io/pivotalcf/2-2/opsman-api
(later versions may be available at the same site).

## Usage

Sample use:

```
from pyopsman.client import PyOpsmanClient

client = PyOpsmanClient("http://foo/bar", "me", "passwd"[, port=42])

try:
    client.uaa.expiration()
except Exception as exn:
    print("uaa expiration request exception: {}".format(exn))
```

## TODO
* Add header capability to request
* Get token, add to header
* Add (empty) bodies for major command groups (as in UAA)
* Add specific major commands to command groups
* Unit tests
