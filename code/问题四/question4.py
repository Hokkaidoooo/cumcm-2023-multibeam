import math as m

h1 = 84.4 + 8869.44 * m.tan(m.radians(0.388))
h2 = 47.2 + 5722.96 * m.tan(m.radians(0.372))
h3 = 47.2 + 5599.82 * m.tan(m.radians(1.534))
h4 = 24.4 + 6383.61 * m.tan(m.radians(1.551))


def seek_wd(x, h, a):
    depth = h - x * m.sin(m.radians(a))
    l_width = (depth / m.cos(m.radians(60 + a))) * m.sin(m.radians(60)) * m.cos(m.radians(a))
    r_width = (depth / m.cos(m.radians(-60 + a))) * m.sin(m.radians(60)) * m.cos(m.radians(a))
    return depth, l_width, r_width


def find_x1(k):
    x1 = 0
    x1_values = []  # 存储x值的列表
    while True:
        depth, l_width, r_width = seek_wd(x1,h1,0.388)
        if x1 + r_width > k:
            break
        x1_values.append(x1)
        x1 += 0.9 * (l_width + r_width)
    return x1_values


def find_x2(k):
    x2 = 0
    x2_values = []  # 存储x值的列表
    while True:
        depth, l_width, r_width = seek_wd(x2,h2,0.372)
        if x2 + r_width > k:
            break
        x2_values.append(x2)
        x2 += 0.9 * (l_width + r_width)
    return x2_values


def find_x3(k):
    x3 = 0
    x3_values = []  # 存储x值的列表
    while True:
        depth, l_width, r_width = seek_wd(x3,h3,1.534)
        if x3 + r_width > k:
            break
        x3_values.append(x3)
        x3 += 0.9 * (l_width + r_width)
    return x3_values


def find_x4(k):
    x4 = 0
    x4_values = []  # 存储x值的列表
    while True:
        depth, l_width, r_width = seek_wd(x4,h4,1.551)
        if x4 + r_width > k:
            break
        x4_values.append(x4)
        x4 += 0.9 * (l_width + r_width)
    return x4_values

x1_values = find_x1(8869.44)
x2_values = find_x2(5722.96)
x3_values = find_x3(5599.82)
x4_values = find_x4(6373.61)
r1=[]
r2=[]
r3=[]
r4=[]
for i in range(len(x1_values)):
    r1.append(x1_values[i]/m.cos(m.radians(16.7)))
for i in range(len(x2_values)):
    r2.append(x2_values[i]/m.sin(m.radians(23.5)))
for i in range(len(x3_values)):
    r3.append(x3_values[i]/m.sin(m.radians(57.8)))
for i in range(len(x4_values)):
    r4.append(x4_values[i]/m.sin(m.radians(59.5)))

print(r1)
print(r2)
print(r3)
print(r4)
sum1=len(x1_values)*4878.25*5*1852*1852/(4878.25*8869.43)
sum2=len(x2_values)*6793.58*5*1852*1852/(6793.58*5722.96)
sum3=len(x3_values)*7840.05*5*1852*1852/(7840.05*5599.81)
sum4=len(x4_values)*5869.12*5*1852*1852/(5869.19*6383.61)
sum=sum1+sum2+sum3+sum4
print(sum)
