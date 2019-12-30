#!/usr/bin/env python
# -*- coding:utf8 -*-
#
#      Copyright 2019, Hal Moroff
#
#      Licensed under the GNU General Purpose License.
#
from logzero import logger
from pyopsman.core.basecomponent import BaseComponent


class UAA(BaseComponent):
    """
    Component primary class

    Dealing with UAA (tokens)

    """
    base_url = 'uaa'

    def __init__(self, requestor):
        logger.debug("Initializing component: UAA")
        super().__init__(requestor)
        self.expiration = UAAToken(requestor)


# #
# Component ancillary / supporting classes
class UAAToken(BaseComponent):
    # This code is an example only (non-functional)
    # Get the UAA token that the admin client will use
    base_url = '/'.join([UAA.base_url, 'tokens_expiration'])

    def __init__(self, *args, **kwargs):
        logger.debug("Initializing sub-component: UAAToken")
        super().__init__(*args, **kwargs)
