import json5
import requests


class JSONRPCError(RuntimeError):
    pass


class JSONRPCClient:
    def __init__(self, url):
        self.__url__ = url
        self.__msg_id__ = 0

    def get_base_content(self):
        res = requests.get(self.__url__, timeout=5)
        return res.text

    def call(self, method, /, **kwargs):
        try:
            self.__msg_id__ += 1

            res = requests.post(self.__url__,
                                json={'jsonrpc': '1.1',
                                      'method': method,
                                      'params': kwargs,
                                      'id': self.__msg_id__},
                                timeout=5,
                                )

            # Handle malformed JSON with trailing comma
            result = json5.loads(res.text)

            # Test for JSONRPC result
            if not (result and 'version' in result and 'id' in result and result['id'] == self.__msg_id__):
                raise JSONRPCError(f'Server did not respond with JSONRPC ({self.__url__})')

            # Raise exception from error result
            if 'error' in result and result['error']:
                raise JSONRPCError(f"{result['error']['message']} ({result['error']['code']})")
            else:
                return result['result']
        except requests.exceptions.ConnectTimeout:
            raise JSONRPCError(f'Connection timeout ({self.__url__})') from None


if __name__ == '__main__':
    import sys
    from pprint import pp

    if len(sys.argv) > 3:
        addr = sys.argv[1]
        user = sys.argv[2]
        pwd = sys.argv[3]
    else:
        sys.exit(f'Try: {sys.argv[0]} ADDRESS USERNAME PASSWORD')

    jrc = JSONRPCClient(f'{addr}/api/homematic.cgi')

    session = jrc.call('Session.login', username=user, password=pwd)

    pp(jrc.call('system.listMethods'))

    # details = jrc.call('Device.listAllDetail', _session_id_=session)
    # print('Type\tAddress\tName')
    # for d in details:
    #     print(f"{d['type']}\t{d['address']}\t{d['name']}")

    jrc.call('Session.logout', _session_id_=session)
