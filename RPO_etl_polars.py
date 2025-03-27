import os
import numpy as np
import polars as pl
import openpyxl
from openpyxl import load_workbook

#TODO: create some func to import xlsx file and some gui idk
#import wb
wb = load_workbook(filename='Data\dummy.xlsx')


def readCritalParams(wb):
    """read Mechanical Critical Parameters from Mechanical excel file"""
    #HARDCODED
    params_cells = ['A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7']
    params_values = [wb.active[cell].value for cell in params_cells]
    value_cells = ['D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7']
    values = [[wb.active[cell].value for cell in value_cells]]
    df = pl.DataFrame(values, schema=params_values, orient="row")
    conv_dict = {
        'Supplier Code and Name': 'supplier_codeand_name',
        'Supplier Factory Location':'supplier_factory_location',
        'WD Part Number': 'wd_part_number',
        'Commodity Code and Name': 'commodity_codeand_name',
        'Supplier Part Number and Revision': 'supplier_part_numberand_revision',
        'WD SQE (Development/Sustaining)': 'wdsqe',
        'QA Supervisor': 'qa_supervisor',
        'QA Inspector(s)': 'qa_inspector',
        'Date Inspected': 'date_inspected',
        'Submit Date': 'submit_date',
        'WD Program Name': 'wd_program_name',
        'Build Phase': 'build_phase'
    }
    df = df.rename(conv_dict)
    return df

def readInspectionData(wb):
    """read Inspection Data from Mechanical excel file"""
    #HARDCODED
    all_data = []
    columns_name = []
    ws = wb.active
    cell_range = ws['A9':'A59']
    for row in cell_range:
        for cell in row:
            columns_name.append(cell.value)
    for sheet in wb.worksheets:
        for column_range in range (4, 10):
            data = []
            for i in range(9, 60):
                if sheet.cell(column=column_range, row=9).value is None:
                    break
                data.append(sheet.cell(column=column_range, row=i).value)
            if data != []:
                all_data.append(data)
    df = pl.DataFrame(all_data, schema=columns_name)
    conv_dict = {
        'Critical Parameter Numbers à': 'critical_parameter_numbers',
        'Description': 'descriptions',
        'CP Type': 'cp_type',
        'Nominal': 'nominal',
        'Tolerance': 'tolerance',
        'USL': 'usl',
        'LSL': 'lsl',
        'MC Upper Limit': 'mc_upper_limit',
        'MC Lower Limit': 'mc_lower_limit',
        'Mean': 'mean_stats',
        'MC % Error': 'mc_percent_error',
        'Stdev': 'stdev',
        'UCL of HVM Cpk Estimate': 'uc_lof_hvm_cpk_estimate',
        'HVM Cpk Point Estimate': 'hvm_cpk_point_estimate',
        'LCL of HVM Cpk Estimate': 'lc_lof_hvm_cpk_estimate',
        'Min': 'min_stats',
        'Max': 'max_stats',
        'Range': 'range_stats',
        'Count': 'count_stats'
        }
    df = df.rename(conv_dict)
    return df

def supplierDimension(loadedCritical):
    dfSuppliers = loadedCritical[:, 0:2]
    return dfSuppliers

def partDimension(loadedCritical):
    dfParts = loadedCritical[:, 8:]
    return dfParts

def inspectionDimension(loadedCritical):
    dfInspect = loadedCritical[:, 2:8]
    return dfInspect

def descDimension(loaded_df):
    dfDescription = loaded_df[:, 0:2]
    return dfDescription

def statsDimension(loaded_df):
    dfStats = loaded_df[:, 2:19]
    return dfStats

def factSam(loaded_df, criticalParams):
    sampleColumns=[f'Sample #{i}' for i in range(1, 33)]
    melted_df = loaded_df.melt(
        id_vars=[col for col in loaded_df.columns if col not in sampleColumns],  # Column to keep as identifier
        value_vars=sampleColumns,  # Columns to collapse
        value_name='Sample Value'  # Name of the column containing the values
    )
    melted_df_cleaned = melted_df.drop_nans(subset=['Sample Value'])
    melted_df_cleaned = melted_df_cleaned.drop(['variable'])
    factSample = criticalParams.join(melted_df_cleaned, how='cross', coalesce=True)
    factSample = factSample.rename({'Sample Value':'sample_value'})
    return factSample


# inspect = readInspectionData(wb)
# critical = readCritalParams(wb)
# print(factSam(inspect, critical))
# print(statsDimension(inspect))
# print(inspectionDimension(critical))

# def dataQuality(loaded_df):
#     """check the data quality"""
#     #check whether loaded_df is empty
#     if loaded_df.empty:
#         print('No Data Extracted')
#         return False
#     #replace None with NaN
#     loaded_df = loaded_df.fillna(value=np.nan)
#     return loaded_df

def rpo(exelFile):
    #Importing the songs_df from the Extract.py
    load_df= readInspectionData(exelFile)
    critical = readCritalParams(exelFile)
    
    supplier = supplierDimension(critical)
    part = partDimension(critical)
    inspect = inspectionDimension(critical)

    desc = descDimension(load_df)
    stats = statsDimension(load_df)

    fact = factSam(load_df, critical)

    return supplier, part, inspect, desc, stats, fact

# rpo()
