# -*- coding: utf-8 -*-

__author__ = 'Manfred'
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment
from dbtest.views import class_info_query, temp_table_update
import random


class XlsxInfo:
    pass

    def __init__(self, _class_id, _scores):
        self.class_id = _class_id
        self.scores = _scores


def parse_xlsx(xlsx_filename):
    wb = load_workbook(filename=xlsx_filename, read_only=True)
    ws = wb.active

    # check whether the syntax remains the same from sample.xlsx
    if ws['A5'].value == '学号':
        # and str(ws['A6'].value).startswith('31')
        if ws['F3'].value is not None:
            course_id = ws['F3'].value
        else:
            print('[Syntax Error] course id not found!')
            return
        print('ok!')
    else:
        print('wrong format!')
        return

    start_row = 6
    end_row = ws.get_highest_row()
    score_info = []
    for row in range(start_row, end_row + 1):
        # print('processing row: {}'.format(row))
        if ws['A{}'.format(row)].value is None :
            break
        if ws['B{}'.format(row)].value is None :
            break
        if ws['C{}'.format(row)].value is None :
            break

        row_info = {'studentID': ws['A{}'.format(row)].value, 'score': float(ws['C{}'.format(row)].value)}
        # print(row_info)
        score_info.append(row_info)

    return XlsxInfo(course_id, score_info)


def get_demo_xlsx(course_id='0000000001'):
    wb = Workbook()
    ws = wb.active
    ws.title = 'score sheet 1'

    # todo: should get course id from front-end
    course_id = '0000000001'
    student_info = class_info_query(course_id)
    # student_info = views.class_info_query(course_id)


    # Formatting
    ws.append([])
    ws.append([])
    ws.merge_cells('A1:F2')
    center_align = Alignment(horizontal='center', vertical='center')

    # Initialization
    ws['A1'] = '浙江大学课程考试成绩记录表'
    ws['A1'].alignment = center_align

    ws.append(['教学班名称', '', '教师姓名', '', '课程编号'])
    ws.append([])
    ws.append(['学号', '姓名', '成绩', '备注'])


    # Filling the data.
    ws['F3'] = course_id

    for row in student_info:
        # for row in range(5, 5 + 10):
        # ws['A' + str(row)] = '312xxxxxxx'
        # ws['B' + str(row)] = 'Elder Wang'
        # ws['C' + str(row)] = '{0:.2f}'.format(random.Random().random() * 100)
        row_info = [row['studentID'], row['studentName']]
        ws.append(row_info)

    # Save the file
    ws.page_setup.fitToWidth = 1
    wb.save("./download/sample.xlsx")


def update_score(xlsx_filename):
    xlsx_info = parse_xlsx(xlsx_filename)
    # views.temp_table_update(xlsx_info.class_id, xlsx_info.scores)
    temp_table_update(xlsx_info.class_id, xlsx_info.scores)


# get_demo_xlsx()
# xlsx_info = parse_xlsx('sample.xlsx')
# print(xlsx_info.scores)
