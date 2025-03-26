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

def loadWB(path):
    """load and cleann data from excel file"""
    combined_df = pd.DataFrame()
    dfs = pd.read_excel(path, sheet_name=None)
    for key, value in dfs.items():
        #skipped 6 rows
        skipped_value = value.iloc[7:58]
        skipped_value = skipped_value.transpose()
        #get header
        new_header = skipped_value.iloc[0]
        skipped_value = skipped_value[1:]
        skipped_value.columns = new_header
        #remove first 2 empty row
        skipped_value = skipped_value.iloc[2:]
        #combine
        combined_df = pd.concat([combined_df, skipped_value])
    combined_df = combined_df.dropna(how='all')
    #drop that annoying index column
    combined_df = combined_df.reset_index(drop=True)
    combined_df = combined_df.rename_axis(None, axis=1)
    combined_df = combined_df.rename(columns={'Critical Parameter Numbers à':'Critical Parameter Numbers'})
    return combined_df

def getSample(loaded_df):
    dfSample = loaded_df.iloc[:, [0] + list(range(19, 51))]
    melted_df = dfSample.melt(
        id_vars=['Critical Parameter Numbers'],  # Column to keep as identifier
        value_vars=[f'Sample #{i}' for i in range(1, 33)],  # Columns to collapse
        value_name='Sample Value'  # Name of the column containing the values
    )
    melted_df_cleaned = melted_df.dropna(subset=['Sample Value'])
    return melted_df_cleaned

# loaded_df = loadWB(path='Data\Machanical (Suspension).xlsx')
# print(getSample(loaded_df))


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
