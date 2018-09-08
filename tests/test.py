
import os
import re
import json
import sys
sys.path.insert(0, '/home/roman/development/ebot-dev/')

os.environ['TAC_USERNAME'] = 'eqmread'
os.environ['TAC_PASSWORD'] = 'ghjcnjtrev'

from handlers._netools import IPv4, Device

def json_serial(obj):
    if isinstance(obj, IPv4):
        return str(obj)
    return obj

routers = [
    {'name': 'Санк-Петербург', 'address': '10.78.0.95', 'vendor': 'cisco'},
]

min = 30

free_filters = [IPv4(0, i).count_cidr for i in range(24, min+1)]
free_subnets = {}

for router in routers:
    router = Device(**router).init()
    router.login()

    cmd = router.cmd('sh run | s bgp', timeout=30)
    for bgp_network in router.BGP_NETWORKS.findall(cmd):
        print(bgp_network)
        if bgp_network[0].startswith('10.'): continue
        network = IPv4('/'.join(bgp_network))
        free_subnets[str(network)] = {a[1]:[] for a in free_filters}

        for subnet in network.div(24):
            cmd = router.cmd('sh ip route %s %s longer-prefixes' %\
                (subnet.ip_addr, subnet.ip_mask),
                timeout=30)
            dots = ['.'] * 256
            for c, r in router.IP_ROUTES.findall(cmd):
                r = IPv4(r)
                if r.wild+1 > 256: continue
                for i in range(r.wild+1): dots[r.octets[-1]+i] = c
            dots = ''.join(dots)
            for c, cidr in free_filters:
                items = [dots[i*c:i*c+c] for i in range(256//c)]
                for i, item in enumerate(items):
                    if item == '.'*c:
                        addr = re.sub('\d+\/\d+', str(c*i), str(subnet))
                        if not any(addr in a for a in free_subnets[str(network)][cidr]):
                            free_subnets[str(network)][cidr].append(IPv4('%s/%d' % (addr, cidr)))

print(json.dumps(free_subnets, indent=4, default=json_serial))
for network, subnets in free_subnets.items():
    for cidr, nets in subnets.items():
        if len(nets) > 0:
            print('%s /%d: %d' %(network, cidr, len(nets)))
