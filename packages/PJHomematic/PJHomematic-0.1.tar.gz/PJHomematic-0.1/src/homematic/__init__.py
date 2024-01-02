"""An interface to the Homematic JSON-API"""

import functools
import lxml.etree

from . import hmrpc
from .__version__ import __version__

__author_name__ = 'Andreas Schawo'
__author_email__ = 'andreas@schawo.de'
__copyright__ = 'Copyright 2023 by Andreas Schawo,licensed under CC BY-SA 4.0'
__proj_name__ = 'PJHomematic'

__description__ = 'An interface to the Homematic JSON-API'


def __api_method__(self, cname: str, fname: str, /, **kwargs):
    return self.__api_call__(f'{cname}.{fname}', **kwargs)


# noinspection PyPep8Naming
class __API_Class__:
    def __init__(self, parent):
        self.__parent__: Homematic = parent

    def __api_call__(self, method, /, **params):
        return self.__parent__.call(method, **params)


class Homematic(hmrpc.HMRPCClient):
    """This class is an abstarction of the Homematic JSON-API
    On intantiation it will build the class hierachy and methods dynamically

    To access API methods i.e. 'Device.listAllDetail' or 'Device.setName'

    >>> import homematic
    >>> hm = homematic.Homematic('http://homematic', username='user', password='pwd')
    >>> details = hm.Device.listAllDetail()
    >>> hm.Device.setName(id='1234', name='Special device')
    >>> hm.logout()

    You must not use _session_id_ parameter to a method.
    The abstarction layer already cares about session management.

    :param url: the base url of the Homematic appliance (i.e. http://192.168.1.200)
    :param username: the username (if login is to be performed immediatly)
    :param password: the password (if login is to be performed immediatly)
    :param auto_renew: renew the session key automatically
    """

    def __init__(self, url: str, **kwargs):
        super().__init__(url, **kwargs)

        self.__api_doc__: dict = {}

        self.__init_classes__()

    def __init_classes__(self):
        html = lxml.etree.fromstring(self.get_base_content(), lxml.etree.HTMLParser())

        api_table = html.find('body').find('table')

        self.__api_doc__ = {}

        first = True
        for row in api_table.iterfind('tr'):
            if first:
                first = False
                continue

            cols = [c.text for c in row.iterfind('td')]

            self.__api_doc__[cols[0]] = {
                'level': cols[1],
                'help': cols[2],
                'params': cols[3].strip().split()
            }

        for m in self.__api_doc__:
            cname, mname = m.split('.')

            if mname in ('login', 'logout', 'renew'):
                continue

            if cname in self.__dir__():
                api_class = self.__getattribute__(cname)
            else:
                api_class = __API_Class__(self)
                self.__setattr__(cname, api_class)

            api_class.__setattr__(mname, functools.partial(__api_method__, api_class, cname, mname))

    @property
    def api_doc(self) -> dict:
        """Get the API documentation as dict for class.method

        You must not use _session_id_ parameter to a method.
        The abstarction layer already cares about session management.
        The existance of _session_id_ only hints, if a login is required."""
        return self.__api_doc__

    def call(self, method, /, **params):
        return super().call(method, **params)
