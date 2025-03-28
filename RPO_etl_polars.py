import os
import polars as pl
import openpyxl
from openpyxl import load_workbook
# import time


# start_time = time.time()
#TODO: create some func to import xlsx file and some gui idk


def readCritalParams(excelfile):
    """read Mechanical Critical Parameters from Mechanical excel file"""
    #HARDCODED
    df = pl.read_excel(excelfile)
    critical_df = df[:6]
    critical_df_params_1 = critical_df.select(pl.nth([0])).rename({"Machanical Critical Parameters":"a"})
    critical_df_params_2 = critical_df.select(pl.nth([3])).rename({"__UNNAMED__5":"a"})
    critical_df_params = critical_df_params_1.vstack(critical_df_params_2)
    critical_df_params = critical_df_params.transpose()
    critical_df_value_1 = critical_df.select(pl.nth([1])).rename({"__UNNAMED__3":"b"})
    critical_df_value_2 = critical_df.select(pl.nth([5])).rename({"__UNNAMED__7":"b"})
    critical_df_value = pl.concat([critical_df_value_1, critical_df_value_2], how="vertical")
    critical_df_value = critical_df_value.transpose()
    critical = pl.concat([critical_df_params, critical_df_value], how="vertical")
    critical = critical.rename(critical.head(1).to_dicts().pop()).slice(1)
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
    critical = critical.rename(conv_dict)
    return critical

def readInspectionData(excelfile):
    """read Inspection Data from Mechanical excel file"""
    df = pl.read_excel(excelfile)
    mechanical_df = df[7:58]
    mechanical_df = mechanical_df.transpose()
    mechanical_df = mechanical_df.rename(mechanical_df.head(1).to_dicts().pop()).slice(1)
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
    mechanical_df = mechanical_df.rename(conv_dict)
    mechanical_df = mechanical_df.with_columns(
    pl.col('nominal').cast(pl.Float64),
    pl.col('tolerance').cast(pl.Float64),
    pl.col('usl').cast(pl.Float64),
    pl.col('lsl').cast(pl.Float64),
    pl.col('mean_stats').cast(pl.Float64),
    pl.col('stdev').cast(pl.Float64),
    pl.col('uc_lof_hvm_cpk_estimate').cast(pl.Float64),
    pl.col('hvm_cpk_point_estimate').cast(pl.Float64),
    pl.col('lc_lof_hvm_cpk_estimate').cast(pl.Float64),
    pl.col('min_stats').cast(pl.Float64),
    pl.col('max_stats').cast(pl.Float64),
    pl.col('range_stats').cast(pl.Float64),
    pl.col('count_stats').cast(pl.Float64)
)
    return mechanical_df

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
    # melted_df_cleaned = melted_df.drop_nans(subset=['Sample Value'])
    melted_df = melted_df.drop(['variable'])
    factSample = criticalParams.join(melted_df, how='cross', coalesce=True)
    factSample = factSample.rename({'Sample Value':'sample_value'})
    factSample = factSample.with_columns(
    pl.col('sample_value').cast(pl.Float64)
)
    factSample = factSample.drop_nans(subset=['sample_value'])
    return factSample


# inspect = readInspectionData(excelfile='Data\dummy.xlsx')
# print(inspect)
# critical = readCritalParams(excelfile='Data\dummy.xlsx')
# print(critical)
# print(factSam(inspect, critical))
# print(partDimension(inspect))

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

# print(rpo(exelFile='Data\dummy.xlsx'))
# polars_time = time.time() - start_time
# print(polars_time)

