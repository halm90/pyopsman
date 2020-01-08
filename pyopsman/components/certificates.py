#!/usr/bin/env python
"""
      Copyright 2019
      Licensed under the GNU General Purpose License.
"""
from logzero import logger
from pyopsman.core.basecomponent import BaseComponent

#pylint: disable=too-few-public-methods

class Certificates(BaseComponent):
    """
    Component primary class

    Dealing with certificates

    """
    base_url = None

    def __init__(self, requestor):
        logger.debug("Initializing component: Sessions")
        super().__init__(requestor)
        self.generate = Generate(requestor)
        self.information = Information(requestor)


class Generate(BaseComponent):
    """
    """
    base_url = '/'.join(['certificates', 'generate'])

    def __init__(self, requestor):
        logger.debug("Initializing Certificates sub-component: Generate")
        super().__init__(requestor)


class Information(BaseComponent):
    """
    """
    base_url = '/'.join(['deployed', 'certificates'])

    def __init__(self, requestor):
        logger.debug("Initializing Certificates sub-component: Information")
        super().__init__(requestor)
