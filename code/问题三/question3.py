import math

mid_width=[]
def seek_wd(x):
    depth = 206.9594 - x * math.sin(math.radians(1.5))
    l_width = (depth / math.cos(math.radians(61.5))) * math.sin(math.radians(60)) * math.cos(math.radians(1.5))
    r_width = (depth / math.cos(math.radians(-58.5))) * math.sin(math.radians(60)) * math.cos(math.radians(1.5))
    return depth, l_width, r_width


def find_x(k):
    x = 341.374978
    x_values = []  # 存储x值的列表
    while True:
        depth, l_width, r_width = seek_wd(x)
        if x + r_width > k:
            break
        x_values.append(x)
        x += 0.9 * (l_width + r_width)
    return x_values


k = 4 * 1852  # 指定k的值
x_values = find_x(k)
sum=2*1852*len(x_values)
print(x_values)
print(sum)
