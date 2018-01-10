import xlrd
import unicodecsv


student_list_file = "student_list.xlsx"

def xls2csv(xls_filename):

    wb = xlrd.open_workbook(xls_filename)
    sh = wb.sheet_by_index(0)

    fh = open("students.csv","wb")
    csv_out = unicodecsv.writer(fh, encoding='utf-8')

    for row_number in xrange (sh.nrows):
        csv_out.writerow(sh.row_values(row_number))

    fh.close()


xls2csv(student_list_file)