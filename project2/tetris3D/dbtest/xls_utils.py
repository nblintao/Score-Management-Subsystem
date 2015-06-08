__author__ = 'manfred'
from openpyxl import *
from openpyxl.styles import Alignment
from dbtest import views


def get_demo_xlsx():
    wb = Workbook()
    ws = wb.active
    ws.title = 'score sheet 1'

    # todo: should get course id from front-end
    course_id = '0000000001'
    student_info = views.class_info_query(course_id)
    print(student_info)
    # Formatting
    ws.merge_cells('A1:F2')
    center_align = Alignment(horizontal='center', vertical='center')

    # Initialization
    ws['A1'] = '浙江大学课程考试成绩记录表'
    ws['A1'].alignment = center_align

    # print(ws['A1'].column)

    ws.append(['教学班名称', '', '教师姓名', '', '课程编号'])
    ws.append([])
    ws.append(['学号', '姓名', '成绩', '备注'])

    # Filling the data.
    for row in student_info:
        # ws['A' + str(row)] = '312xxxxxxx'
        # ws['B' + str(row)] = 'Elder Wang'
        # ws['C' + str(row)] = '{0:.2f}'.format(random.Random().random() * 100)
        row_info = [row['studentID'], row['studentName']]
        ws.append(row_info)

    # Save the file
    ws.page_setup.fitToWidth = 1
    wb.save("sample.xlsx")

get_demo_xlsx()