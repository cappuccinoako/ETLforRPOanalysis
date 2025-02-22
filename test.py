import os
import pandas as pd
import openpyxl
from openpyxl import load_workbook

#import wb
wb = load_workbook(filename='Data\Machanical (Suspension).xlsx')

def readCritalParams(wb):
    #HARDCODED
    cells = ['A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7']
    values = [wb.active[cell].value for cell in cells]
    return values

