# CSV 2 XLSX Converter
# Ron Egli - github.com/smugzombie

import os
import glob
import csv, sys
from xlsxwriter.workbook import Workbook

csvfile = sys.argv[1]
workbook = Workbook(csvfile + '.xlsx')
worksheet = workbook.add_worksheet()
with open(csvfile, 'rb') as f:
    reader = csv.reader(f)
    for r, row in enumerate(reader):
        for c, col in enumerate(row):
            worksheet.write(r, c, col)
workbook.close()
