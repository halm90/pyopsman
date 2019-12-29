#!/usr/bin/env python
# -*- coding:utf8 -*-
"""

      Copyright 2019, Hal Moroff

      Licensed under the GNU General Purpose License.

"""
import importlib

# See the comment in __init__ below.  This table allows adding a
# module without altering this module's code and without repeating
# module/package/class names
#
# The format is:
#  <module import path> : (<module class/package name>, <local/reference name>)
import_list = {"pyopsman.components.admin": ("Admin", "admin"),
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
        # This allows us to add new modules by simply adding them to the
        # "import_list" above.  Loop through each list entry:
        #    - import the module
        #    - instantiate the module class
        #    - assign the instantiated class to a class variable
        # The caller can then do this:
        #   > myclient = PyOpsmanClient(...args...)
        #   > myclient.<module>.<module command
        # For example:
        #   > myclient = PyOpsman("url", 42, "myuser", "mypasswd")
        #   > myclient.auth.authenticate(args)
        for module, (component, package) in import_list.items():
            imported = importlib.import_module(module, package=package)
            cmd = "imported.{}(self._requestor)".format(component)
            exec("self.{} = {}".format(package, cmd))