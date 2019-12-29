#!/usr/bin/env python
# -*- coding:utf8 -*-
#
#      Copyright 2019, Hal Moroff
#
#      Licensed under the GNU General Purpose License.
#

#from pyopsman.components.admin import Admin
import importlib

import_list = {"pyopsman.components.admin": ("admin", "Admin"),
              }

from pyopsman.core.requestors import HttpRequestor

class PyOpsmanClient():
    def __init__(self, url: str, port: int, user: str, pwd: str):
        self._url = url
        self._port = port
        self._ops_user = user
        self._pwd = pwd

        self._requestor = HttpRequestor(self._url, self._port,
                                        self._ops_user, self._pwd)

        # Instantiate the class for each main operation
        for module, (package, component) in import_list.items():
            imported = importlib.import_module(module, package=package)
            # WIP / ERROR / can't use component in next line like that
            self.package = imported.component(self._requestor)
