'''
    This method takes excel file and saves as csv
'''

from kivy.logger import Logger

import xlrd, unicodecsv

def xls2csv(xls_filename, output_filename):
    wb = xlrd.open_workbook(xls_filename)
    sh = wb.sheet_by_index(0)

    fh = open(output_filename, "wb")
    csv_out = unicodecsv.writer(fh, encoding="utf-8")

    for row_number in xrange(sh.nrows):
        csv_out.writerow(sh.row_values(row_number))

    fh.close()

    Logger.info("excel_to_csv: Excel successfully saved as csv")

    return output_filename

