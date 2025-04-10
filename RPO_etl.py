import os
import pandas as pd
# import time


# start_time = time.time()



#TODO: create some func to import xlsx file and some gui idk
def loadCriticalParams(path):
    """idk"""
    # Read all required columns
    df = pd.read_excel(
        path, 
        usecols=[0, 5, 3, 7],
        skiprows=1,
        nrows=6, 
        header=None
    )
    # Combine parameters
    parameters = pd.concat([df[0], df[5]], ignore_index=True)
    values = pd.concat([df[3], df[7]], ignore_index=True)
    
    # Create DataFrame
    mechanicalCritalParamsdf = pd.DataFrame({
        'Parameter': parameters,
        'Value': values
    })
    mechanicalCritalParamsdf = mechanicalCritalParamsdf.transpose()
    #get header
    new_header = mechanicalCritalParamsdf.iloc[0]
    mechanicalCritalParamsdf = mechanicalCritalParamsdf[1:]
    mechanicalCritalParamsdf.columns = new_header
    #remove that annoying index
    mechanicalCritalParamsdf = mechanicalCritalParamsdf.reset_index(drop=True)
    mechanicalCritalParamsdf = mechanicalCritalParamsdf.rename_axis(None, axis=1)
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
    # convert the columns into a new datframe
    critialRenamed = mechanicalCritalParamsdf.rename(columns=conv_dict)
    
    return critialRenamed

def loadWB(path):
    """load and clean data from excel file"""
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
    conv_dict = {
        'Critical Parameter Numbers': 'critical_parameter_numbers',
        'Description': 'descriptions',
        'CP Type': 'cp_type',
        'Nominal': 'nominal',
        'Tolerance': 'tolerance',
        'USL': 'usl',
        'LSL': 'lsl',
        'MC Upper Limit': 'mc_upper_limit',
        'MC Lower Limit': 'mc_lower_limit',
        'Mean': 'mean_stats',
        'MC % Error': 'mc_percent_error_real',
        'Stdev': 'stdev',
        'UCL of HVM Cpk Estimate': 'uc_lof_hvm_cpk_estimate',
        'HVM Cpk Point Estimate': 'hvm_cpk_point_estimate',
        'LCL of HVM Cpk Estimate': 'lc_lof_hvm_cpk_estimate',
        'Min': 'min_stats',
        'Max': 'max_stats',
        'Range': 'range_stats',
        'Count': 'count_stats'
        }
    # convert the columns into a new datframe
    combined_df = combined_df.rename(columns=conv_dict)
    return combined_df

def supplierDimension(loadedCritical):
    dfSuppliers = loadedCritical.iloc[:, 0:2]
    return dfSuppliers

def partDimension(loadedCritical):
    dfParts = loadedCritical.iloc[:, 8:]
    return dfParts

def inspectionDimension(loadedCritical):
    dfInspect = loadedCritical.iloc[:, 2:8]
    return dfInspect

def descDimension(loaded_df):
    dfDescription = loaded_df.iloc[:, 0:2]
    return dfDescription

def statsDimension(loaded_df):
    dfStats = loaded_df.iloc[:, 2:19]
    return dfStats

def factSam(loaded_df, criticalParams):
    sampleColumns=[f'Sample #{i}' for i in range(1, 33)]
    melted_df = loaded_df.melt(
        id_vars=[col for col in loaded_df.columns if col not in sampleColumns],  # Column to keep as identifier
        value_vars=sampleColumns,  # Columns to collapse
        value_name='Sample Value'  # Name of the column containing the values
    )
    melted_df_cleaned = melted_df.dropna(subset=['Sample Value'])
    melted_df_cleaned = melted_df_cleaned.drop(columns='variable')
    factSample = criticalParams.merge(melted_df_cleaned, how='cross')
    factSample = factSample.rename(columns={'Sample Value':'sample_value'})
    return factSample




# loaded_df = loadWB(path='Data\dummy.xlsx')
# critial = loadCriticalParams(path='Data\dummy.xlsx')
# print(statsDimension(loaded_df))
# print(factSam(loaded_df, critial))
# print(inspectionDimension(loadCriticalParams(path='Data\dummy.xlsx')))



# def dataQuality(loaded_df):
#     """check the data quality"""
#     #check whether loaded_df is empty
#     if loaded_df.empty:
#         print('No Data Extracted')
#         return False
#     return loaded_df

def rpo(exelFile):
    #Importing the songs_df from the Extract.py
    load_df= loadWB(exelFile)
    critical = loadCriticalParams(exelFile)
    
    supplier = supplierDimension(critical)
    part = partDimension(critical)
    inspect = inspectionDimension(critical)

    desc = descDimension(load_df)
    stats = statsDimension(load_df)

    fact = factSam(load_df, critical)

    return supplier, part, inspect, desc, stats, fact

# rpo(exelFile='Data\dummy.xlsx')
# pandas_time = time.time() - start_time
# print(pandas_time)
