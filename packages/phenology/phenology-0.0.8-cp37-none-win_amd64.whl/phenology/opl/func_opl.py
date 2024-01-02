import numpy as np
import multiprocessing as mp
from tqdm import tqdm
from datetime import datetime, timedelta
from joblib import Parallel, delayed
from .api_opl_v2 import opl_api


def opl_for_parallel(args):
    y, x, max_month, index = args
    result = opl_api(y, x, max_month=max_month)
    return index, result
  

def get_opl(y:np.ndarray, x:np.ndarray, **kwargs):
    """
    Calculate the optimal pre-season length for specified variables.

    Parameters:
    - y: np.ndarray, shape (rows, cols, years, 1) or (years, 1)
      Target variable data over the years. such as phenological data at an annual scale.

    - x: np.ndarray, shape (rows, cols, months, vars) or (months, vars)
      Explanatory variables data at a monthly scale, covering one more year than y data (months = 12 * (years + 1)).

    Keyword Arguments (kwargs):
    - n_jobs: int, default --> mp.cpu_count()
      number of jobs to run in parallel. 
    
    - max_month: int, default 6
      Maximum pre-season length calculated forward from the current month.

    - target_vars: list, default None
      variable names for calculating optimal pre-season length. Default --> x.columns.to_list().

    Returns: 
    - for multiple data (eg. x.ndim == 4)
      result: np.ndarray, shape (rows, cols, 6, len(target_vars))
      In the 3rd dimension of result, the 6 elements are ['n', 'r', 'ci95lower', 'ci95upper', 'p-val', 'opl'], where opl is the optimal pre-season length.
      
    - for single data (eg. x.ndim == 2)
      result: pd.DataFrame
      Columns: ['n', 'r', 'CI95%', 'p-val', 'opl', 'var', 'index'], where opl is the optimal preseason length.
    """
    

    n_jobs = kwargs.get('n_jobs', mp.cpu_count())
    max_month = kwargs.get('max_month', 6)
 
    
    if x.ndim == 2:
      if y.ndim == 1:
        y = y.reshape((-1, 1))
      return opl_api(y, x, max_month=max_month)
    

    rows, cols, months, vars  = x.shape
    x = x.reshape((rows * cols, months, vars)) 
    y = y.reshape((rows * cols, -1, 1))

    args_list = [[y[index], x[index], max_month, index] for index in range(rows * cols)]
    
    print('Start parallel computation, parallel processing cores: ', n_jobs)
    
    result = np.full((rows * cols, vars), np.nan)
    with mp.Pool(processes=n_jobs) as pool:
        for index, res in tqdm(pool.imap_unordered(opl_for_parallel, args_list), ncols=100, total=len(args_list)):
            result[index] = res
    result = result.reshape(rows, cols, -1).astype(np.float32)
                      
    return result


# -------------------------------------------------------------------------- #

    
def single_mean(x, opl, pheno):
    """
    x: shape (months, )
    opl: number
    pheno: number
    """
    k_indices = np.arange(12, len(x), 12) # (months//12-1, )
    start_indices = (k_indices + pheno - opl - 1).astype(int) # (months//12-1, )
    end_indices = (k_indices + pheno).astype(int) # (months//12-1, )
    mask = (np.arange(len(x)) >= start_indices[:, np.newaxis]) & (np.arange(len(x)) < end_indices[:, np.newaxis])
    x_masked = np.where(mask, x, np.nan) 
    resarr = np.nanmean(x_masked, axis=1) # shape (months//12-1, )
    
    return resarr


def seasonal_mean(x_arr: np.ndarray, opl_arr: np.ndarray, pheno_arr: np.ndarray):
    """
    Calculate pre-seasonal mean from input arrays.

    Parameters:
    - x_arr (np.ndarray): Climate variable array (months, rows, cols), where months is a multiple of 12.
    - opl_arr (np.ndarray): The optimal preseason length (rows, cols).
    - pheno_arr (np.ndarray): Phenological dates (rows, cols), typically multi-year average in day of year (1-365) or month (1-12).

    Returns:
    - result (np.ndarray): Pre-seasonal mean (months//12-1, rows, cols).

    """

    if np.nanmax(pheno_arr) > 12: # if the value of pheno_arr is the "day of year" (1-365), then convert it to the month
        pheno_arr[~np.isnan(pheno_arr)] = np.array([(datetime(2023, 1, 1) + timedelta(days=eos - 1)).month for eos in pheno_arr[~np.isnan(pheno_arr)]])

    months, rows, cols = x_arr.shape
 
    nn_indices = np.where(~np.isnan(opl_arr) & ~np.isnan(pheno_arr)) # nn_indices, means the indices of non-NaN elements
    nn_opl = opl_arr[nn_indices] # shape (806542,)
    nn_pheno = pheno_arr[nn_indices] # shape (806542,)
    nn_x = x_arr[:, nn_indices[0], nn_indices[1]] # shape (504, 806542)

    # slice the data
    args_list = [(nn_x[:, i], nn_opl[i], nn_pheno[i]) for i in range(nn_opl.shape[0])]
    res = np.array(Parallel(n_jobs=-1)(delayed(single_mean)(x, opl, pheno) for x, opl, pheno in tqdm(args_list))) # shape (806542, 41)
    result = np.full((months//12-1, rows, cols), np.nan)
    result[:, nn_indices[0], nn_indices[1]] = res.swapaxes(0, 1)

    return result
 
    

    
            
