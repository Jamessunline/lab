# from IPy import IP


# # var = IP('10.0.0.0/24')
# # print(var.len())
# # for ip in var:
# # 	print(ip)


# # print('192.168.13.249' in IP('192.168.0.0/16'))

# a = input('input your ip address:')
# ip = IP(a)
# print(ip.iptype())

import dns.resolver

A = dns.resolver.query('www.baidu.com', 'A')   # A,MX, CNAME 三种类型
for i in A.response.answer:
	print(i)
