#!/usr/bin/env python
"""
      Copyright 2019, Hal Moroff
      Licensed under the GNU General Purpose License.
"""
from logzero import logger
from pyopsman.core.basecomponent import BaseComponent


class Admin(BaseComponent):
    """
    Component primary class

    Administrative / authentication.

    TODO:
    This component was implemented as part of the architecture bring-up and
    is likely not necessary at all in the final implementation.
    """
    base_url = 'admin'

    def __init__(self, requestor):
        logger.debug("Initializing component: Admin")
        super().__init__(requestor)
