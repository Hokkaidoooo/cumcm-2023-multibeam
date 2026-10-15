% 读取xlsx文件
data = xlsread('D:\桌面\处理后数据2.xlsx');

% 提取x、y、z数据列
x = data(:, 1);
y = data(:, 2);
z = data(:, 3);

% 定义插值网格
[X, Y] = meshgrid(min(x):0.1:max(x), min(y):0.1:max(y));

% 进行插值
Z = griddata(x, y, z, X, Y, 'cubic');

% 绘制三维曲面图
figure;
surf(X, Y, Z, 'EdgeColor', 'none');
colormap parula; % 使用parula颜色映射
colorbar; % 添加颜色条

xlabel('X');
ylabel('Y');
zlabel('Z');
