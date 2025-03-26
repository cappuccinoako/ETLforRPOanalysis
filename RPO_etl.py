import os
import pandas as pd
import numpy as np

#TODO: create some func to import xlsx file and some gui idk


# def readCritalParams(wb):
#     """read Mechanical Critical Parameters from Mechanical excel file"""
#     #HARDCODED
#     cells = ['A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7']
#     values = [wb.active[cell].value for cell in cells]
#     return(values)

def readWB(path):
    """read workbook"""
    combined_df = pd.DataFrame()
    dfs = pd.read_excel(path, sheet_name=None)
    for key, value in dfs.items():
        skipped_value = value.iloc[7:58]
        skipped_value = skipped_value.transpose()
        new_header = skipped_value.iloc[0]
        skipped_value = skipped_value[1:]
        skipped_value.columns = new_header
        skipped_value = skipped_value.iloc[2:]
        combined_df = pd.concat([combined_df, skipped_value])
        combined_df = combined_df.dropna(how='all')
    return combined_df

# readWB(path='Data\Machanical (Suspension).xlsx')



def dataQuality(loaded_df):
    """check the data quality"""
    #check whether loaded_df is empty
    if loaded_df.empty:
        print('No Data Extracted')
        return False
    return loaded_df

def rpo(exelFile='Data\Machanical (Suspension).xlsx'):
    #Importing the songs_df from the Extract.py
    load_df=readWB(exelFile)
    dataQuality(load_df)
    return (load_df)

# rpo()
