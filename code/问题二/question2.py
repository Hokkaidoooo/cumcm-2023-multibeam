import math as m
import openpyxl

b_values = [0, 45, 90, 135, 180, 225, 270, 315]
ta_list = []
ia_list = []
d0 = [0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1]
d_values = []
width=[]
l_width_list = []
r_width_list = []

for i in range(len(d0)):
    d_values.append(d0[i] * 1852)


def angle(a, b):
    a1 = m.tan(m.radians(a)) / m.sqrt(1 + m.tan(m.radians(b)) ** 2 + m.tan(m.radians(a) ** 2))
    a2 = m.tan(m.radians(a)) / m.sqrt(1 + m.tan(m.radians(b + 90)) ** 2 + m.tan(m.radians(a) ** 2))
    ta = m.asin(a1)
    ia = m.asin(a2)
    return ta, ia


for b1 in b_values:
    travel_a, investigate_a = angle(1.5, b1)
    ta_list.append(travel_a)
    ia_list.append(investigate_a)


def seek_wd(d, a, b, c, p):
    if 90 < p < 270:
        depth = 120 - d * m.tan(a)
    else:
        depth = 120+d*m.tan(a)
    l_width = (depth / m.cos((c / 2) + b)) * m.sin(c / 2)*m.cos(b)
    r_width = (depth / m.cos(b - (c / 2))) * m.sin(c / 2)*m.cos(b)
    return l_width, r_width


for i in range(len(ta_list)):
    for d1 in d_values:
        l_wid, r_wid = seek_wd(d1, ta_list[i], ia_list[i], m.radians(120), b_values[i])
        l_width_list.append(l_wid)
        r_width_list.append(r_wid)

for i in range (len(l_width_list)):
    width.append(l_width_list[i]+r_width_list[i])


result = [width[i:i+8] for i in range(0, len(width), 8)]

workbook = openpyxl.load_workbook('result2.xlsx')
sheet = workbook['Sheet1']
for row_index, row_data in enumerate(result):
    for col_index, value in enumerate(row_data):
        sheet.cell(row=row_index + 3, column=col_index + 3, value=value)
workbook.save('result2.xlsx')