"""
excel_to_csv
============

`excel_to_csv` converts excel file to csv file without changing content.
"""

import unicodecsv
import xlrd

__author__ = "Ali Emre Oz"


def xls2csv(xls_filename, output_filename):
    """
    This method converts given excel file into csv file.
    :param xls_filename: It is path and name of excel file to convert.
    :param output_filename: It is path and name of csv file to save.
    :return:
    """

    wb = xlrd.open_workbook(xls_filename)
    sh = wb.sheet_by_index(0)

    fh = open(output_filename, "wb")
    csv_out = unicodecsv.writer(fh,
                                encoding="utf-8"
                                )

    for row_number in xrange(sh.nrows):
        csv_out.writerow(sh.row_values(row_number))

    fh.close()
