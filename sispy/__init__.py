# -*- coding: utf-8 -*-

"""Client library for interacting with the SIS RESTful API"""

__version__ = (0, 4, 5)
__author__ = 'Anton Gavrik'

import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

LOG = logging.getLogger(__name__)
LOG.addHandler(NullHandler())

# attempt to use ujson to handle json, fall back to stdlib json if unavailable
try:
    import ujson as json
except ImportError:
    import json

class Response(object):
    """Represent the client's response.

    Depending on the calling method behaves either like a dictionary 
    for methods returning a single object e.g. .get() or like a list
    for methods returning multiple objects e.g. .fetch_all()

    """
    def __init__(self, result, meta=None):
        self._result = result    
        self._meta = meta 

    def __len__(self):
        return len(self._result)

    def __getitem__(self, key):
        return self._result[key]

    def __setitem__(self, key, value):
        self._result[key] = value

    def __delitem__(self, key):
        del self._result[key]

    def __iter__(self):
        return iter(self._result)

    def __contains__(self, item):
        """x in Response 

        """     
        if item in self._result:
            return True
        else:
            return False
        
    def __str__(self):
        return str(self._result)

    def to_dict(self):
        """Returns a dict representaton of the object
        
        """
        if not isinstance(self._result, dict):
            raise Error('{0} is not a dict-like object'.format(
                self.__class__.__name__))
        return dict(self._result)

    def to_list(self):
        """Returns a list representation of the object
        
        """
        if not isinstance(self._result, list):
            raise Error('{0} is not a list-like object'.format(
                self.__class__.__name__))
        return list(self._result)

class Meta(object):
    """Represents meta data in the clients response."""

    def __init__(self, headers):
        """    
        args:
            headers: dict containing http headers

        Derived attributes:
            .total_count
                is created and is set to the value of 'x-total-count' header 
                if it's present. 
        """           
        self.headers = headers

        if 'x-total-count' in self.headers:
            self.total_count = int(self.headers['x-total-count'])

class Error(Exception):
    """SIS Error"""

    def __init__(self, error, http_status_code=None, 
                 code=None, response_dict={}):
        """
        args:
            error: string representing error description
            code: string representing error code
            http_status_code: HTTP status code
            response_dict: dictionary representing encoded 
                http response body 
        """
        self.error = error
        self.http_status_code = http_status_code
        self.code = code
        self.response_dict = response_dict

        super(Error, self).__init__(self.__str__())

    def __repr__(self):
        return ('Error(http_status_code="{http_status_code}", '
                'error={error}, code="{code}", '
                'response_dict={response_dict})'
                .format(error=json.dumps(self.error),
                        code=self.code,
                        http_status_code=self.http_status_code,
                        response_dict=json.dumps(str(self.response_dict))))

    def __str__(self):
        return self.error

from .client import Client

