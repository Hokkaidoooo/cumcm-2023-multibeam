import math
import pandas  as pd
result =  []
def seek_wd(x):
    depth = 206.9594 - x * math.sin(math.radians(1.5))
    l_width = (depth / math.cos(math.radians(61.5))) * math.sin(math.radians(60)) * math.cos(math.radians(1.5))
    r_width = (depth / math.cos(math.radians(-58.5))) * math.sin(math.radians(60)) * math.cos(math.radians(1.5))
    return depth, l_width, r_width


def find_x(k,c):
    x = 341.374978
    x_values = []  # 存储x值的列表
    while True:
        depth, l_width, r_width = seek_wd(x)
        if x + r_width > k:
            break
        x_values.append(x)
        x += c * (l_width + r_width)
    return x_values

data = []
k = 4 * 1852  # 指定k的值
for step in range(80, 91):
    new_c = 0.01 * step
    x_values = find_x(k, new_c)
    total_distance = 2 * 1852 * len(x_values)
    data.append([1-new_c, total_distance])
    print(f"Step size: {new_c}, Total distance: {total_distance}")
df = pd.DataFrame(data, columns=['η', 's'])

# 将数据保存到Excel文件
df.to_excel('output.xlsx', index=False)