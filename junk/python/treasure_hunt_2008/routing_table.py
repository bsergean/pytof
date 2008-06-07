#!/usr/bin/env python
'''
http://treasurehunt.appspot.com/confirmation?email_address=bsergean%40gmail.com&question_name=network&confirmation_code=b1e723
'''

class RouteNode:
    def __init__(self, node, ip, from1, to1, from2, to2, cidr, to3, default):
        self.node = node
        self.ip = ip
        self.from1 = from1
        self.to1 = to1
        self.from2 = from2
        self.to2 = to2
        self.cidr = cidr
        self.to3 = to3
        self.default = default

        self.subnet = '.'.join(self.cidr.split('.')[:3])
    
    def route(self, address):
        if address == self.from1: return self.to1
        if address == self.from2: return self.to2
        if address.startswith(self.subnet): return self.to3
        return self.default

def read_route_table():
    routing_table = {}
    for l in open('routing_table.txt').read().splitlines():
        # A     108.232.169.113     175.1.125.160 => 236.0.3.152    212.8.88.45 => 175.78.28.176    26.2.153.0/24 => 218.136.143.134    175.1.125.160
        node,   ip,                 from1,       dum, to1,          from2,     dum, to2,            cidr,       dum, to3,              default = l.split()

        routing_table[node] = RouteNode(node, ip, from1, to1, from2, to2, cidr, to3, default)
    return routing_table

routing_table = read_route_table()

first_node = 'F'
cur_node = first_node
last_node_ip = '227.209.242.47'

node = [n.node for n in routing_table.values() if n.ip == last_node_ip][0]
print 'Last node will be:', node
last_node = node[0]

route = []
route.append(cur_node)

while cur_node != last_node:
    
    rn = routing_table[cur_node]
    next_node_ip = rn.route(last_node_ip)
    print 'Next ip:', next_node_ip

    cur_node = [n.node for n in routing_table.values() if n.ip == next_node_ip][0]
    print 'Next node:', cur_node

    route.append(cur_node)
        
print ''.join(route)
