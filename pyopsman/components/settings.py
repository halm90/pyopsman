#!/usr/bin/env python
"""
      Copyright 2019, Hal Moroff
      Licensed under the GNU General Purpose License.
"""
from logzero import logger
from pyopsman.core.basecomponent import BaseComponent

#pylint: disable=too-few-public-methods

class Settings(BaseComponent):
    """
    Component primary class

    Dealing with Settings

    """
    base_url = 'settings'

    def __init__(self, requestor):
        logger.debug("Initializing component: settings")
        super().__init__(requestor)

        self.rbac = RBAC(requestor)
        self.banner = Banner(requestor)
        self.syslog = Syslog(requestor)
        self.ssl = SSL(requestor)


class RBAC(BaseComponent):
    """
    """
    base_url = '/'.join([Settings.base_url, 'rbac'])

    def __init__(self, requestor):
        logger.debug("Initializing Settings sub-component: RBAC")
        super().__init__(requestor)


class Banner(BaseComponent):
    """
    """
    base_url = '/'.join([Settings.base_url, 'banner'])

    def __init__(self, requestor):
        logger.debug("Initializing Settings sub-component: Banner")
        super().__init__(requestor)


class Syslog(BaseComponent):
    """
    """
    base_url = '/'.join([Settings.base_url, 'syslog'])

    def __init__(self, requestor):
        logger.debug("Initializing Settings sub-component: Syslog")
        super().__init__(requestor)


class SSL(BaseComponent):
    """
    """
    base_url = '/'.join([Settings.base_url, 'ssl_certificate'])

    def __init__(self, requestor):
        logger.debug("Initializing Settings sub-component: SSL")
        super().__init__(requestor)
