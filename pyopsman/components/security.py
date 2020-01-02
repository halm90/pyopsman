#!/usr/bin/env python
"""
      Copyright 2019, Hal Moroff
      Licensed under the GNU General Purpose License.
"""
from logzero import logger
from pyopsman.core.basecomponent import BaseComponent

#pylint: disable=too-few-public-methods

class Security(BaseComponent):
    """
    Component primary class

    Dealing with security

    """
    base_url = 'security'

    def __init__(self, requestor):
        logger.debug("Initializing component: Sessions")
        super().__init__(requestor)
        self.rootcert = RootCert(requestor)


class RootCert(BaseComponent):
    """
    """
    base_url = '/'.join([Security.base_url, 'root_ca_certificate'])

    def __init__(self, requestor):
        logger.debug("Initializing Security sub-component: RootCert")
        super().__init__(requestor)
