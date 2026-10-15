import numpy as np

# 三个点的坐标
point1 = np.array([0, 0, -24.4])
point2 = np.array([0, 5*1852, -84.4])
point3 = np.array([2*1852, 2.5*1852, -47.2])
point4 = np.array([4*1852, 5*1852, -65.2])
point5 = np.array([4*1852, 0, -197.2])
# 计算两个向量
vector1 = point2 - point3
vector2 = point1 - point3
vector3 = point5 - point3
vector4 = point4 - point3


# 计算平面法向量
n1_vector = np.cross(vector1, vector2)
n2_vector = np.cross(vector1, vector4)
n3_vector = np.cross(vector3, vector4)
n4_vector = np.cross(vector2, vector3)
# 计算平面与 xoy 平面的夹角
plane1_xoy = np.arccos(
    np.dot(n1_vector, np.array([0, 0, 1])) / (np.linalg.norm(n1_vector) * np.linalg.norm([0, 0, 1])))
plane2_xoy = np.arccos(
    np.dot(n2_vector, np.array([0, 0, 1])) / (np.linalg.norm(n2_vector) * np.linalg.norm([0, 0, 1])))
plane3_xoy = np.arccos(
    np.dot(n3_vector, np.array([0, 0, 1])) / (np.linalg.norm(n3_vector) * np.linalg.norm([0, 0, 1])))
plane4_xoy = np.arccos(
    np.dot(n4_vector, np.array([0, 0, 1])) / (np.linalg.norm(n4_vector) * np.linalg.norm([0, 0, 1])))
# 计算平面法向量在 xoy 平面上的投影
projection_n1_xoy = np.array([n1_vector[0], n1_vector[1], 0])
projection_n2_xoy = np.array([n2_vector[0], n2_vector[1], 0])
projection_n3_xoy = np.array([n3_vector[0], n3_vector[1], 0])
projection_n4_xoy = np.array([n4_vector[0], n4_vector[1], 0])
# 计算法向量在 x 轴上的投影与 x 轴的夹角
angle1_projection_x_axis = np.arccos(np.dot(projection_n1_xoy, np.array([1, 0, 0])) / (
            np.linalg.norm(projection_n1_xoy) * np.linalg.norm([1, 0, 0])))
angle2_projection_x_axis = np.arccos(np.dot(projection_n2_xoy, np.array([1, 0, 0])) / (
            np.linalg.norm(projection_n2_xoy) * np.linalg.norm([1, 0, 0])))
angle3_projection_x_axis = np.arccos(np.dot(projection_n3_xoy, np.array([1, 0, 0])) / (
            np.linalg.norm(projection_n3_xoy) * np.linalg.norm([1, 0, 0])))
angle4_projection_x_axis = np.arccos(np.dot(projection_n4_xoy, np.array([1, 0, 0])) / (
            np.linalg.norm(projection_n4_xoy) * np.linalg.norm([1, 0, 0])))

# 将弧度转换为度
angle_plane1_xoy_deg = np.degrees(plane1_xoy)
angle_plane2_xoy_deg = 180 - np.degrees(plane2_xoy)
angle_plane3_xoy_deg = np.degrees(plane3_xoy)
angle_plane4_xoy_deg = np.degrees(plane4_xoy)
angle1_projection_x_axis_deg = np.degrees(angle1_projection_x_axis)
angle2_projection_x_axis_deg = np.degrees(angle2_projection_x_axis)
angle3_projection_x_axis_deg = np.degrees(angle3_projection_x_axis)
angle4_projection_x_axis_deg = np.degrees(angle4_projection_x_axis)
print("平面与xoy的夹角（度）：", angle_plane1_xoy_deg, angle_plane2_xoy_deg,angle_plane3_xoy_deg ,angle_plane4_xoy_deg)
print("平面法向在xoy上的投影与x轴的夹角（度）：", angle1_projection_x_axis_deg,angle2_projection_x_axis_deg,angle3_projection_x_axis_deg,angle4_projection_x_axis_deg)
