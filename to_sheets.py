from __future__ import print_function
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

def numberToLetters(q):
    q = q - 1
    result = ''
    while q >= 0:
        remain = q % 26
        result = chr(remain+65) + result;
        q = q//26 - 1
    return result

def spreadsheet_setup():
	SCOPE = ["https://spreadsheets.google.com/feeds"]
	credentials = ServiceAccountCredentials.from_json_keyfile_name('../creds/client_secret.json', SCOPE)

	gc = gspread.authorize(credentials)

	return gc

def updatesheet(spreadsheet_name, sheet_name,updatedf,start_cell,length_new_data):
	
	# start_cell = int(start_cell)
	# length_new_data = int(length_new_data)
	gc = spreadsheet_setup()


	print("Data to sheets")
	num_lines, num_columns = updatedf.shape
	spreadsheet = gc.open(spreadsheet_name)
	worksheet = spreadsheet.worksheet(sheet_name)
	
	columns = updatedf.columns.values.tolist()
	endcolumn = numberToLetters(len(columns))
	
	num_lines = start_cell+num_lines-1

	

	cell_list = worksheet.range('a1:'+endcolumn+'1')
	# cell_list = worksheet.range('a1:'+endcolumn+'1')

	for cell in cell_list:
		cell.value = columns[cell.col -len(columns) -1]

	worksheet.update_cells(cell_list)



	print(start_cell)
	cell_list = worksheet.range('a'+str(start_cell)+':'+numberToLetters(num_columns)+str(num_lines))

	for cell in cell_list:
	    # val = updatedf.ix[cell.row,cell.col-1]
	    val = updatedf.iloc[cell.row-start_cell-1,cell.col-1]
	    # cell.value = (val.encode('utf-8') if type(val) is str else val)
	    cell.value = val

	worksheet.update_cells(cell_list)
