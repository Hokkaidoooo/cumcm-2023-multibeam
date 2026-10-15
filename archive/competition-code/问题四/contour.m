data = xlsread('D:\桌面\处理后数据1.xlsx');
x = data(:, 1); % 获取第一列数据，即 x 坐标
y = data(:, 2); % 获取第二列数据，即 y 坐标
z = data(:, 3); % 获取第三列数据，即 z 坐标
[X, Y] = meshgrid(unique(x), unique(y));
Z = griddata(x, y, z, X, Y, 'cubic'); % 插值以填充网格上的值
contourf(X, Y, Z)
colorbar % 添加颜色条
xlabel('X 坐标')
ylabel('Y 坐标')
