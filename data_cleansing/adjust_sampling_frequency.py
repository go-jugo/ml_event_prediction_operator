import pandas as pd
import os
from monitoring.time_it import timing
import dask
import dask.dataframe as dd
from math import floor
#artifical_timestamp = 'global_timestamp'
#fill_missing_values = 'ffill'
from tools.series_list_to_df import series_list_to_df

def calc_resampling(series, sampling_frequency):
    return series.resample(sampling_frequency).last().shift(1)

@timing
def adjust_sampling_frequency(df, sampling_frequency='30S', v_dask=True):
    if v_dask:
        lazy_results=[]
        len_df_befor_adj = len(df)
        len_df_col_before_adj = len(df.columns)
        for col in df.columns:
            series = df[col]
            lazy_result = dask.delayed(calc_resampling)(series, sampling_frequency)
            lazy_results.append(lazy_result) 
        series_collection = dask.compute(*lazy_results)
        df = series_list_to_df(series_collection,  v_dask)         
        len_df_after_adj = len(df)
        len_df_col_after_adj = len(df.columns)
        print('rows: ' + str(len_df_befor_adj) + " >> " + str(len_df_after_adj))
        print('cols: ' + str(len_df_col_before_adj) + " >> " + str(len_df_col_after_adj))
    else:
        df = df.asfreq(sampling_frequency, method='ffill')
    return df