import xlrd
import unicodecsv


def xls2csv(xls_filename,output_filename):

    wb = xlrd.open_workbook(xls_filename)
    sh = wb.sheet_by_index(0)

    fh = open(output_filename,"wb")
    csv_out = unicodecsv.writer(fh, encoding='utf-8')

    for row_number in xrange (sh.nrows):
        csv_out.writerow(sh.row_values(row_number))

    fh.close()
    return output_filename

