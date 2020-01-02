#!/usr/bin/env python
"""
      Copyright 2019, Hal Moroff
      Licensed under the GNU General Purpose License.
"""
from logzero import logger
from pyopsman.core.basecomponent import BaseComponent

#pylint: disable=too-few-public-methods

class Sessions(BaseComponent):
    """
    Component primary class

    Dealing with sessions

    """
    base_url = 'sessions'

    def __init__(self, requestor):
        logger.debug("Initializing component: Sessions")
        super().__init__(requestor)
        self.logout = Delete(requestor)
        self.current = Current(requestor)


class Delete(BaseComponent):
    """
    """
    def __init__(self, requestor):
        logger.debug("Initializing Sessions sub-component: Delete")
        super().__init__(requestor)


class Current(BaseComponent):
    """
    """
    base_url = '/'.join([Sessions.base_url, 'current'])

    def __init__(self, requestor):
        logger.debug("Initializing Sessions sub-component: Current")
        super().__init__(requestor)
