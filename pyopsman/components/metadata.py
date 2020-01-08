#!/usr/bin/env python
"""
      Copyright 2019
      Licensed under the GNU General Purpose License.
"""
from logzero import logger
from pyopsman.core.basecomponent import BaseComponent

#pylint: disable=too-few-public-methods

class Metadata(BaseComponent):
    """
    Component primary class

    Dealing with metadata

    """
    base_url = 'metadata'

    def __init__(self, requestor):
        logger.debug("Initializing component: Metadata")
        super().__init__(requestor)
        self.migrate = Migrate(requestor)


class Migrate(BaseComponent):
    """
    """
    base_url = '/'.join([Metadata.base_url, 'migrate'])

    def __init__(self, requestor):
        logger.debug("Initializing Metadata sub-component: Migrate")
        super().__init__(requestor)
