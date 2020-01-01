#!/usr/bin/env python
"""
      Copyright 2019, Hal Moroff
      Licensed under the GNU General Purpose License.
"""
from logzero import logger
from pyopsman.core.requestors import HttpRequestor

class BaseComponent():
    """
    Defines the base class for each component.

    Inheriting classes may override base_url for extensions to
    the primary (opsman) endpoint url used when the client was
    created.  If there's no override then the getattr override
    will append the extension based on the client request
    (ie: "<myclient>.<foobar>" will append "/foobar".

    Inheriting classes may also override "request_args" with
    a dictionary of arguments to be used by the request call
    in the HttpRequestor.
    """
    base_url = None
    request_args = dict()

    def __init__(self, requestor: HttpRequestor, **kwargs):
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
        return self._requestor.request(**request, request_args=self.request_args)

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

        required_params = {'method': 'GET',
                           'data': None,
                           'json': None
                          }
        request = {k: parameters.pop(k,v) for k,v in required_params.items()}
        # TODO
        #request.update(parameters.pop('<extension??>', None)

        # url = {base_url}[/{endpoint}]
        url = '/'.join(filter(None, (self.__class__.base_url, endpoint)))

        # Append query filter(s) (if any)
        for index, (key, value) in enumerate(parameters.items()):
            url += '{symbol}{key}={value}'.format(symbol='&' if index
                                                             else '?',
                                                   key=key, value=value)
        request['url'] = url
        logger.debug("BaseComponent._build_request: built %s", request)
        return request
