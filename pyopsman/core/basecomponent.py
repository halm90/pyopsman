#!/usr/bin/env python
# -*- coding:utf8 -*-
#
#      Copyright 2019, Hal Moroff
#
#      Licensed under the GNU General Purpose License.
#
from logzero import logger
from pyopsman.core.requestors import HttpRequestor

class BaseComponent():
    """Defines the base class for each component."""
    base_url = None

    def __init__(self, requestor: HttpRequestor):
        """ Constructor only contains an instance of HttpRequestor.

        :param requestor:   instance of an HTTP request manager
        :rtype:             BaseComponent
        """
        logger.debug("BaseComponent initializing")
        self._requestor = requestor

    def __call__(self, **parameters: dict):
        """ Gets a properly built request and queries the Requestor.

        :param parameters:  URL query parameters
        :rtype:             BaseComponent
        """
        request = self._build_request(**parameters)
        return self._requestor.request(**request)

    def __getattr__(self, endpoint: str):
        # closure, expects keyword argument unpacking:
        def handler(**parameters):
            return self._inner_getattr(endpoint, **parameters)
        return handler

    def _inner_getattr(self, endpoint: str, **parameters: dict):
        """ Gets a properly built request and queries the Requestor.

        :param endpoint:    the endpoint path (without parameters)
        :param parameters:  URL query parameters
        :rtype:             BaseComponent
        """
        request = self._build_request(endpoint, **parameters)

        return self._requestor.request(**request)

    def _build_request(self, endpoint: str = '', **parameters: dict) -> dict:
        """ Builds a data structure that contains a properly built URL (from
        the optional endpoint argument and unpacked parameters), the HTTP
        request method, a data key and a json key.

            URL example:
                base_url/endpoint?param1=value1&param2=value2

        :param endpoint:    the endpoint path (without parameters)
        :param parameters:  URL query parameters
        :rtype:             dict
        """

        request = {'method': parameters.pop('method', 'GET'),
                   'data': parameters.pop('data', None),
                   'json': parameters.pop('json', None)
                  }

        # url = {base_url}[/{endpoint}]
        url = '/'.join(filter(None, (self.__class__.base_url, endpoint)))

        for index, (key, value) in enumerate(parameters.items()):
            url += '{symbol}{key}={value}'.format(symbol='&' if index
                                                             else '?',
                                                   key=key, value=value)
        request['url'] = url
        logger.debug("BaseComponent._build_request: built %s", request)
        return request
