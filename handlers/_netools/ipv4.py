
import re
import subprocess

from utils import Memory

class IPv4(object):
    REGX = re.compile('((?:\d{1,3}\.){3}\d{1,3}(?:\/(?:(?:\d{1,3}\.){3}\d{1,3}|\d+))?)')
    REGX_IPS = re.compile(r'^((?:\d{1,3}\.){3}\d{1,3})$')
    REGX_IPB = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    REGX_NET = re.compile(r'^((?:\d{1,3}\.){3}\d{1,3})(\/|\s+)?((?:\d{1,3}\.){3}\d{1,3}|\d+)?$')

    __slots__ = ('_addr', '_mask')

    def __init__(self, address, netmask=4294967295):
        assert address is not None and netmask is not None
        self._addr = None
        self._mask = None
        if isinstance(address, IPv4):
            self._addr = address.addr
            self._mask = address.mask
        elif isinstance(address, str):
            match = self.REGX_NET.search(address)
            assert match is not None
            address, sep, mask = match.groups()
            self._addr = self.address_to_int(address)
            if mask is not None:
                self._mask = self.netmask_to_int(mask)
        elif isinstance(address, (int, float)):
            assert 4294967295 >= int(address) >= 0
            self._addr = int(address)
        if self._mask is None:
            assert isinstance(netmask, (int, float, str))
            if isinstance(netmask, str):
                self._mask = self.netmask_to_int(netmask)
            else:
                assert 4294967295 >= int(netmask) >= 0
                self._mask = int(netmask)

    @property
    def ip_addr(self):
        return self.address_to_str(self.addr)

    @property
    def ip_mask(self):
        return self.address_to_str(self.mask)

    @property
    def addr(self):
        return self._addr

    @addr.setter
    def addr(self, value):
        self._addr = value

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, value):
        self._mask = value

    @property
    def network(self):
        return self.addr & self.mask

    @property
    def wildcard(self):
        return 4294967295 - self.mask

    @property
    def broadcast(self):
        return self.network | self.wildcard

    @property
    def count(self):
        return self.wildcard + 1

    @property
    def host_count(self):
        count = self.wildcard - 1
        return count if count > 0 else 1

    @property
    def first(self):
        network, broadcast = self.network, self.broadcast
        if network == broadcast or network == broadcast-1:
            return network
        return network + 1

    @property
    def last(self):
        network, broadcast = self.network, self.broadcast
        if network == broadcast or network == broadcast-1:
            return broadcast
        return broadcast - 1

    @property
    def cidr(self):
        return bin(self.mask)[2:].count('1')

    @property
    def octets(self):
        return list(map(int, self.addr.to_bytes(4, 'big')))

    @property
    def count_cidr(self):
        return (self.count, self.cidr)

    @property
    def type(self):
        if self.is_private(): return 'private'
        if self.is_localhost(): return 'localhost'
        if self.is_linklocal(): return 'link-local'
        return 'public'

    def __contains__(self, other):
        return IPv4(other).addr in range(self.network, self.broadcast + 1)

    def __eq__(self, other):
        other = IPv4(other)
        return self.addr == other.addr and self.mask == other.mask

    def __ne__(self, other):
        other = IPv4(other)
        return self.addr != other.addr or self.mask != other.mask

    def __gt__(self, other):
        return self.addr > IPv4(other).addr

    def __ge__(self, other):
        return self.addr >= IPv4(other).addr

    def __lt__(self, other):
        return self.addr < IPv4(other).addr

    def __le__(self, other):
        return self.addr <= IPv4(other).addr

    def __add__(self, other):
        if isinstance(other, int):
            if other < 0: other = 0
            elif other > 4294967295: other = 4294967295
        other = IPv4(other)
        if self.addr + other.addr > 4294967295:
            return IPv4(4294967295, self.mask)
        return IPv4(self.addr + other.addr, self.mask)

    def __sub__(self, other):
        if isinstance(other, int):
            if other < 0: other = 0
            elif other > 4294967295: other = 4294967295
        other = IPv4(other)
        if self.addr - other.addr < 0:
            return IPv4(0, self.mask)
        return IPv4(self.addr - other.addr, self.mask)

    def __div__(self, other):
        if not isinstance(other, (int, float)): other = 32
        elif other < 1: other = 1
        elif other > 32: other = 32
        if other < self.cidr: other = self.cidr
        count = IPv4(0, self.netmask_to_int(other)).wildcard + 1
        return [IPv4(self.network + count*i, self.netmask_to_int(other))
                for i in range((self.wildcard + 1) // count)]

    def __truediv__(self, other):
        return self.__div__(other)

    def __repr__(self):
        return "IPv4('%s/%d')" % (
            self.address_to_str(self.addr),
            self.netmask_to_cidr(self.mask))

    def __str__(self):
        return '%s/%d' % (
            self.address_to_str(self.addr),
            self.netmask_to_cidr(self.mask))

    def __iter__(self):
        return self.range(self.network, self.broadcast)

    def range(self, start, stop):
        for addr in range(start, stop + 1):
            yield IPv4(addr, self.mask)

    def ip_addresses(self):
        return [self.address_to_str(a) for a in range(self.network, self.broadcast + 1)]

    def is_private(self):
        return (184549375  >= self.addr >= 167772160)\
            or (2887778303 >= self.addr >= 2886729728)\
            or (3232301055 >= self.addr >= 3232235520)

    def is_localhost(self):
        return (2147483647 >= self.addr >= 2130706432)

    def is_linklocal(self):
        return (2852060927 >= self.addr >= 2851995904)

    def is_public(self):
        return not (self.is_private() or self.is_localhost() or self.is_linklocal())

    def info(self):
        return '\n'.join([
            ' address: %s' % self,
            ' netmask: %s' % self.address_to_str(self.mask),
            ' network: %s' % self.address_to_str(self.network),
            '   first: %s' % self.address_to_str(self.first),
            '    last: %s' % self.address_to_str(self.last),
            '  brcast: %s' % self.address_to_str(self.broadcast),
            'wildcard: %s' % self.address_to_str(self.wildcard),
            '   count: %d' % self.host_count,
            '    type: %s' % self.type,
            '\nbinary:',
            ' address: %s' % self.address_to_bin(self.addr),
            ' netmask: %s' % self.address_to_bin(self.mask),
            ' network: %s' % self.address_to_bin(self.network),
            '   first: %s' % self.address_to_bin(self.first),
            '    last: %s' % self.address_to_bin(self.last),
            '  brcast: %s' % self.address_to_bin(self.broadcast),
            'wildcard: %s' % self.address_to_bin(self.wildcard),
            '\ninteger:',
            ' address: %d' % self.addr,
            ' netmask: %d' % self.mask,
            ' network: %d' % self.network,
            '   first: %s' % self.first,
            '    last: %s' % self.last,
            '  brcast: %d' % self.broadcast,
            'wildcard: %d' % self.wildcard,
        ])

    @staticmethod
    def address_to_int(address):
        assert isinstance(address, str)
        octets = map(lambda x: int(x) if int(x) <= 255 else 255, address.split('.'))
        return int.from_bytes(octets, byteorder='big')

    @staticmethod
    def address_to_str(address):
        assert isinstance(address, int)
        return '.'.join(map(str, address.to_bytes(4, 'big')))

    @staticmethod
    def address_to_bin(address):
        assert isinstance(address, int)
        b = bin(address)[2:].zfill(32)
        return '.'.join([b[i*8:i*8+8] for i in range(4)])

    @staticmethod
    def netmask_to_int(netmask):
        if netmask is None:
            netmask = 32
        elif isinstance(netmask, str):
            if netmask.isdigit():
                netmask = int(netmask)
                netmask = netmask if 32 >= netmask >= 0 else 32
            elif IPv4.REGX_IPS.search(netmask):
                return IPv4.address_to_int(netmask)
            else: netmask = 32
        return (0xffffffff >> (32 - netmask)) << (32 - netmask)

    @staticmethod
    def netmask_to_cidr(netmask):
        assert isinstance(netmask, int)
        return bin(netmask)[2:].count('1')

    @staticmethod
    def findall(string):
        return list(map(IPv4, IPv4.REGX.findall(string)))

    @staticmethod
    def ping(address):
        (output, error) = subprocess.Popen(
            'ping -c 3 -w 3 %s' % address,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        ).communicate()
        if error: output = error.decode('utf8')
        else: output = output.decode('utf8')
        output = list(filter(lambda l: l, output.split('\n')))
        return '\n'.join(output)

    @staticmethod
    def trace(address):
        (output, error) = subprocess.Popen(
            'traceroute -w 1 -n %s' % address,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        ).communicate()
        if error: output = error.decode('utf8')
        else: output = output.decode('utf8')
        output = list(filter(lambda l: l, output.split('\n')))
        return '\n'.join(output)

    @staticmethod
    def whois(address):
        (output, error) = subprocess.Popen(
            'whois %s' % address,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        ).communicate()
        if error: output = error.decode('utf8')
        else: output = output.decode('utf8')
        output = list(filter(
            lambda l: l and not l.startswith('%') and not l.startswith('remark'),
            output.split('\n')
        ))
        return '\n'.join(output)
