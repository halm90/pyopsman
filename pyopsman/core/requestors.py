#!/usr/bin/env python
"""
      Copyright 2019, Hal Moroff
      Licensed under the GNU General Purpose License.
"""
import requests
from requests import urllib3
from logzero import logger

#pylint: disable=bad-continuation, logging-not-lazy
#pylint: disable=too-few-public-methods, too-many-instance-attributes

class HttpRequestor():
    """
    Defines a basic REST API client to be extended by components.
    """

    def __init__(self, url: str, user: str, pwd: str,
                 *,
                 port: int = None,
                 version: str = None,
                 warn: bool = False):
        """
        Opsman constructor, requires information regarding the admin
        API server provided by opsman.  These are the base parameters.
        Additional parameters may be set by the component class.

        :param url:         the opsman admin url
        :param user:        admin API user
        :param pwd:         admin user password
        :param port:        TCP opsman target port
        :param warn:        enable/disable warnings
        """
        logger.debug("HttpRequestor initializing " +
                     "url: %s, port: %s, user: %s, pwd: <redacted>, " +
                     "version: %s, warn: %s",
                     url, str(port), user, version, warn)
        self._url = url
        parsed = urllib3.util.url.parse_url(self._url)
        self._version = version
        self._host = parsed.host
        # Port is given port or port in given url (given overrides)
        self._port = port or parsed.port
        self._user = user
        self._pwd = pwd
        self._warn = warn

    def request(self,
                url: str,
                *,
                port: int = None,
                data: dict = None,
                json: dict = None,
                method: str = 'GET',
                request_args: dict = {}) -> str:
        """ Builds a request and fetches its response from the targeted opsman.
        Returns a JSON encoded string. SSL verification is disabled.
        Simply put: this method works as a request.requests() wrapper.

        :param url:         the endpoint with all parameters to GET request
        :param port:        optional port
        :param data:        file-like object to send in the body of the request
        :param json:        json data to send in the body of the request
        :param method:      HTTP method (GET, POST, HEAD, DELETE, etc)
        """
        if not self._warn:
            logger.debug("HttpRequestor.request: disable warnings")
            requests.urllib3.disable_warnings()

        # Request port overrides object port for this request
        # If neither object nor request specifies port, none is used
        # If object specifies port but request speficies <= 0 then none is used
        port = port or self._port
        port = port if (port and port > 0) else None
        host = "{}:{}".format(self._host, port) if port else self._host
        parsed = urllib3.util.url.parse_url(self._url)
        self._port = port or parsed.port

        vsn = self._version if request_args.get('use_version', True) else None
        qry = parsed.query
        full_url = '{scheme}://{host}{ver}{path}/{call}{query}'.format(
                    scheme=parsed.scheme,
                    host=host,
                    ver="/api/{}".format(vsn) if vsn else "",
                    path=parsed.path if parsed.path else "",
                    call=url,
                    query="?{}".format(qry) if qry else ""
                   )
        logger.debug("HttpRequestor.request: %s", full_url)
        try:
            response = requests.request(verify=False, method=method,
                                        url=full_url,
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
