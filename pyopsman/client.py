#!/usr/bin/env python
"""
      Copyright 2019, Hal Moroff
      Licensed under the GNU General Purpose License.
"""
import importlib
import logging
import os
from logzero import logger
from logzero import loglevel
from pyopsman.core.requestors import HttpRequestor

loglevel(os.environ.get('LOGLEVEL', logging.INFO))

#pylint: disable=bad-continuation
# See the comment in __init__ below.  This table allows adding a
# module without altering this module's code and without repeating
# module/package/class names
#
# The format is:
#  <module import path> : (<module class/package name>, <local/reference name>)
IMPORT_LIST = {
               "pyopsman.components.admin": ("Admin", "admin"),
               "pyopsman.components.uaa": ("UAA", "uaa"),
              }


#pylint: disable=exec-used, too-few-public-methods, logging-not-lazy

class PyOpsmanClient():
    """
    The main client object.  Instantiate this and then use the object to
    access all major/minor commands.

    For example to access the "token_expiration" opsman endpoint use this:
        client = PyOpsmanClient(<opsman url>, <user>, <password>)
        client.uaa.expiration()
    """
    def __init__(self, url: str, user: str, pwd: str,
                 *,
                 port: int = None, version: str = "v0"):
        self._url = url
        self._port = port
        self._ops_user = user
        self._pwd = pwd
        self._version = version

        logger.debug("PyOpsmanClient instantiating HttpRequestor " +
                     "url: %s, port: %s, user: %s, pwd: <redacted>",
                     url, str(port), user)
        self._requestor = HttpRequestor(self._url, self._ops_user, self._pwd,
                                        version=self._version,
                                        port=self._port)

        # Instantiate the class for each main operation
        # This allows us to add new modules by simply adding them to the
        # "IMPORT_LIST" above.  Loop through each list entry:
        #    - import the module
        #    - instantiate the module class
        #    - assign the instantiated class to a class variable
        # The caller can then do this:
        #   > myclient = PyOpsmanClient(...args...)
        #   > myclient.<module>.<module command
        # For example:
        #   > myclient = PyOpsman("url", 42, "myuser", "mypasswd")
        #   > myclient.auth.authenticate(args)
        logger.debug("PyOpsmanClient importing components")
        for module, (component, package) in IMPORT_LIST.items():
            logger.debug("PyOpsmanClient: from %s import %s as %s",
                         module, component, package)
            #pylint: disable=unused-variable
            imported = importlib.import_module(module, package=package)
            cmd = "imported.{}(self._requestor)".format(component)
            exec("self.{} = {}".format(package, cmd))
