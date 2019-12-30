#!/usr/bin/env python
# -*- coding:utf8 -*-
#
#      Copyright 2019, Hal Moroff
#
#      Licensed under the GNU General Purpose License.
#
import requests
from requests import urllib3
from logzero import logger


class HttpRequestor():
    """
    Defines a basic REST API client to be extended by components.
    """

    def __init__(self, url: str, user: str, pwd: str,
                 *,
                 port: int = None,
                 version: str = None,
                 warn: bool = False):
        """ Opsman constructor, requires information regarding the admin
        API server provided by opsman

        :param url:         the opsman admin url
        :param user:        admin API user
        :param pwd:         admin user password
        :param port:        TCP opsman target port
        :param warn:        enable/disable warnings
        """
        logger.debug("HttpRequestor initializing " +
                     "url: %s, port %s, user: %s, pwd: <redacted>, " +
                     "version: %s, warn: %s",
                     url, str(port), user, version, warn)
        self._url = url
        self._port = port
        parsed = urllib3.util.url.parse_url(self._url)
        if self._port and not parsed.port:
            self._url = "{}://{}:{}{}".format(parsed.scheme,
                                              parsed.host,
                                              self._port,
                                              parsed.path if parsed.path else ""
                                             )
        self._url += "/api/{}".format(version) if version else ""
        self._user = user
        self._pwd = pwd
        self._warn = warn

    def request(self, url: str, *,
                data: dict=None, json: dict = None, method: str = 'GET') -> str:
        """ Builds a request and fetches its response from the targeted opsman.
        Returns a JSON encoded string. SSL verification is disabled.
        Simply put: this method works as a request.requests() wrapper.

        :param req_url: the endpoint with all parameters to GET request
        :param data:    file-like object to send in the body of the request
        :param json:    json data to send in the body of the request
        :param method:  HTTP method (GET, POST, HEAD, DELETE, etc)
        """
        if not self._warn:
            logger.debug("HttpRequestor.request: disable warnings")
            requests.urllib3.disable_warnings()

        api_call = '{url}/{call}'.format(url=self._url,
                                         call=url
                                        )
        logger.debug("HttpRequestor.request: %s", api_call)
        try:
            response = requests.request(verify=False, method=method,
                                        url=api_call,
                                        data=data,
                                        json=json,
                                        auth=(self._user, self._pwd),
                                       )
        except Exception as exn:
            logger.error("HttpRequestor.request exception: %s", exn)
            raise

        logger.debug("HttpRequestor.request: response status code %d",
                     response.status_code)
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                # GET /system/version
                logger.debug("HttpRequestor.request: ValueError <%s>",
                             response.text)
                return response.text
            except Exception as exn:
                logger.debug("HttpRequestor.request: json error <%s>", exn)
                raise
        else:
            logger.error("HttpRequestor.request failed %d: " +
                         "reason <%s> url <%s>",
                         response.status_code, response.reason,
                         response.request.url)
            return {'reason': response.reason,
                    'status_code': response.status_code,
                    'url': response.request.url}

