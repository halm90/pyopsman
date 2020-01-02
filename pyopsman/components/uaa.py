#!/usr/bin/env python
"""
      Copyright 2019, Hal Moroff
      Licensed under the GNU General Purpose License.
"""
from logzero import logger
from pyopsman.core.basecomponent import BaseComponent

#pylint: disable=too-few-public-methods

class UAA(BaseComponent):
    """
    Component primary class

    Dealing with UAA (tokens)

    """
    base_url = 'uaa'

    def __init__(self, requestor):
        logger.debug("Initializing component: UAA")
        super().__init__(requestor)
        # without this a call to expiration would yield the url
        # "<base>/uaa/expiration".  This allows a substitution
        # so that the url is "<base>/uaa/tokens_expiration".
        self.expiration = UAAToken(requestor)


class UAAToken(BaseComponent):
    """
    This code is an example only (non-functional)
    Get the UAA token that the admin client will use
    """
    base_url = '/'.join([UAA.base_url, 'tokens_expiration'])
    request_args = {'use_version': False}

    def __init__(self, requestor):
        logger.debug("Initializing sub-component: UAAToken")
        super().__init__(requestor, use_version=False)
