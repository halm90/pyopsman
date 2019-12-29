#!/usr/bin/env python
# -*- coding:utf8 -*-
#
#      Copyright 2019, Hal Moroff
#
#      Licensed under the GNU General Purpose License.
#
from logzero import logger
from pyopsman.core.basecomponent import BaseComponent


class Admin(BaseComponent):
    """
    Component primary class
    """
    base_url = 'admin'

    def __init__(self, requestor):
        logger.debug("Initializing component: Admin")
        super().__init__(requestor)
        self._token = UAAToken(requestor)


# #
# Component ancillary / supporting classes
class UAAToken(BaseComponent):
    # This code is an example only (non-functional)
    # Get the UAA token that the admin client will use
    base_url = '/'.join([Admin.base_url, 'uaa_token'])

    def __init__(self, *args, **kwargs):
        logger.debug("Initializing sub-component: UAAToken")
