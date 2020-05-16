import socket as s


s1 = s.socket(s.AF_INET, s.SOCK_DGRAM)
s1.bind(('127.0.0.1', 1298))

s2 = s.socket(s.AF_INET, s.SOCK_DGRAM)
s2.bind(('127.0.0.1', 1298))




