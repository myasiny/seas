import json
import xlrd

student_list_file = "student_list.xlsx"
lecture_name = "ENGR102"

def xlsToJson(xls_file, lecture_name):
    workbook = xlrd.open_workbook(xls_file)
    worksheet = workbook.sheet_by_index(0)

    data = []
    keys = [v.value for v in worksheet.row(0)]
    for row_number in range(worksheet.nrows):
        if row_number == 0:
            continue
        row_data = {}
        for col_number, cell in enumerate(worksheet.row(row_number)):
            row_data[keys[col_number]] = cell.value
        data.append(row_data)

    with open("students.json", 'w') as json_file:
        json_file.write(json.dumps({lecture_name: data}))
xlsToJson(student_list_file,lecture_name)