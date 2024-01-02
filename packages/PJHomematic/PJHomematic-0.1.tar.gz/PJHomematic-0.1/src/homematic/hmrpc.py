import time
import threading

from homematic import jsonrpc


class HMRPCClientWarning(Warning):
    pass


class HMRPCClient(jsonrpc.JSONRPCClient, threading.Thread):
    """Access to a Homematic appliance via JSON-RPC

    :param url: the base url of the Homematic appliance (i.e. http://192.168.1.200)
    :param username: the username (if login is to be performed immediatly)
    :param password: the password (if login is to be performed immediatly)
    :param auto_renew: renew the session key automatically
    """

    def __init__(self, url, username=None, password=None, auto_renew=False):
        jsonrpc.JSONRPCClient.__init__(self, f'{url}/api/homematic.cgi')
        threading.Thread.__init__(self)

        self.__session__ = None

        self.__auto_renew__ = auto_renew

        if username and password:
            self.login(username, password)

    def login(self, username:str, password:str):
        """Login if not already logged in
        the implementation of Session.login

        :param username: the username
        :param password: the password
        """

        if not self.__session__:
            self.__session__ = super(HMRPCClient, self).call('Session.login', username=username, password=password)

            if self.__auto_renew__:
                self.start()
        else:
            raise HMRPCClientWarning('Already logged in')

    def logout(self):
        """Logout of the homematic
        the implementation of Session.logout
        """

        if self.__session__:
            res = self.call('Session.logout')
            self.__session__ = None
            return res
        else:
            raise HMRPCClientWarning('Not logged in')

    def renew(self):
        """Renew the session key to stay logged in
        the implementation of Session.renew
        """

        if self.__session__:
            return self.call('Session.renew')
        else:
            raise HMRPCClientWarning('Not logged in')

    def call(self, method, /, **kwargs):
        if self.__session__:
            kwargs['_session_id_'] = self.__session__
            return super(HMRPCClient, self).call(method, **kwargs)
        else:
            raise HMRPCClientWarning('Not logged in')

    # def __del__(self):
    #     if self.__session__:
    #         self.logout()

    def run(self):
        time.sleep(10)
        while self.__session__:
            print('Renewing session...')
            self.renew()

            for i in range(60):
                if not self.__session__:
                    break

                time.sleep(1)

    def list_methods(self) -> dict:
        """Convenient method to retreive all available methods

        :return: dict of all methods with access level and help text"""

        methods = {}
        for m in self.call('system.listMethods'):
            if 'name' in m:
                name = m.pop('name')
                methods[name] = m
        return methods

    def method_help(self, name:str) -> dict:
        """Convenient method to retreive all help text of a method

        :param name: the full method name
        :return: help text"""

        return self.call('system.methodHelp', name=name)


if __name__ == '__main__':
    import sys
    from pprint import pp

    if len(sys.argv) > 3:
        addr = sys.argv[1]
        user = sys.argv[2]
        pwd = sys.argv[3]
    else:
        sys.exit(f'Try: {sys.argv[0]} IP-ADDRESS USERNAME PASSWORD')

    hmrc = HMRPCClient(addr, username=user, password=pwd)

    pp(hmrc.list_methods())

    # details = hmrc.call('Device.listAllDetail')
    # print('Type\tAddress\tName')
    # for d in details:
    #     print(f"{d['type']}\t{d['address']}\t{d['name']}")

    hmrc.logout()
