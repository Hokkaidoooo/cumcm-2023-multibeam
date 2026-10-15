import math as m


def f(m, point):
    b = point[1] - m * point[0]
    return b


m4 = m.tan(m.radians(30.49))
m1 = m.tan(m.radians(106.7))
m2 = m.tan(m.radians(66.5))
m3 = m.tan(m.radians(32.15))
point1 = (0, 0)
point2 = (0, 5 * 1852)
point3 = (2 * 1852, 2.5 * 1852)
point4 = (4 * 1852, 5 * 1852)
point5 = (4 * 1852, 0)
b11 = f(m1, point1)
b12 = f(m1, point3)
b21 = f(m2, point2)
b22 = f(m2, point4)
b31 = f(m3, point4)
b32 = f(m3, point5)
b41 = f(m4, point5)
b42 = f(m4, point3)
c11 = f(-1/m1, point1)
c12 = f(-1/m1, point2)
c21 = f(-1/m2, point3)
c22 = f(-1/m2, point4)
c31 = f(-1/m3, point4)
c32 = f(-1/m3, point3)
c41 = f(-1/m4, point5)
c42 = f(-1/m4, point1)
print((b11 - b12) / m.sqrt(1 + m1 ** 2))
print((b21 - b22) / m.sqrt(1 + m2 ** 2))
print((b31 - b32) / m.sqrt(1 + m3 ** 2))
print((b41 - b42) / m.sqrt(1 + m4 ** 2))
print((c11 - c12) / m.sqrt(1 + (1/m1) ** 2))
print((c21 - c22) / m.sqrt(1 + (1/m2) ** 2))
print((c31 - c32) / m.sqrt(1 + (1/m3) ** 2))
print((c41 - c42) / m.sqrt(1 + (1/m4) ** 2))
