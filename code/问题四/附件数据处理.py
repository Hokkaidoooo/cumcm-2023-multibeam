import pandas as pd

# 读取原始Excel文件
df = pd.read_excel(r'D:\桌面\附件.xlsx')

# 获取横坐标和纵坐标的列名
x_label = df.columns[1:]
y_label = df.iloc[1:, 0].tolist()

# 创建新的DataFrame来存储转换后的数据
df_transformed = pd.DataFrame(columns=['X', 'Y', 'Z'])

# 遍历原始数据，将横坐标、纵坐标和z值添加到新的DataFrame中
for i, y in enumerate(y_label):
    for j, x in enumerate(x_label):
        z = df.iloc[i+1, j+1]
        df_transformed = pd.concat([df_transformed, pd.DataFrame({'X': [x], 'Y': [y], 'Z': [z]})], ignore_index=True)

# 保存转换后的数据到新的Excel文件
df_transformed.to_excel('处理后数据1.xlsx', index=False)
