from ...dtype import *
from ...datahub import *



import pandas as pd
import numpy





def calc(df=None, x=None, y=None, cfg=None, dtypes=None, vars=None):
    """Call function based on the number of arguments (all, uni, bi)"""
    if df is not None and x is None and y is None:
        explore_univariate(df, dtypes,vars)
    elif x is not None and y is None:
        return calculate_univariate(df, x, cfg, dtypes)
    elif x is not None and y is not None:
        return calculate_bivariate(df, x, y, cfg, dtypes)
    else:
        raise ValueError("Invalid number of arguments")



def explore_univariate(df, dtypes, vars=None):
    """Explore univariate analysis for all columns"""
    from ..__init__ import eda
    if vars:
        dtypes = Configs.get_dtypes(df)
        selected_vars = [var for var, dtype in dtypes.items() if dtype == vars]
        
        print('dtypes',dtypes)
        print('sel.vars',selected_vars)

           
        for column in selected_vars:
            plot_instance = eda(df, column)
            plot_instance.show()
        
    else:
        for column in df.columns:
            plot_instance = eda(df, column)
            plot_instance.show()


def calculate_univariate(df, x, cfg, dtypes):
    """Calculate univariate analysis for a single variable"""
    col = df[x]
    dtype = get_dtype_info(col,x, dtypes)
    data = cont_comps(col, cfg, dtype)
    
    if dtype[0] == 'categorical' and data['MISSING'] > 0:
        col = col.dropna()
    
    return DataHub(col=col, data=data, variable_type=dtype[0])


def calculate_bivariate(df, x, y, cfg, dtypes):
    """Calculate bivariate analysis for two variables"""
    col1, dtype1 = get_dtype_info(df[x], dtypes)
    col2, dtype2 = get_dtype_info(df[y], dtypes)
    
    print(dtype1, dtype2)

    if dtype1[0] == 'continuous' and dtype2[0] == 'continuous':
        return DataHub(col1=col1, col2=col2, data=None, variable_type='biv_con')
    elif (dtype1[0] == 'continuous' and dtype2[0] == 'categorical') or (dtype2[0] == 'continuous' and dtype1[0] == 'categorical'):
        return DataHub(col1=col1, col2=col2, data=None, variable_type='biv_con_cat')
    elif dtype1[0] == 'categorical' and dtype2[0] == 'categorical':
        return DataHub(col1=col1, col2=col2, data=None, variable_type='biv_cat')
    else:
        print('compute_bivariate -> biv in progress')
        return None


def get_dtype_info(col,var_name, dtypes):
    """Get dtype information for a column"""
    if dtypes is None:
        return determine_variable_type(col)
    else:
        dtype_info = dtypes.get(var_name, determine_variable_type(col)[0])
        col_un = col.nunique()
        return dtype_info, col_un, col_un / len(col)



def cont_comps(ser = None, cfg = None, dtype = None):
    # ser = pd.series -> df.column => series
    
    def series_memory_usage(col, deep=False):
        total_memory_bytes = col.memory_usage(deep)

        if total_memory_bytes < 1_000_000:
            total_memory_mb = total_memory_bytes / (1024)
            return f"{total_memory_mb:.2f} KB"
        else:
            total_memory_mb = total_memory_bytes / (1024 ** 2)
            return f"{total_memory_mb:.2f} MB"

    dt = dtype[0]
    #print(dtype)
    if dt == 'unknown':
        return ser
    if isinstance(ser, np.ndarray):
        return ser
    else:
        data = {
            'TOTAL': ser.size,
            'VALUES': ser.count(),
            'VALUES_P': np.round((ser.count() / ser.size) * 100, 2),
            'MISSING': ser.isna().sum(),
            'MISSING_P': np.round((ser.isna().sum() / ser.size) * 100, 2),
            'DISTINCT': dtype[1],
            'DISTINCT_P': np.round(dtype[2] * 100, 2),
            '': '',
            'MEMORY': series_memory_usage(ser),
            'DTYPE': ser.dtype,
            'v_type': dt
        }
    
    
    if dt == 'categorical':
        #print('categorical is comming next')
        None
    elif dt == 'continuous':
        data.update({
            'MAX': np.round(np.nanmax(ser), 2),
            '95%': np.round(np.nanpercentile(ser, 95), 2),
            'Q3': np.round(np.nanpercentile(ser, 75), 2),
            'AVG': np.round(np.nanmean(ser), 1),
            'MEDIAN': np.round(np.nanmedian(ser), 1),
            'Q1': np.round(np.nanpercentile(ser, 25), 1),
            '5%': np.round(np.nanpercentile(ser, 5), 2),
            'MIN': np.round(np.nanmin(ser), 2),
            'RANGE': np.round(np.nanmax(ser) - np.nanmin(ser), 1),
            'IQR': np.round(np.nanpercentile(ser, 75) - np.nanpercentile(ser, 25), 1),
            'STD': np.round(np.nanstd(ser), 1),
            'VAR': np.round(np.nanvar(ser)),
            ' ': ' ',
            'KURT.': np.round(ser.kurtosis(), 3),
            'SKEW': np.round(ser.skew(), 3),
            'SUM': np.round(np.nansum(ser), 3)
        })

    elif dt == 'text': 
        w_len = ser.str.len()
        data.update({
        'w_len' : w_len,
        'Max length' : w_len.max(),
        'Mean length' : np.round(w_len.mean(),2),
        'Min length' : w_len.min()
        })

    elif dt == 'datetime':
        data.update({
            'MAX': ser.max(),
            # '95%': np.round(np.nanpercentile(ser, 95), 2),
            # 'Q3': np.round(np.nanpercentile(ser, 75), 2),
            # 'AVG': np.round(np.nanmean(ser), 1),
            # 'MEDIAN': np.round(np.nanmedian(ser), 1),
            # 'Q1': np.round(np.nanpercentile(ser, 25), 1),
            # '5%': np.round(np.nanpercentile(ser, 5), 2),
            'MIN': ser.min(),
            # 'RANGE': np.round(np.nanmax(ser) - np.nanmin(ser), 1),
            # 'IQR': np.round(np.nanpercentile(ser, 75) - np.nanpercentile(ser, 25), 1),
            # 'STD': np.round(np.nanstd(ser), 1),
            # 'VAR': np.round(np.nanvar(ser)),
            # ' ': ' ',
            # 'KURT.': np.round(ser.kurtosis(), 3),
            # 'SKEW': np.round(ser.skew(), 3),
            # 'SUM': np.round(np.nansum(ser), 3)
        })
    else:
        None
    
    return data

# data = np.random.randn(1000)  # Replace this with your dataset
# #compute(data,data).get('col')
# compute(data,data).get('data')
# compute(data,data).get('variable_type')

