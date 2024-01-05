#import os
#os.environ['CUDA_PATH'] = "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.7"

import pandas as pd
import numpy as np
import time
from collections import deque
from scipy import linalg
from numpy.linalg import pinv
import warnings
warnings.filterwarnings("ignore")
import math
import random
from termcolor import colored
import time 

try :
    import cupy as cp  # tested on cupy-cuda117==10.6.0
except : 
    pass # Either code is executed only using CPU or it will it will throw some error regarding library CUPY.

global myDevice
myDevice = 'CPU'
# Functions required

## Conversion Fn
def ten2mat(tensor, mode):
    return np.reshape(np.moveaxis(tensor, mode, 0), (tensor.shape[mode], -1), order = 'F')
    
def mat2ten(mat, dim, mode):
    index = list()
    index.append(mode)
    for i in range(dim.shape[0]):
        if i != mode:
            index.append(i)
    return np.moveaxis(np.reshape(mat, list(dim[index]), order = 'F'), 0, mode)
    
def folding_3D(Unfold_Tens, unfol_dim , other_dim_seq, Tens_shape):
    a = [0,1,2]
    items = deque(a)
    items.rotate(unfol_dim) 
    a_up= list(items)
    X = Unfold_Tens.reshape(Tens_shape[unfol_dim], Tens_shape[other_dim_seq[0]],Tens_shape[other_dim_seq[1]]).transpose(a_up[0], a_up[1], a_up[2])    
    return (X)
    
def unfolding_3D(Tens, unfol_dim, other_dim_seq ):
    X = Tens.transpose(unfol_dim, other_dim_seq[0], other_dim_seq[1])
    X= X.reshape(Tens.shape[unfol_dim], Tens.shape[other_dim_seq[0]] * Tens.shape[other_dim_seq[1]])
    return (X)

def convert_numpy_to_cupy(dictionary, myDevice):
    if myDevice == 'GPU':
        converted_dict = {}
        for key, value in dictionary.items():
            if isinstance(value, np.ndarray):
                converted_dict[key] = cp.array(value)
            else:
                converted_dict[key] = value
        return converted_dict


# Used to create NaN
def replace_decimal_with_nan(x):
    if x == int(x):
        return x
    else:
        decimal_count = len(str(x).split('.')[1])
        return np.nan if decimal_count > 1 else x
    

## Function 

def add_missing(Original_Dataframe, Tens_shape, miss_type, zero_as_missing, missing_rate, missing_rate_val, block_window):
    # replace zero with 0.01 and define dense tensor
    dense_tensor = folding_3D(np.array(Original_Dataframe.replace(0,0.01)), unfol_dim = 0 , other_dim_seq = [1,2], Tens_shape = Tens_shape).transpose(1,2,0) #
    # get dimensions of the dense tensor
    dim1, dim2, dim3 = dense_tensor.shape
    #random seed
    np.random.seed(1000)
    #add sparsity to the dense tensor to define sparse tensor for random and non-random missing scenarios
    if miss_type == 'NM': #Non-random missing scenario
        sparse_tensor = dense_tensor * np.round(np.random.rand(dim1, dim3) + 0.5 - missing_rate)[:, None, :]
        sparse_tensor_val = dense_tensor * np.round(np.random.rand(dim1, dim3) + 0.5 - missing_rate_val)[:, None, :]
        sparse_tensor_val = np.where(sparse_tensor == 0.0, dense_tensor, sparse_tensor_val)
        sparse_tensor_val = np.where(dense_tensor == 0.01, dense_tensor, sparse_tensor_val)
    if miss_type == 'RM': #random missing scenario
        sparse_tensor = dense_tensor * np.round(np.random.rand(dim1, dim2, dim3) + 0.5 - missing_rate)
        sparse_tensor_val = dense_tensor * np.round(np.random.rand(dim1, dim2, dim3) + 0.5 - missing_rate_val)
        sparse_tensor_val = np.where(sparse_tensor == 0, dense_tensor, sparse_tensor_val)
        sparse_tensor_val = np.where(dense_tensor == 0.01, dense_tensor, sparse_tensor_val)
    if miss_type == 'BM': 
        dim1, dim2, dim3 = dense_tensor.shape
        dim_time = dim2 * dim3
        vec = np.random.rand(int(dim_time / block_window))
        temp = np.array([vec] * block_window)
        vec = temp.reshape([dim2 * dim3], order = 'F')
        sparse_tensor = mat2ten(ten2mat(dense_tensor, 0) * np.round(vec + 0.5 - missing_rate)[None, :], np.array([dim1, dim2, dim3]), 0)
        sparse_tensor_val = mat2ten(ten2mat(dense_tensor, 0) * np.round(vec + 0.5 - missing_rate_val)[None, :], np.array([dim1, dim2, dim3]), 0)
        sparse_tensor_val = np.where(sparse_tensor == 0, dense_tensor, sparse_tensor_val)
        sparse_tensor_val = np.where(dense_tensor == 0.01, dense_tensor, sparse_tensor_val)
        
    if miss_type == 'MM2':
        dim1, dim2, dim3 = dense_tensor.shape
        dim_time = dim2 * dim3
        vec = np.random.rand(int(dim_time / block_window))
        temp = np.array([vec] * block_window)
        vec = temp.reshape([dim2 * dim3], order = 'F')
        sparse_tensor = mat2ten(ten2mat(dense_tensor, 0) * np.round(vec + 0.5 - missing_rate[0])[None, :], np.array([dim1, dim2, dim3]), 0)
        sparse_tensor = sparse_tensor * np.round(np.random.rand(dim1, dim2, dim3) + 0.5 - missing_rate[1])
        sparse_tensor = sparse_tensor * np.round(np.random.rand(dim1, dim3) + 0.5 - missing_rate[2])[:, None, :]
        sparse_tensor_val = mat2ten(ten2mat(dense_tensor, 0) * np.round(vec + 0.5 - missing_rate_val[0])[None, :], np.array([dim1, dim2, dim3]), 0)
        sparse_tensor_val = sparse_tensor_val * np.round(np.random.rand(dim1, dim2, dim3) + 0.5 - missing_rate_val[1])
        sparse_tensor_val = sparse_tensor_val * np.round(np.random.rand(dim1, dim3) + 0.5 - missing_rate_val[2])[:, None, :]
        sparse_tensor_val = np.where(sparse_tensor == 0, dense_tensor, sparse_tensor_val)
        sparse_tensor_val = np.where(dense_tensor == 0.01, dense_tensor, sparse_tensor_val)

    if miss_type == 'MM':    
        sparse_tensor = dense_tensor * np.round(np.random.rand(dim1, dim2, dim3) + 0.5 - missing_rate[0])
        sparse_tensor = sparse_tensor * np.round(np.random.rand(dim1, dim3) + 0.5 - missing_rate[1])[:, None, :]
        sparse_tensor_val = dense_tensor * np.round(np.random.rand(dim1, dim2, dim3) + 0.5 - missing_rate_val[0])
        sparse_tensor_val = sparse_tensor_val * np.round(np.random.rand(dim1, dim3) + 0.5 - missing_rate_val[1])[:, None, :]
        sparse_tensor_val = np.where(sparse_tensor == 0, dense_tensor, sparse_tensor_val)
        sparse_tensor_val = np.where(dense_tensor == 0.01, dense_tensor, sparse_tensor_val)
    #Unfold sparse tensor to along day mode to get a corrupted dataframe similar to Original Dataframe
    if zero_as_missing == True:
        Dataframe_corrupted10 = pd.DataFrame(unfolding_3D(sparse_tensor, 2, [0,1]),columns = Original_Dataframe.columns, index = Original_Dataframe.index).replace(0,np.nan).replace(0.01,np.nan)
        Dataframe_corrupted10_val = pd.DataFrame(unfolding_3D(sparse_tensor_val, 2, [0,1]),columns = Original_Dataframe.columns, index = Original_Dataframe.index).replace(0,np.nan)
    if zero_as_missing == False:
        Dataframe_corrupted10 = pd.DataFrame(unfolding_3D(sparse_tensor, 2, [0,1]),columns = Original_Dataframe.columns, index = Original_Dataframe.index).replace(0,np.nan)
        Dataframe_corrupted10_val = pd.DataFrame(unfolding_3D(sparse_tensor_val, 2, [0,1]),columns = Original_Dataframe.columns, index = Original_Dataframe.index).replace(0,np.nan)
    if zero_as_missing == True:
        #replace 0.01 in dense tensor by 0
        dense_tensor[dense_tensor == 0.01] = 0
        #replace 0.01 in sparse tenosr by 0
        sparse_tensor[sparse_tensor == 0.01] = 0
    return(dense_tensor, sparse_tensor, sparse_tensor_val, Dataframe_corrupted10,Dataframe_corrupted10_val, dim1, dim2, dim3)


## Funciton group 1
def Data_Structuring(X1, TrueDf):
    X = (X1[0] + X1[1])/2
    W = np.array((X - X + 1).replace(np.nan, 0))
    RW1 = np.array((X1[0] - X1[0]).replace(np.nan, 1))
    RW_val = np.array((X1[1] - X1[1]).replace(np.nan, 1))
    RW_val[RW1 == 1] = 0
    Y = X.copy()
    Y = np.array(X.replace(np.nan, 0))
    beta = np.sqrt((Y* Y).sum().sum())
    dict_temp = {}
    parms = [W, RW1, Y/beta, beta, Y, TrueDf, RW_val]
    for i in [0,1,2,3, 4,5, 6]:
        dict_temp[i] = parms[i]
    return (dict_temp)
'''
def Data_Structuring(X1, TrueDf):
    X = (TrueDf + X1[0] + X1[1])/3
    W = np.array((X - X + 1).replace(np.nan, 0))
    R_T = np.array((TrueDf - TrueDf + 1).replace(np.nan, 0))
    RW1 = np.array(((X1[0] - X1[0]).replace(np.nan, 1) + (TrueDf - TrueDf).replace(np.nan, -1))) * R_T
    RW_val = np.array(((X1[1] - X1[1]).replace(np.nan, 1) + (TrueDf - TrueDf).replace(np.nan, -1))) * R_T
    RW_val[RW1 == 1] = 0
    Y = X.copy()
    Y = np.array(X.replace(np.nan, 0))
    beta = np.sqrt((Y* Y).sum().sum())
    dict_temp = {}
    parms = [W, RW1, Y/beta, beta, Y, np.array(TrueDf), RW_val]
    for i in [0,1,2,3, 4,5, 6]:
        dict_temp[i] = parms[i]
    return (dict_temp)
'''
def r_squared(ytrue,ypred):
    if len(ytrue) == len(ypred):
        pred_mean = ypred.mean()
        var_mean = np.power((ypred-pred_mean),2)
        var_line = np.power((ytrue-ypred),2)
        r_sq = 1 - ((var_line.sum())/(var_mean.sum()))
        return r_sq
    else:
        print('Lengths Dont Match')

def define_prior_nuclear_norm(Original_Dataframe, Dataframe_corrupted10, dict1, a_int = 1, b_int = 30, step_int = 2, n_int = 3, err_val_int = 1000, hist = False):
    
    #Step2: Generate Intial
    Original_Dataframes = [Original_Dataframe.copy(deep = True),
                          Original_Dataframe.copy(deep = True).T.unstack(0),
                          Original_Dataframe.copy(deep = True).T.unstack(1)]
    if hist == True:
        Dataframe_corrupted11 = Dataframe_corrupted10.copy(deep = True)
        Dataframe_corrupted11['day_of_week'] = Dataframe_corrupted11.index
        #Debug # Gunjan
        #Dataframe_corrupted11['day_of_week'] = Dataframe_corrupted11['day_of_week'].astype('datetime64[ns]').day_name()
        Dataframe_corrupted10_DOW = Dataframe_corrupted11.groupby('day_of_week')[Dataframe_corrupted11.columns[:-1]].mean().reset_index()
        print(Dataframe_corrupted10_DOW.shape, Dataframe_corrupted10.shape)
        Dataframe_corrupted10_DOW = Dataframe_corrupted11[['day_of_week']].merge(Dataframe_corrupted10_DOW, on = ['day_of_week'], how = 'left' )
        del Dataframe_corrupted10_DOW['day_of_week']
        Dataframe_corrupted10_DOW = Dataframe_corrupted10_DOW.fillna(Dataframe_corrupted10_DOW.mean())
        print(Dataframe_corrupted10_DOW.shape, Dataframe_corrupted10.shape)
    
    #print((Dataframe_corrupted10/Dataframe_corrupted10).copy(deep = True).replace(np.nan, 0).sum().sum() * 100/(Original_Dataframe.shape[0]* Original_Dataframe.shape[1]) )
    Dataframe_corrupted_initialzed = [Dataframe_corrupted10.copy(deep = True).replace(np.nan, 0),
                                     Dataframe_corrupted10.copy(deep = True).replace(np.nan, 0).T.unstack(0),
                                     Dataframe_corrupted10.copy(deep = True).replace(np.nan, 0).T.unstack(1)]
    mat_original = [np.array(Dataframe_corrupted_initialzed[0]),
                   np.array(Dataframe_corrupted_initialzed[1]),
                   np.array(Dataframe_corrupted_initialzed[2])]
    if hist == True:
        Dataframe_corrupted_initialzed = [Dataframe_corrupted10_DOW.copy(deep = True).replace(np.nan, 0),
                                         Dataframe_corrupted10_DOW.copy(deep = True).replace(np.nan, 0).T.unstack(0),
                                         Dataframe_corrupted10_DOW.copy(deep = True).replace(np.nan, 0).T.unstack(1)]
    
    mats = [np.array(Dataframe_corrupted_initialzed[0]),
           np.array(Dataframe_corrupted_initialzed[1]),
           np.array(Dataframe_corrupted_initialzed[2])]

    for r in range (a_int, b_int,step_int):
        for i in range(0, n_int):
            u, s, v = np.linalg.svd(mats[0], full_matrices = 0)
            s[s <= s[r]] =0
            mat_new = u.dot(np.diag(s)).dot(v)
            mats[0] = np.where(mat_original[0] == 0, mat_new, mats[0])
            mats[0][mats[0]<0] = 0
            mats[0]


            mats[1] = np.array(pd.DataFrame(mats[0], columns = Original_Dataframes[0].columns, index = Original_Dataframes[0].index).T.unstack(0))
            u, s, v = np.linalg.svd(mats[1], full_matrices = 0)
            s[s <= s[r]] =0
            mat_new = u.dot(np.diag(s)).dot(v)
            mats[1] = np.where(mat_original[1] == 0, mat_new, mats[1])
            mats[1][mats[1]<0] = 0
            mats[1]


            mats[2] = pd.DataFrame(mats[1], index = Original_Dataframes[1].index, columns = Original_Dataframes[1].columns).T.unstack(1).T.unstack(0)
            u, s, v = np.linalg.svd(mats[2], full_matrices = 0)
            s[s <= s[r]] =0
            mat_new = u.dot(np.diag(s)).dot(v)
            mats[2] = np.where(mat_original[2] == 0, mat_new, mats[2])
            mats[2][mats[2]<0] = 0
            mats[2]

            mats[0] = pd.DataFrame(mats[2], index = Original_Dataframes[2].index, columns = Original_Dataframes[2].columns).T.unstack(1)

            err = dict1[0][1] * (Original_Dataframe - pd.DataFrame(mats[0], columns = Original_Dataframe.columns, index = Original_Dataframe.index))
            
            err_val = dict1[0][6] * (Original_Dataframe - pd.DataFrame(mats[0], columns = Original_Dataframe.columns, index = Original_Dataframe.index))
            #err_train = dict1[0][0] * (Original_Dataframe - pd.DataFrame(mats[0], columns = Original_Dataframe.columns, index = Original_Dataframe.index))
            err = np.round(np.sqrt((err* err).sum().sum()/dict1[0][1].sum()), 2)
            err_val = np.round(np.sqrt((err_val* err_val).sum().sum()/dict1[0][6].sum()), 2)
            #err_train = np.round(np.sqrt((err_train* err_train).sum().sum()/dict1[0][1].sum()), 2)
            #print(err_val, err)
            if err_val < err_val_int:
                err_val_int = err_val
                err_test_int = err
                r_final = r
                mat1 = mats[0].copy()         
    if hist == True:
        print('Initialized using HA: ', colored(['prior minimization    ........:  ' , r_final, err_test_int, err_val_int], 'red'))
    if hist == False:
        print('Initialized from zero: ', colored(['prior minimization    ........:  ' , r_final, err_test_int, err_val_int], 'red'))
    Original_Dataframes, Dataframe_corrupted_initialzed, mat_original = 0,0,0
    print()
    return(mat1, err_val_int)

def randomly_fill_nan_tens(nan_tensor):
    nan_tensor_filled_random = nan_tensor.copy()
    nan_tensor_filled_random[np.isnan(nan_tensor_filled_random)] = abs(np.round(np.random.randn(len(nan_tensor_filled_random[np.isnan(nan_tensor_filled_random)])),2))
    return (nan_tensor_filled_random)

## Spline implementation
def initialize_spline_variables(A1, B1, C1, T3, weight_tens3, reverse_weight_tens3, k = 3,  thresh_spline_window = 11, thresh_spline = 4):

    V = linalg.khatri_rao(A1, B1)
    e_all = pd.DataFrame(weight_tens3*(T3-C1.dot(V.T)))
    k = k
    knots = e_all.shape[0]/k
    knots = math.ceil(knots)
    alpha_all_C = pd.DataFrame(np.random.rand(int(knots) + 3, len(e_all.columns)))
    alpha_all_C
    t_C = e_all[[0]].copy(deep = True)

    for i in range (0, int(round(knots) + 3)):
        if i == 0:
            t_C[i] = 1
        if i == 1:
            t_C[i] = t_C.index+1
        if i == 2:
            t_C[i] = np.power(t_C.index+1 -k, 2) 

        if i ==3:
            t_C[i] = np.power(t_C.index+1- k, 3) 
        if i>=4:
            t_C[i] = np.power(np.where(t_C.index > k * (i-3) -1 , t_C[1] - (k * (i-3)), 0), 3)
    t_C.loc[t_C.index >= knots*k - k,  i] = np.power(t_C[1] + (k * (i-3))-2* (knots*k - k),1)
    list_columns= []
    for a in range (0,int(t_C.columns[-1:][0])):
        list_columns.append(a)
    t_C.loc[t_C.index >= knots*k - k,  list_columns] = t_C.loc[t_C.index == knots*k - k-1, list_columns].values

    t_C.loc[pd.DataFrame(T3).index < k,  2] = 0
    t_C.loc[pd.DataFrame(T3).index < k,  3] = 0

    W1_surrounding = pd.DataFrame(weight_tens3).rolling(thresh_spline_window, center = True).sum().replace(np.nan, 0)
    W1_surrounding[W1_surrounding<= thresh_spline ] = 0
    W1_surrounding[W1_surrounding> thresh_spline ] = 1
    W_spline = np.array(reverse_weight_tens3* W1_surrounding)
    #print(reverse_weight_tens3.sum().sum()/(reverse_weight_tens3.shape[0]* reverse_weight_tens3.shape[1]))
    W_spline
    return (t_C, W_spline)

def spline(A1, B1, C1, T3, T3_dash, t_C, weight_tens3, reverse_weight_tens3, W_spline):
    V = linalg.khatri_rao(A1, B1)
    e_all = pd.DataFrame(weight_tens3*(T3_dash-C1.dot(V.T)))
    #print(weight_tens3)
    e_ls = e_all.copy() 
    t_mod = t_C.copy()
    numerator = e_ls.T.dot(t_mod)
    t_mod.T.dot(t_mod)
    denominator = pinv(t_mod.T.dot(t_mod))
    alpha_all_C = numerator.dot(denominator).T
    finale = C1.dot(linalg.khatri_rao(A1, B1).T) +  np.array(W_spline * (t_mod.dot(alpha_all_C)))
    #print(W_spline.max())
    finale[finale<0] = 0
    err = abs(T3 - finale)
    rmse1 = np.round(np.sqrt(abs(reverse_weight_tens3 * (err * err)).sum()/(reverse_weight_tens3.sum())), 2)
    mape1  = np.round(abs(reverse_weight_tens3 * np.array(pd.DataFrame(abs(err)/T3).replace(np.nan, 0).replace(np.inf, 0))).sum()/(reverse_weight_tens3.sum())* 100,2) 
    temp = (reverse_weight_tens3* ((T3-C1.dot(linalg.khatri_rao(A1, B1).T)-t_C.dot(alpha_all_C))/T3))
    try:
        mape = round(100 * abs(pd.DataFrame(reverse_weight_tens3* ((T3-C1.dot(linalg.khatri_rao(A1, B1).T) -  np.array(W_spline* (t_mod.dot(alpha_all_C))))/T3)) ).replace(np.inf, 0).sum().sum() / (reverse_weight_tens3 .sum().sum() - temp.groupby(np.isinf(temp)).count()[True]), 2)
    except:
        mape = round(100 * abs(pd.DataFrame(reverse_weight_tens3* ((T3- C1.dot(linalg.khatri_rao(A1, B1).T) -  np.array(W_spline* (t_mod.dot(alpha_all_C))))/T3)) ).replace(np.inf, 0).sum().sum() / (reverse_weight_tens3 .sum().sum()), 2)
        pass
    
    return (rmse1, mape1, t_mod, alpha_all_C, finale)

## Some tensor utility functions

def required_tensors(dict1, Original_DataframeA, Dataframe_corrupted10_filledA,  Tens_shape):
    Reverse_Weight_Matrix1A = pd.DataFrame(dict1[0][1] +dict1[0][6] , columns = Original_DataframeA.columns, index = Original_DataframeA.index)
    TrueTensA = folding_3D(np.array(Original_DataframeA), unfol_dim = 0 , other_dim_seq = [1,2], Tens_shape = Tens_shape) #
    TensA = folding_3D(np.array(Dataframe_corrupted10_filledA), unfol_dim = 0 , other_dim_seq = [1,2], Tens_shape = Tens_shape)
    Tens_ReverseWeight1A = folding_3D(np.array(Reverse_Weight_Matrix1A), unfol_dim = 0 , other_dim_seq = [1,2], Tens_shape = Tens_shape)
    randomly_filled_tensA = randomly_fill_nan_tens(TensA)
    reverse_weight_tens3 = unfolding_3D(folding_3D(np.array(pd.DataFrame(dict1[0][1] , columns = Original_DataframeA.columns, index = Original_DataframeA.index)), unfol_dim = 0 , other_dim_seq = [1,2], Tens_shape = Tens_shape), unfol_dim = 2, other_dim_seq = [0,1] )
    return(Reverse_Weight_Matrix1A, TrueTensA, TensA, Tens_ReverseWeight1A, randomly_filled_tensA, reverse_weight_tens3)

def initialize_Tensor_decomposition(r,hyp_prior, hyper_smooth, Tens_shape, TensA, TrueTensA, dict1, Original_DataframeA, Tens_ReverseWeight1A ):
    A = np.random.rand(TensA.shape[0],r)/1000
    B = np.random.rand(TensA.shape[1],r)/1000
    C = np.random.rand(TensA.shape[2],r)/1000
    T1 = unfolding_3D(TensA, unfol_dim = 0, other_dim_seq = [1,2] )
    T2 = unfolding_3D(TensA, unfol_dim = 1, other_dim_seq = [2,0] )
    T3 = unfolding_3D(TensA, unfol_dim = 2, other_dim_seq = [0,1] )
    T3_true = unfolding_3D(TrueTensA, unfol_dim = 2, other_dim_seq = [0,1] )

    Weight_Matrix1 = pd.DataFrame(dict1[0][0] + hyp_prior * dict1[0][1] + hyp_prior * dict1[0][6], columns = Original_DataframeA.columns, index = Original_DataframeA.index)
    #print(Weight_Matrix1)
    Tens_Weight1 = folding_3D(np.array(Weight_Matrix1), unfol_dim = 0 , other_dim_seq = [1,2], Tens_shape = Tens_shape)

    weight_tens1 = unfolding_3D(Tens_Weight1, unfol_dim = 0, other_dim_seq = [1,2] )
    weight_tens2 = unfolding_3D(Tens_Weight1, unfol_dim = 1, other_dim_seq = [2,0] )
    weight_tens3 = unfolding_3D(Tens_Weight1, unfol_dim = 2, other_dim_seq = [0,1] )
    print('min, ',  weight_tens1.min().min(),weight_tens2.min().min()  ,weight_tens3.min().min() ,Weight_Matrix1.min().min() )

    reverse_weight_tens1 = dict1[0][1] * unfolding_3D(Tens_ReverseWeight1A, unfol_dim = 0, other_dim_seq = [1,2] )
    #reverse_weight_tens2 = unfolding_3D(Tens_ReverseWeight1A, unfol_dim = 1, other_dim_seq = [2,0] )
    #reverse_weight_tens3 = unfolding_3D(Tens_ReverseWeight1A, unfol_dim = 2, other_dim_seq = [0,1] )

    W_smooth = -pd.DataFrame(np.identity(C.shape[0])).rolling(2, axis = 1).sum().replace(np.nan, 0)
    W_smooth[0] = -pd.DataFrame(np.identity(C.shape[0]))[0]
    W_smooth = np.array(W_smooth + 2* pd.DataFrame(np.identity(C.shape[0])))
    
    return(A, B , C, T1, T2, T3, T3_true, Weight_Matrix1,weight_tens1, weight_tens2, weight_tens3 , reverse_weight_tens1,W_smooth,  Tens_Weight1)

def stats (Comp_df, dataset = 'val' ):
    if dataset == 'val':
        Merger_df = Comp_df[Comp_df['Weights_val'] ==1]
        Merger_df = Merger_df[Merger_df['True']>=1]
        Merger_df['diff'] = Merger_df['True'] - Merger_df['Estimated']
        rmse_stat = np.sqrt((Merger_df['diff'] * Merger_df['diff']).sum()/Merger_df['diff'].shape[0])
        MAPE_stat = (abs(Merger_df['diff']/Merger_df['True'])*100).sum()/Merger_df['diff'].shape[0]
        r2_stat = r_squared(np.array(Merger_df['True']),np.array(Merger_df['Estimated']))
    if dataset == 'test':
        Merger_df = Comp_df[Comp_df['Weights_test'] ==1]
        Merger_df = Merger_df[Merger_df['True']>=1]
        Merger_df['diff'] = Merger_df['True'] - Merger_df['Estimated']
        rmse_stat = np.sqrt((Merger_df['diff'] * Merger_df['diff']).sum()/Merger_df['diff'].shape[0])
        MAPE_stat = (abs(Merger_df['diff']/Merger_df['True'])*100).sum()/Merger_df['diff'].shape[0]
        r2_stat = r_squared(np.array(Merger_df['True']),np.array(Merger_df['Estimated']))
    return(np.round(rmse_stat,2), np.round(MAPE_stat,2), np.round(r2_stat,3))

def get_test_val_stat(Original_Dataframe, reverse_weight_tens1, Reconstructed_Matrix, dict1):
    True_df = pd.DataFrame(Original_Dataframe.unstack(0))
    True_df.columns = ['True']
    Weights_df = pd.DataFrame(pd.DataFrame(dict1[0][1], columns = Original_Dataframe.columns, index = Original_Dataframe.index).unstack(0))
    Weights_df.columns = ['Weights_test']
    Estimated_df = pd.DataFrame(pd.DataFrame(Reconstructed_Matrix, columns = Original_Dataframe.columns, index = Original_Dataframe.index).unstack(0))
    Estimated_df.columns = ['Estimated']                
    reverse_weight_tens1_validation =pd.DataFrame( pd.DataFrame(dict1[0][6], columns = Original_Dataframe.columns, index = Original_Dataframe.index).unstack(0))
    reverse_weight_tens1_validation.columns = ['Weights_val']
    Comp_df = True_df.merge(Weights_df , left_index = True, right_index = True)
    Comp_df = Comp_df.merge(Estimated_df , left_index = True, right_index = True)
    Comp_df = Comp_df.merge(reverse_weight_tens1_validation , left_index = True, right_index = True)
    rmse_stat_test, MAPE_stat_test, r2_stat_test = stats (Comp_df.copy(), dataset = 'test' )
    rmse_stat_val, MAPE_stat_val, r2_stat_val = stats (Comp_df.copy(), dataset = 'val' )
    return(rmse_stat_test, MAPE_stat_test, rmse_stat_val, MAPE_stat_val, r2_stat_test, r2_stat_val)

def spline_impuatation_CPU(A1, B1, C1, T3,T3_true,TrueTens, weight_tens3_, reverse_weight_tens3, reverse_weight_tens3_val, Original_Dataframe, Dataframe_corrupted10A, rmse_thresh):
    for k in [2,4,6,8,10,12,14,16, 18, 20]:
        for miss_threshold in [0.20,0.40,0.60]:
            t_C, W_spline = initialize_spline_variables(A1, B1, C1, T3,weight_tens3_, reverse_weight_tens3 + reverse_weight_tens3_val, k = k,  miss_threshold = miss_threshold)
            rmse1, mape1, t_mod, alpha_all_C, finale = spline(A1, B1, C1, T3_true, T3, t_C, weight_tens3_, reverse_weight_tens3, W_spline)
            True_df = pd.DataFrame(unfolding_3D(TrueTens, unfol_dim = 2, other_dim_seq = [0,1]), index = Original_Dataframe.T.unstack(0).index, columns = Original_Dataframe.T.unstack(0).columns).unstack(0).reset_index()
            True_df.columns = ['date', 'sections', 'time', 'True']
            Weights_df = pd.DataFrame(reverse_weight_tens3, index = Original_Dataframe.T.unstack(0).index, columns = Original_Dataframe.T.unstack(0).columns).unstack(0).reset_index()
            Weights_df.columns = ['date', 'sections', 'time', 'Weights_test']
            Weights_df_val = pd.DataFrame(reverse_weight_tens3_val, columns =Original_Dataframe.T.unstack(0).columns, index = Original_Dataframe.T.unstack(0).index ).unstack(0).reset_index()
            Weights_df_val.columns = ['date', 'sections', 'time', 'Weights_val']
            Estimated_df = pd.DataFrame(finale, index = Original_Dataframe.T.unstack(0).index, columns = Original_Dataframe.T.unstack(0).columns).unstack(0).reset_index()
            Estimated_df.columns = ['date', 'sections', 'time', 'Estimated']
            Comp_dfA = True_df.merge(Weights_df, on = ['date', 'sections', 'time']).merge(Weights_df_val, on = ['date', 'sections', 'time']).merge(Estimated_df, on = ['date', 'sections', 'time'])
            r_spline_test, m_spline_test, r2_stat_test = stats (Comp_dfA, dataset = 'test' )
            r_spline_val,  m_spline_val, r2_stat_val =  stats (Comp_dfA, dataset = 'val' )
            #print(k, miss_threshold, r_spline_test,m_spline_test, r_spline_val, m_spline_val)
            if r_spline_val < rmse_thresh:
                finale_final = finale.copy()
                r_spline_test_final = r_spline_test.copy()
                m_spline_test_final = m_spline_test.copy()
                r_spline_val_final = r_spline_val.copy()
                m_spline_val_final = m_spline_val.copy()
                r2_stat_test_final = r2_stat_test.copy()
                r2_stat_val_final = r2_stat_val.copy()
                rmse_thresh = r_spline_val
    try:
        print('         ', colored([miss_threshold, k,  'test:', r_spline_test_final, m_spline_test_final, r2_stat_test_final, ' val :', r_spline_val_final, m_spline_val_final, r2_stat_val_final], 'red'))
        finale_final[finale_final<0]=0
        finale = pd.DataFrame(finale_final, index = Original_Dataframe.T.unstack(0).index, columns = Original_Dataframe.T.unstack(0).columns)
        rec_df = finale.T.unstack(1).T.unstack(0).T.unstack(1)
        rec_df = Dataframe_corrupted10A.copy(deep = True).fillna(rec_df)
        Dataframe_corrupted10_filled = Dataframe_corrupted10A.copy(deep = True).fillna(rec_df)
        return(Dataframe_corrupted10_filled, r_spline_test_final, m_spline_test_final, r2_stat_test_final, r_spline_val_final)
    except:
        print('previous was best')
        pass

def Final_stats (Comp_df, t = 'True', e = 'Proposed'):
    Merger_df = Comp_df[Comp_df['Weights_val'] ==1]
    Merger_df = Merger_df[Merger_df[t]>=1]
    Merger_df['diff'] = Merger_df[t] - Merger_df[e]
    Merger_df['add'] = Merger_df[t] + Merger_df[e]
    Merger_df['GEH'] = 2 * np.sqrt((2 * Merger_df['diff'] * Merger_df['diff']) / (Merger_df['add']))
    geh_stat =  Merger_df[Merger_df['GEH'] <= 5].shape[0] * 100 / Merger_df.shape[0]
    rmse_stat = np.sqrt((Merger_df['diff'] * Merger_df['diff']).sum()/Merger_df['diff'].shape[0])
    MAPE_stat = (abs(Merger_df['diff']/Merger_df[t])*100).sum()/Merger_df['diff'].shape[0]
    r2_stat = r_squared(np.array(Merger_df[t]),np.array(Merger_df[e]))
    return(np.round(rmse_stat,2), np.round(MAPE_stat,2), np.round(r2_stat,3), np.round(geh_stat,2))

def spline_impuatation(A1, B1, C1, T3, T3_true, missing_rate, converted_dict, Tens, weight_tens3,weight_tens3_, reverse_weight_tens3, reverse_weight_tens3_val, Original_Dataframe, Dataframe_corrupted10A, rmse_thresh, myDevice):
    if myDevice == 'GPU':
        Original_matrix = unfolding_3D(Tens, unfol_dim = 0, other_dim_seq = [1,2])
        def calculate_weighted_rmse(Original_matrix, Reconstructed_Matrix, weight_matrix):
            assert Original_matrix.shape == Reconstructed_Matrix.shape == weight_matrix.shape, "Arrays must have the same shape"
            masked_original = Original_matrix * weight_matrix
            masked_reconstructed = Reconstructed_Matrix * weight_matrix
            squared_diff = (masked_original - masked_reconstructed) ** 2
            num_nonzero = cp.count_nonzero(weight_matrix)
            rmse = cp.sqrt(squared_diff.sum() / num_nonzero)
            return rmse.item()
        Original_matrix_df = Original_Dataframe.copy(deep = True).replace(np.nan, 0)
        weight_test_df = pd.DataFrame(converted_dict[1].get(), index = Original_Dataframe.index,
                                            columns = Original_Dataframe.columns)
        weight_val_df = pd.DataFrame(converted_dict[6].get(), index = Original_Dataframe.index,
                                            columns = Original_Dataframe.columns)
        for k in [2,3,4,5,7,9]:
            for thresh_spline in [4,6,8,10,12]:
                bb = time.time()
                t_C, W_spline = initialize_spline_variables(A1, B1, C1, T3, weight_tens3,reverse_weight_tens3 + reverse_weight_tens3_val, k = k,  thresh_spline_window = 11, thresh_spline =thresh_spline)
                #print('7a', time.time() - bb)
                rmse1, mape1, t_mod, alpha_all_C, finale = spline(A1, B1, C1, T3_true, T3, t_C, weight_tens3_, reverse_weight_tens3, W_spline)
                #print('7b', time.time() - bb)
                #print(finale.shape, converted_dict[0].shape, Original_matrix.shape)
                #print(unfolding_3D(folding_3D(finale, 2 , [0,1]borte, Tens.shape), 0, [1,2]).shape)
                finale1 = unfolding_3D(folding_3D(finale, 2 , [0,1], Tens.shape), 0, [1,2])
                r_spline_test = calculate_weighted_rmse(cp.asarray(Original_matrix), cp.asarray(finale1), converted_dict[1])
                #print('1')
                r_spline_val = calculate_weighted_rmse(cp.asarray(Original_matrix), cp.asarray(finale1), converted_dict[6])
                #print('7c', time.time() - bb)
                finale1[finale1<0]=0
                finale1 = pd.DataFrame(finale1, index = Original_Dataframe.index, columns = Original_Dataframe.columns)
                diff = (weight_test_df * (Original_matrix_df - finale1) * (Original_matrix_df - finale1)).sum().sum()
                rmsee = np.sqrt(diff/ weight_test_df.sum().sum())
                print(rmsee)
                diff = (weight_val_df * (Original_matrix_df - finale1) * (Original_matrix_df - finale1)).sum().sum()
                rmsee_val = np.sqrt(diff/ weight_val_df.sum().sum())
                r_spline_test = rmsee
                r_spline_val = rmsee_val
                print(k, thresh_spline, r_spline_test, r_spline_val)
                if r_spline_val < rmse_thresh:
                    print('yo')
                    finale_final = finale.copy()
                    r_spline_test_final = r_spline_test
                    r_spline_val_final = r_spline_val
                    rmse_thresh = r_spline_val
        try: 
            print('yes')
            print('         ', missing_rate, k)
            print('yes')
            finale_final[finale_final<0]=0
            print('yes')
            finale = pd.DataFrame(finale_final, index = Original_Dataframe.T.unstack(0).index, columns = Original_Dataframe.T.unstack(0).columns)
            print('yes')
            rec_df = finale.T.unstack(1).T.unstack(0).T.unstack(1)
            print('yes')
            rec_df = Dataframe_corrupted10A.copy(deep = True).fillna(rec_df)
            print('yes')
            Dataframe_corrupted10_filled = Dataframe_corrupted10A.copy(deep = True).fillna(rec_df)
            return(Dataframe_corrupted10_filled, r_spline_test_final,  r_spline_val_final)
        except:
            print('previous was best')
            pass


def NTD(A, B, C, hy1, Original_Dataframe, reverse_weight_tens1, dict1, Tens, Tens_Weight1, W_smooth, Batch_per, Batch_iter, max_iter, hyper_smooth, p=1):
    Tens_Weight1 = Tens_Weight1 * Tens_Weight1
    rmse_stat1 = 1000
    previous_rmse = []
    
    for i in range(max_iter):
        for indexo, j in enumerate(Batch_iter):
            if i <= j:
                Batch_per1 = Batch_per[indexo]
                Batch_per2 = Batch_per[indexo]
                Batch_per3 = Batch_per[indexo]
                Batch_size1 = int(Tens.shape[0] * Batch_per1 / 100)
                Batch_size2 = int(Tens.shape[1] * Batch_per2 / 100)
                Batch_size3 = int(Tens.shape[2] * Batch_per3 / 100)
        
        if (i % 50== 0) & (Batch_per1 == 100) & (i>250) :
            #print(Batch_per1)
            Reconstructed_Matrix = A.dot(linalg.khatri_rao(B, C).T)
            rmse_stat_test, MAPE_stat_test, rmse_stat_val, MAPE_stat_val, r2_stat_test, r2_stat_val = get_test_val_stat(Original_Dataframe, reverse_weight_tens1, Reconstructed_Matrix, dict1)
            print(f'                           {i} {Batch_per1} {rmse_stat_test} | {MAPE_stat_test} | {rmse_stat_val} | {MAPE_stat_val} | {r2_stat_test} | {r2_stat_val}')
            
            if Batch_per1 >= 80:
                if rmse_stat_val < rmse_stat1:
                    rmse_stat1 = rmse_stat_val
                    mape_stat1 = MAPE_stat_val
                    rmse_stat1_test = rmse_stat_test
                    mape_stat1_test = MAPE_stat_test
                    r2_stat_test1 = r2_stat_test
                    r2_stat_val1 = r2_stat_val
                    A1, B1, C1 = A.copy(), B.copy(), C.copy()
                
                previous_rmse.append(rmse_stat_val)
                
                try:
                    if len(previous_rmse) > 4 and rmse_stat_val > max(previous_rmse[-4:-1]):
                        print(f'aborted at iteration {i} since {rmse_stat_val} > {rmse_stat1} & {Batch_per1} > 80')
                        print(colored(['optimum:', i, '|', Batch_per1, '|', rmse_stat1_test, '|', mape_stat1_test, '|', rmse_stat1, '|', mape_stat1, '|', r2_stat_test1, '|', r2_stat_val1], 'blue'))
                        break
                except:
                    pass
        
        if i % 1 == 0:
            sample1 = random.sample(range(0, Tens.shape[0]), Batch_size1)
            sample2 = random.sample(range(0, Tens.shape[1]), Batch_size2)
            sample3 = random.sample(range(0, Tens.shape[2]), Batch_size3)
            
            Tens_sampled = Tens[:, sample2, :][:, :, sample3]
            T1_sampled = unfolding_3D(Tens_sampled, unfol_dim=0, other_dim_seq=[1, 2])
            Tens_Weight1_sampled = Tens_Weight1[:, sample2, :][:, :, sample3]
            weight_tens1_sampled = unfolding_3D(Tens_Weight1_sampled, unfol_dim=0, other_dim_seq=[1, 2])
            Tens_sampled = Tens[sample1, :, :][:, :, sample3]
            T2_sampled = unfolding_3D(Tens_sampled, unfol_dim=1, other_dim_seq=[2, 0])
            Tens_Weight2_sampled = Tens_Weight1[sample1, :, :][:, :, sample3]
            weight_tens2_sampled = unfolding_3D(Tens_Weight2_sampled, unfol_dim=1, other_dim_seq=[2, 0])
            Tens_sampled = Tens[sample1, :, :][:, sample2, :]
            T3_sampled = unfolding_3D(Tens_sampled, unfol_dim=2, other_dim_seq=[0, 1])
            Tens_Weight3_sampled = Tens_Weight1[sample1, :, :][:, sample2, :]
            weight_tens3_sampled = unfolding_3D(Tens_Weight3_sampled, unfol_dim=2, other_dim_seq=[0, 1])
        
        V = linalg.khatri_rao(B[sample2, :], C[sample3, :])
        A = A * np.power(((weight_tens1_sampled * T1_sampled).dot(V) + 0.0000000001) / ((weight_tens1_sampled * (A.dot(V.T))).dot(V) + hy1 * A + 0.0000000001), p)
        
        V = linalg.khatri_rao(C[sample3, :], A[sample1, :])
        B = B * np.power(((weight_tens2_sampled * T2_sampled).dot(V) + 0.0000000001) / ((weight_tens2_sampled * (B.dot(V.T))).dot(V) + hy1 * B + 0.0000000001), p)
        
        V = linalg.khatri_rao(A[sample1, :], B[sample2, :])
        C = C * np.power(((weight_tens3_sampled * T3_sampled).dot(V) + 0.0000000001) / ((weight_tens3_sampled * (C.dot(V.T))).dot(V) + hy1 * C + 0.0000000001), p)
    
    try:
        return A1, B1, C1, [rmse_stat1_test, mape_stat1_test, rmse_stat1, mape_stat1, r2_stat_test, r2_stat_val]
    except:
        rmse_stat1 = rmse_stat_val
        mape_stat1 = MAPE_stat_val
        rmse_stat1_test = rmse_stat_test
        mape_stat1_test = MAPE_stat_test
        r2_stat_test1 = r2_stat_test
        r2_stat_val1 = r2_stat_val
        A1, B1, C1 = A.copy(), B.copy(), C.copy()
        return A1, B1, C1, [rmse_stat1_test, mape_stat1_test, rmse_stat1, mape_stat1, r2_stat_test, r2_stat_val]


## NTD using GPU 

# Option : Here multiple functions are present in a function, this can be written outside of this as this has become too long.
# Option : Many try: and except: are present. If this are just for debugging then we can delete most.

def NTD_cp(myDevice, A, B, C, hy1, Original_Dataframe,reverse_weight_tens1, dict1, converted_dict, Tens, Tens_Weight1, W_smooth,Batch_per, Batch_iter, max_iter, hyper_smooth, p = 1):
    if myDevice == 'GPU':
        rmse_stat1= 1000
        previous_rmse = []
        def khatri_rao_product(a, b):
            array = cp.kron(a, b)
            selected_columns = [i * a.shape[1] + i for i in range(a.shape[1] )]
            result = array[:, selected_columns]
            return result
        try:
            print(Original_Dataframe.shape, A.shape, B.shape, C.shape)
            print(khatri_rao_product(B, C).shape)
        except:
            pass
        Original_matrix_df = Original_Dataframe.copy(deep = True).replace(np.nan, 0)
        weight_test_df = pd.DataFrame(converted_dict[1].get(), index = Original_Dataframe.index,
                                            columns = Original_Dataframe.columns)
        weight_val_df = pd.DataFrame(converted_dict[6].get(), index = Original_Dataframe.index,
                                            columns = Original_Dataframe.columns)
        for i in range(0,max_iter):
            for indexo, j in enumerate(Batch_iter): 
                if i <=j:
                    Batch_per1 = Batch_per[indexo]
                    Batch_per2 = Batch_per[indexo]
                    Batch_per3 = Batch_per[indexo]
                    Batch_size1 = int(Tens.shape[0]*Batch_per1/100)
                    Batch_size2 = int(Tens.shape[1]*Batch_per2/100)
                    Batch_size3 = int(Tens.shape[2]*Batch_per3/100)
            if i%50 == 0:
                try:
                    Reconstructed_Matrix = A.dot(khatri_rao_product(B, C).T)
                except:
                    def khatri_rao_product(a, b):
                        #print('yeah')
                        n = a.shape[0]
                        n2 = b.shape[0]
                        m1 = a.shape[1]
                        m2 = b.shape[1]
                        #print(n, m1, m2)
                        khatri_rao_result = cp.zeros((n * n2, m2), dtype=a.dtype)
                        #print(khatri_rao_result.shape)
                        for i in range(m2):
                            #print(i, cp.kron(a[:, i: i+1], b[:, i: i+1]).shape, a[:, i: i + 1].shape, b[:, i: i+1].shape)
                            khatri_rao_result[:, i] = cp.kron(a[:, i], b[:, i])
                    
                        return khatri_rao_result
                    Reconstructed_Matrix = A.dot(khatri_rao_product(B, C).T)
                    pass
                #Original_matrix = unfolding_3D(Tens, unfol_dim = 0, other_dim_seq = [1,2])
                Reconstructed_Matrix_df = pd.DataFrame(Reconstructed_Matrix.get(), index = Original_Dataframe.index,
                                                    columns = Original_Dataframe.columns)
                
                diff = (weight_test_df * (Original_matrix_df - Reconstructed_Matrix_df) * (Original_matrix_df - Reconstructed_Matrix_df)).sum().sum()
                rmsee = np.sqrt(diff/ weight_test_df.sum().sum())
                print(rmsee)
                rmse_stat_test = rmsee
                diff = (weight_val_df * (Original_matrix_df - Reconstructed_Matrix_df) * (Original_matrix_df - Reconstructed_Matrix_df)).sum().sum()
                rmsee_val = np.sqrt(diff/ weight_val_df.sum().sum())
                rmse_stat_val = rmsee_val
                print('                           ',i,Batch_per1, rmse_stat_test, rmse_stat_val )
                if Batch_per1 == 100:   
                    if rmse_stat_val < rmse_stat1:
                        rmse_stat1 = rmse_stat_val
                        rmse_stat1_test = rmse_stat_test
                        A1 = A.copy()
                        B1 = B.copy()
                        C1 = C.copy()
                    previous_rmse.append(rmse_stat_val)
                    try:
                        if ((len(previous_rmse) > 3) & (rmse_stat_val > max(previous_rmse[-5:-1]))):
                            if Batch_per1 > 80:
                                print('aborted at iteration ', i, 'since ',  rmse_stat_val , '>', rmse_stat1 , ' &' , Batch_per1 , '> 80')
                                #print(colored(['optimum : ', i,'|', Batch_per1, '|', rmse_stat1_test,'|',rmse_stat1_val ], 'blue'))
                                break
                    except:
                        pass
            aa = time.time()
            #Update B
            sample1 = random.sample(range(0, Tens.shape[0]), Batch_size1)
            sample2 = random.sample(range(0, Tens.shape[1]), Batch_size2)
            sample3 = random.sample(range(0, Tens.shape[2]), Batch_size3)
            Tens_sampled = Tens[:, sample2, :][:, :, sample3]
            #Update A
            T1_sampled = unfolding_3D(Tens_sampled, unfol_dim = 0, other_dim_seq = [1,2] )
            Tens_Weight1_sampled = Tens_Weight1[:, sample2, :][:, :, sample3]
            weight_tens1_sampled = unfolding_3D(Tens_Weight1_sampled, unfol_dim = 0, other_dim_seq = [1,2] )
            try:
                V = khatri_rao_product(B[sample2, :],C[sample3, :])
            except:
                def khatri_rao_product(a, b):
                    #print('yeah')
                    n = a.shape[0]
                    n2 = b.shape[0]
                    m1 = a.shape[1]
                    m2 = b.shape[1]
                    #print(n, m1, m2)
                    khatri_rao_result = cp.zeros((n * n2, m2), dtype=a.dtype)
                    #print(khatri_rao_result.shape)
                    for i in range(m2):
                        #print(i, cp.kron(a[:, i: i+1], b[:, i: i+1]).shape, a[:, i: i + 1].shape, b[:, i: i+1].shape)
                        khatri_rao_result[:, i] = cp.kron(a[:, i], b[:, i])
                
                    return khatri_rao_result
                V = khatri_rao_product(B[sample2, :],C[sample3, :])
                pass
            A = A * np.power(((weight_tens1_sampled * T1_sampled).dot(V) 
                    +0.0000000001) / ((weight_tens1_sampled * (A.dot(V.T))).dot(V) 
                                    +  hy1 * A 
                                    +0.0000000001),p)   
            #Update B
            Tens_sampled = Tens[sample1, : , :][:, :, sample3]
            T2_sampled = unfolding_3D(Tens_sampled, unfol_dim = 1, other_dim_seq = [2,0] )
            Tens_Weight2_sampled = Tens_Weight1[sample1,: , :][:, :, sample3]
            weight_tens2_sampled = unfolding_3D(Tens_Weight2_sampled, unfol_dim = 1, other_dim_seq = [2,0] )
            try:
                V = khatri_rao_product(C[sample3, :],A[sample1, :])
            except:
                def khatri_rao_product(a, b):
                    #print('yeah')
                    n = a.shape[0]
                    n2 = b.shape[0]
                    m1 = a.shape[1]
                    m2 = b.shape[1]
                    #print(n, m1, m2)
                    khatri_rao_result = cp.zeros((n * n2, m2), dtype=a.dtype)
                    #print(khatri_rao_result.shape)
                    for i in range(m2):
                        #print(i, cp.kron(a[:, i: i+1], b[:, i: i+1]).shape, a[:, i: i + 1].shape, b[:, i: i+1].shape)
                        khatri_rao_result[:, i] = cp.kron(a[:, i], b[:, i])
                
                    return khatri_rao_result
                V = khatri_rao_product(C[sample3, :],A[sample1, :])
                pass
            B= B * np.power(((weight_tens2_sampled * T2_sampled).dot(V)
                    +0.0000000001) / ((weight_tens2_sampled * (B.dot(V.T))).dot(V) 
                                    + hy1 * B
                                    + 0.0000000001), p)
            #Update C
            Tens_sampled = Tens[sample1, : , :][:, sample2, :]
            T3_sampled = unfolding_3D(Tens_sampled, unfol_dim = 2, other_dim_seq = [0,1] )
            Tens_Weight3_sampled = Tens_Weight1[sample1, : , :][:, sample2, :]
            weight_tens3_sampled = unfolding_3D(Tens_Weight3_sampled, unfol_dim = 2, other_dim_seq = [0,1] )
            try:
                V = khatri_rao_product(A[sample1, :], B[sample2, :])
            except:
                def khatri_rao_product(a, b):
                    #print('yeah')
                    n = a.shape[0]
                    n2 = b.shape[0]
                    m1 = a.shape[1]
                    m2 = b.shape[1]
                    #print(n, m1, m2)
                    khatri_rao_result = cp.zeros((n * n2, m2), dtype=a.dtype)
                    #print(khatri_rao_result.shape)
                    for i in range(m2):
                        #print(i, cp.kron(a[:, i: i+1], b[:, i: i+1]).shape, a[:, i: i + 1].shape, b[:, i: i+1].shape)
                        khatri_rao_result[:, i] = cp.kron(a[:, i], b[:, i])
                
                    return khatri_rao_result
                V = khatri_rao_product(A[sample1, :], B[sample2, :])
                pass
            C = C * np.power(((weight_tens3_sampled * T3_sampled).dot(V)
                    + 0.0000000001 ) / ((weight_tens3_sampled * (C.dot(V.T))).dot(V) 
                                        + hy1 * C
                                        + 0.0000000001  ),p)
            #print(time.time()-aa)
        return (A1, B1, C1 , [rmse_stat1_test,rmse_stat1])


# Apply

# Our main function here :  

def impute(Original_Dataframe,
           Tens_shape,
           device = 'CPU',
           zero_as_missing = False, 
           miss_type = 'MM2', 
           missing_rate = [0.001,0.001,0.001], 
           missing_rate_val = [0.2, 0.2, 0.2] ,
           block_window = 6,
           ranks = [10, 15, 20], 
           max_iter = 4000,
           hy1_list = [0.1, 0.01, 0.001],
           hyp_prior_list = [0.6,0.7,0.8],
           hyper_smooth = 0.00001,
           Batch_per = [100, 70, 50],
           Batch_iter = [2000 , 1500, 1000],
           p = 1.0
           ): # Main function
    """
    Description : Using SPRINT we do the imputation. So, when a dataset having absenceny (or NaN), is processed by this algorithm we can get a complete dataset. 

    Inputs : 

        Original_Dataframe : Address of the dataframe with NaN values
        Tens_shape : Signifying (Number of days, number of links, time intervals per day)
        device : 'CPU' or 'GPU'. The GPU version uses 'cupy' library, so do complete the required installations step.
        zero_as_missing: True (if 0 as well as NaN in Original_Dataframe are to be considered as a missing datapoint), False (if 0 is to be considered as an observed value).
        miss_type: ('RM', 'NM', 'MM', 'BM', 'MM2') Types of missing values to be introduced in the dataset (to classify the validation dataset or define testing scenarios). Four types of missing values to be introduced. Use 'RM' for Random missing, 'NM' for fiber-like non-random missing, 'BM' for Block missing, 'MM' for Mixed-Missing, and 'MM2' for Mixed-missing type-2. Default miss type is set as 'MM2'.
        missing_rate: A scalar value (range 0-1) representing the fraction of cells to be classified as missing for 'RM', 'NM', and 'BM' scenarios. A list with two fractions, e.g., [0.2, 0.3], representing the fraction of ['RM', 'NM'] for 'MM' scenario, and a list of three fractions [0.1, 0.3, 0.2] for ['RM', 'NM', 'BM'] for MM2 scenario. Used only to introduce dummy missing data to create different testing scenarios. Default value is [0.001, 0.001, 0.001].
        missing_rate_val: Fraction of dummy missing cells to be introduced to the dataset to classify the validation set. Input is a scalar value (range 0-1) for 'RM', 'NM', and 'BM' scenarios. A list with two fractions, e.g., [0.2, 0.3], representing the fraction of ['RM', 'NM'] for 'MM' scenario, and a list of three fractions [0.1, 0.3, 0.2] for ['RM', 'NM', 'BM'] for MM2 scenario. Default values for 'RM', 'NM', and 'BM' are 0.5, 'MM' is [0.3, 0.3], and 'MM2' is [0.2, 0.2, 0.2].
        block_window: The size of the square missing block for BM scenario. The default value is 6.
        Ranks: A list constituting iterative stepwise increase in ranks of factorization of SINTD [10, 15, 20].
        max_iter: Maximum number of iterations in SINTD. The default value is 4000.
        hy1_list: List of hyperparameters for L2 norm. Default value is [0.1, 0.01, 0.001]. Each SINTD is performed for every hyperparameter in hy1_list, and the best hyperparameter is selected based on the minimum RMSE of reconstruction calculated for the validation dataset defined by missing_rate_val.
        hyp_prior_list: A list representing the hyperparameters to assign weightage to the prior values in SINTD. The number of elements in the list should be equal to the total number of iterations in the framework, equal to the length of the Ranks.
        hyper_smooth: Hyperparameter for the smoothing regularization term. Default value = 0.00001.
        Batch_per: A list defining the batch sizes (0 to 100%) in the Stepwise batch increment strategy. Important for the efficiency of the SINTD algorithm. The list works from the last element towards the first element, e.g., in Batch_per = [100, 70, 50], the first 50% of the batch size will be used, followed by 70% and then 100%.
        Batch_iter: Number of within SINTD iterations where batch size in Batch_per is to be changed. For example, if Batch_per = [100, 70, 50] and Batch_iter = [4000, 1500, 1000], for the first 1000 iterations, a batch size of 50 will be used, followed by 70% batch size from 1000 to 1500 iterations and 100% from 1500 to 4000.
        p: Parameter to control the learning rate of SINTD. Default value = 1.

    Output : An imputed pandas DataFrame of the same shape as Original_Dataframe
    """

    #new_directory = r'./'
    #Original_Dataframe = pd.read_csv(new_directory + os.sep + 'Logan_data_Smaller.csv', header = [0], index_col = [0,1]).unstack(1)
    Original_Dataframe = pd.read_csv(Original_Dataframe, header = [0], index_col = [0,1]).unstack(1)
    #Tens_shape = (333, 24, 96) # Testing : Previously (333, 476, 96)

    Writecsv = True
    Original_Dataframe = Original_Dataframe.applymap(replace_decimal_with_nan)

    dense_tensor, sparse_tensor, sparse_tensor_val, Dataframe_corrupted10, Dataframe_corrupted10_val, dim1, dim2, dim3 = add_missing(Original_Dataframe, Tens_shape, miss_type, zero_as_missing, missing_rate, missing_rate_val, block_window)

    # Starting Imputation

    if device == 'CPU':

        # Starting Imputation
        print('Imputation Started')
        print('    1. step1 : Data Structuring (started)')

        if Writecsv:
            Dataframe_corrupted10.to_csv('Dataframe_corrupted.csv')
            Dataframe_corrupted10_val.to_csv('Dataframe_corrupted_validation.csv')

        dict1 = {}
        Datasets = [Dataframe_corrupted10, Dataframe_corrupted10_val]
        dict1[0] = Data_Structuring(Datasets, np.array(Original_Dataframe))

        print('        --check wieghts', Dataframe_corrupted10.shape[1] * Dataframe_corrupted10.shape[0] - dict1[0][0].sum() - dict1[0][1].sum() - dict1[0][6].sum())
        print('        --check Missing', np.round(dict1[0][1].sum() * 100 / (Dataframe_corrupted10.shape[1] * Dataframe_corrupted10.shape[0]), 0))
        print('        --check Validation', np.round(dict1[0][6].sum() * 100 / (Dataframe_corrupted10.shape[1] * Dataframe_corrupted10.shape[0]), 0))
        print('        --step1 : done')


        # Step 2: Prior Tensor Mining
        print('    2. step2 : Prior Tensor Mining (started)')
        Dataframe_corrupted10A = (Dataframe_corrupted10 + Dataframe_corrupted10_val) / 2
        mat1, err_mat1 = define_prior_nuclear_norm(Original_Dataframe, Dataframe_corrupted10A, dict1, a_int=1, b_int=min(30, dim1, dim2, dim3), step_int=1, n_int=3, err_val_int=1000, hist=True)
        mat1_, err_mat1_ = define_prior_nuclear_norm(Original_Dataframe, Dataframe_corrupted10A, dict1, a_int=1, b_int=min(30, dim1, dim2, dim3), step_int=1, n_int=3, err_val_int=1000, hist=False)

        if err_mat1_ < err_mat1:
            print('selected prior from ititialization = 0' )
            mat1 = mat1_.copy()
        else: 
            print('selected prior from ititialization = hist' )
        err_mat = min(err_mat1_, err_mat1)
        # Step 2: Define first prior
        kmm_final = pd.DataFrame(mat1, columns=Original_Dataframe.columns, index=Original_Dataframe.index)
        Dataframe_corrupted10_filled = Dataframe_corrupted10A.fillna(kmm_final)
        Dataframe_corrupted10_filled_last = Dataframe_corrupted10_filled.copy()
        if Writecsv:
            Dataframe_corrupted10_filled.to_csv('Dataframe_filled_NNM.csv')

        rmse_initial = 1000
        Step_wise_results = []

        for iteration in range(len(ranks)):
            r = ranks[iteration]
            hyp_prior = hyp_prior_list[iteration]
            print('    Step 3 (iteration' + str(iteration) + '): NTD Started ............')

            # A. Define the Required tensors
            Reverse_Weight_Matrix1, TrueTens, Tens, Tens_ReverseWeight1, randomly_filled_tens, reverse_weight_tens3 = required_tensors(dict1, Original_Dataframe, Dataframe_corrupted10_filled, Tens_shape)

            # B. Initialize tensor decomposition matrices
            A, B, C, T1, T2, T3, T3_true, Weight_Matrix1, weight_tens1, weight_tens2, weight_tens3, reverse_weight_tens1, W_smooth, Tens_Weight1 = initialize_Tensor_decomposition(r, hyp_prior, hyper_smooth, Tens_shape, Tens, TrueTens, dict1, Original_Dataframe, Tens_ReverseWeight1)

            threshold_NTD_rmse = 1000
            for hy1 in hy1_list:
                A1, B1, C1, NTD_stats = NTD(A, B, C, hy1, Original_Dataframe, reverse_weight_tens1, dict1, Tens, Tens_Weight1, W_smooth, Batch_per, Batch_iter, max_iter, hyper_smooth, p=p)
                if NTD_stats[2] < threshold_NTD_rmse:
                    A2 = A1.copy()
                    B2 = B1.copy()
                    C2 = C1.copy()
                    threshold_NTD_rmse = NTD_stats[2].copy()
                print('    Step 3 (iteration' + str(iteration) + '): NTD ended ............ for sparsity', hy1, 'with rmse', NTD_stats[0], NTD_stats[2])

            A1 = A2.copy()
            B1 = B2.copy()
            C1 = C2.copy()

            if Writecsv:
                V = linalg.khatri_rao(B1, C1)
                Rec_df = pd.DataFrame(A1.dot(V.T), columns=Original_Dataframe.columns, index=Original_Dataframe.index)
                Rec_df.to_csv('Dataframe_filled_iteration_without_spline' + str(iteration) + '.csv')

            Combined_Mat = Original_Dataframe.unstack().reset_index().merge(Dataframe_corrupted10.unstack().reset_index(), on=['level_0', 'time', 'date'], how='inner')
            Combined_Mat = Combined_Mat.merge(Rec_df.unstack().reset_index(), on=['level_0', 'time', 'date'], how='inner')
            Combined_Mat.columns = ['section_id', 'time', 'date', 'True', 'corrupt', 'Proposed']
            Combined_Mat['Weights_val'] = 1
            Combined_Mat = Combined_Mat[Combined_Mat['corrupt'].isna()]
            rmse1, mape1, r21, geh1 = Final_stats(Combined_Mat, t='True', e='Proposed')
            Step_wise_results.append(['iter-' + str(iteration + 1), 'NTD', rmse1, mape1, r21, geh1])

            print('    Step 3 (iteration' + str(iteration) + '): Spline Started ............')

            Weight_Matrix1_ = pd.DataFrame(dict1[0][0], columns=Original_Dataframe.columns, index=Original_Dataframe.index)
            Tens_Weight1_ = folding_3D(np.array(Weight_Matrix1_), unfol_dim=0, other_dim_seq=[1, 2], Tens_shape=Tens_shape)
            weight_tens3_ = unfolding_3D(Tens_Weight1_, unfol_dim=2, other_dim_seq=[0, 1])
            T3 = unfolding_3D(Tens, unfol_dim=2, other_dim_seq=[0, 1])
            Reverse_Weight_Matrix3A_val = pd.DataFrame(dict1[0][6], columns=Original_Dataframe.columns, index=Original_Dataframe.index)
            Tens_ReverseWeight3A_val = folding_3D(np.array(Reverse_Weight_Matrix3A_val), unfol_dim=0, other_dim_seq=[1, 2], Tens_shape=Tens_shape)
            reverse_weight_tens3_val = unfolding_3D(Tens_ReverseWeight3A_val, unfol_dim=2, other_dim_seq=[0, 1])
            r2_stat_val_final = NTD_stats[2].copy()
            try:
                if miss_type != 'NM':
                    Dataframe_corrupted10_filled, r_spline_test_final, m_spline_test_final, r2_stat_test_final, r2_stat_val_final = spline_impuatation_CPU(A1, B1, C1, T3, T3_true, TrueTens, weight_tens3_, reverse_weight_tens3, reverse_weight_tens3_val, Original_Dataframe, Dataframe_corrupted10A, rmse_thresh=threshold_NTD_rmse)
                if miss_type == 'NM':
                    rec_dfo = pd.DataFrame(C1.dot(linalg.khatri_rao(A1, B1).T), index=Original_Dataframe.T.unstack(0).index, columns=Original_Dataframe.T.unstack(0).columns).T.unstack(1).T.unstack(0).T.unstack(1)
                    Dataframe_corrupted10_filled = Dataframe_corrupted10A.copy(deep=True).fillna(rec_dfo)
                print('Option1')
            except:
                print('Option 2.........weird........................')
                rec_dfo = pd.DataFrame(C1.dot(linalg.khatri_rao(A1, B1).T), index=Original_Dataframe.T.unstack(0).index, columns=Original_Dataframe.T.unstack(0).columns).T.unstack(1).T.unstack(0).T.unstack(1)
                Dataframe_corrupted10_filled = Dataframe_corrupted10A.copy(deep=True).fillna(rec_dfo)
                pass
            
            if r2_stat_val_final > err_mat: 
                print('Option 3: this iterration was a waste', (r2_stat_val_final > err_mat))
                Dataframe_corrupted10_filled = Dataframe_corrupted10_filled_last.copy(deep = True)
                r2_stat_val_final = err_mat.copy()

            Dataframe_corrupted10_filled_last = Dataframe_corrupted10_filled.copy(deep = True)
            err_mat = r2_stat_val_final.copy()
            print('    Step 3 (iteration' + str(iteration) + '): Spline Ended ............')

            if Writecsv:
                Dataframe_corrupted10_filled.to_csv('Dataframe_filled_iteration' + str(iteration) + '.csv')

            Combined_Mat = Original_Dataframe.unstack().reset_index().merge(Dataframe_corrupted10.unstack().reset_index(), on=['level_0', 'time', 'date'], how='inner')
            Combined_Mat = Combined_Mat.merge(Dataframe_corrupted10_filled.unstack().reset_index(), on=['level_0', 'time', 'date'], how='inner')
            Combined_Mat.columns = ['section_id', 'time', 'date', 'True', 'corrupt', 'Proposed']
            Combined_Mat['Weights_val'] = 1
            Combined_Mat = Combined_Mat[Combined_Mat['corrupt'].isna()]
            rmse1, mape1, r21, geh1 = Final_stats(Combined_Mat, t='True', e='Proposed')
            Step_wise_results.append(['iter-' + str(iteration + 1), 'LSE', rmse1, mape1, r21, geh1])

            Matrix_Proposed = Dataframe_corrupted10_filled.copy()


    elif device == 'GPU':
        myDevice = 'GPU'

        # Starting Imputation
        print('Imputation Started')
        #...............................#Step 1 : Data Structuring
        print('    1. step1 : Data Structuring (started) ')

        if Writecsv == True:
            Dataframe_corrupted10.to_csv('Dataframe_corrupted.csv')
            Dataframe_corrupted10_val.to_csv('Dataframe_corrupted_validation.csv')
        dict1 = {}
        Datasets = [Dataframe_corrupted10, Dataframe_corrupted10_val]
        dict1[0] = Data_Structuring(Datasets,Original_Dataframe)

        converted_dict = convert_numpy_to_cupy(dict1[0], myDevice)
        converted_dict[0]
        print('        --check wieghts', Dataframe_corrupted10.shape[1] * Dataframe_corrupted10.shape[0] - dict1[0][0].sum()-dict1[0][1].sum()-dict1[0][6].sum())
        print('        --check Missing', np.round(dict1[0][1].sum()*100/(Dataframe_corrupted10.shape[1] * Dataframe_corrupted10.shape[0]), 0))
        print('        --check Validation', np.round(dict1[0][6].sum()*100/(Dataframe_corrupted10.shape[1] * Dataframe_corrupted10.shape[0]), 0))
        print('        --step1 : done ')


        print('    2. step2 : Prior Tensor Mining (started) ')
        Dataframe_corrupted10A = (Dataframe_corrupted10 + Dataframe_corrupted10_val)/2
        mat1, err_mat1 = define_prior_nuclear_norm(Original_Dataframe, Dataframe_corrupted10A, dict1, a_int = 1, b_int = min(30,dim1, dim2, dim3), step_int = 1, n_int = 3, err_val_int = 1000)
        #................................#Step2 : Define first prior
        kmm_final = pd.DataFrame(mat1, columns = Original_Dataframe.columns, index = Original_Dataframe.index)
        Dataframe_corrupted10_filled = Dataframe_corrupted10A.fillna(kmm_final)

        if Writecsv == True:
            Dataframe_corrupted10_filled.to_csv('Dataframe_filled_NNM.csv')
        print('    Step 2: Completed ')
        #................................#Step3 : Iterative imputation

        np.random.seed(5)

        # The below code is for using GPU
        print('    Step 3: NTD Started ............')
        rmse_initial = 1000
        for iteration in range(0,len(ranks)):
            r = ranks[iteration]
            hyp_prior = hyp_prior_list[iteration]
            print('    Step 3 (iteration' +  str(iteration) +') : NTD Started ............')
            #A. Define the Required tensors
            Reverse_Weight_Matrix1, TrueTens, Tens, Tens_ReverseWeight1, randomly_filled_tens, reverse_weight_tens3 = required_tensors(dict1, Original_Dataframe, Dataframe_corrupted10_filled,  Tens_shape)
            #B. Initialize tensor decomposition matrices 
            A, B , C, T1, T2, T3, T3_true, Weight_Matrix1,weight_tens1, weight_tens2, weight_tens3 , reverse_weight_tens1,W_smooth,Tens_Weight1 = initialize_Tensor_decomposition(r,hyp_prior, hyper_smooth, Tens_shape, Tens, TrueTens, dict1, Original_Dataframe, Tens_ReverseWeight1 )
            threshold_NTD_rmse = 1000
            for hy1 in hy1_list:
                A1, B1, C1 , NTD_stats = NTD_cp(myDevice, cp.asarray(A), cp.asarray(B), cp.asarray(C), hy1, 
                                                Original_Dataframe, cp.asarray(reverse_weight_tens1), 
                                                dict1, converted_dict,cp.asarray(Tens), cp.asarray(Tens_Weight1),
                                                cp.asarray(W_smooth), Batch_per, Batch_iter, 
                                                max_iter, hyper_smooth, p = 1.4)
                if NTD_stats[1] < threshold_NTD_rmse:
                    A2 = A1.copy().get()
                    B2 = B1.copy().get()
                    C2 = C1.copy().get()
                    threshold_NTD_rmse = NTD_stats[1]
                print('    Step 3 (iteration' +  str(iteration) +') : NTD ended ............ for sparsity' , hy1 , 'with rmse', NTD_stats[0] , NTD_stats[1] )
            A1 = A2.copy()
            B1 = B2.copy()
            C1 = C2.copy()

            if Writecsv == True:
                V = linalg.khatri_rao(B1, C1)
                Rec_df = pd.DataFrame(A1.dot(V.T), columns = Original_Dataframe.columns, index = Original_Dataframe.index )
                Rec_df.to_csv('Dataframe_filled_iteration_without_spline' + str(iteration) +'.csv')
            print('    Step 3 (iteration' +  str(iteration) +') : Spline Started ............')
            aa = time.time()
            Weight_Matrix1_ = pd.DataFrame(dict1[0][0] , columns = Original_Dataframe.columns, index = Original_Dataframe.index)
            #print('1', time.time() -aa)
            Tens_Weight1_ = folding_3D(np.array(Weight_Matrix1_), unfol_dim = 0 , other_dim_seq = [1,2], Tens_shape = Tens_shape)
            #print('2', time.time() -aa)
            weight_tens3_ = unfolding_3D(Tens_Weight1_, unfol_dim = 2, other_dim_seq = [0,1] )
            #print('3', time.time() -aa)
            T3 = unfolding_3D(Tens, unfol_dim = 2, other_dim_seq = [0,1] )
            #print('4', time.time() -aa)
            Reverse_Weight_Matrix3A_val = pd.DataFrame(dict1[0][6], columns = Original_Dataframe.columns, index = Original_Dataframe.index)
            #print('5', time.time() -aa)
            Tens_ReverseWeight3A_val = folding_3D(np.array(Reverse_Weight_Matrix3A_val), unfol_dim = 0 , other_dim_seq = [1,2], Tens_shape = Tens_shape)
            #print('6', time.time() -aa)
            reverse_weight_tens3_val = unfolding_3D(Tens_ReverseWeight3A_val, unfol_dim = 2, other_dim_seq = [0,1] )
            #Dataframe_corrupted10_filled, r_spline_test_final, r_spline_val_final = spline_impuatation(A1, B1, C1, T3,T3_true, weight_tens3_, reverse_weight_tens3,reverse_weight_tens3_val, Original_Dataframe, Dataframe_corrupted10A, rmse_thresh = threshold_NTD_rmse)
            #print('7', time.time() -aa)
            try:
                Dataframe_corrupted10_filled, r_spline_test_final, r_spline_val_final = spline_impuatation(A1, B1, C1, T3,T3_true, missing_rate,converted_dict, Tens, weight_tens3,weight_tens3_, reverse_weight_tens3,reverse_weight_tens3_val, Original_Dataframe, Dataframe_corrupted10A, rmse_thresh = threshold_NTD_rmse, myDevice = myDevice)
                print('done1')
            #print('7', time.time() -aa)
            except:
                rec_dfo = pd.DataFrame(C1.dot(linalg.khatri_rao(A1, B1).T), index = Original_Dataframe.T.unstack(0).index, columns = Original_Dataframe.T.unstack(0).columns).T.unstack(1).T.unstack(0).T.unstack(1)
                #print('8', time.time() -aa)
                Dataframe_corrupted10_filled =  Dataframe_corrupted10A.copy(deep = True).fillna(rec_dfo)
                print('done2')
                pass
            print('    Step 3 (iteration' +  str(iteration) +') : Spline Ended ............')
            if Writecsv == True:
                Dataframe_corrupted10_filled.to_csv('Dataframe_filled_iteration' + str(iteration) +'.csv')
            fake_nans = -((Original_Dataframe - Original_Dataframe).replace(np.nan, 1) + (Dataframe_corrupted10 - Dataframe_corrupted10).replace(np.nan, -1))
            print(np.sqrt(np.power(fake_nans * (Dataframe_corrupted10_filled - Original_Dataframe), 2).replace(np.nan, 0).sum().sum() / fake_nans.sum().sum()))

        # 0utput


        Matrix_Proposed = Dataframe_corrupted10_filled.copy()
        
        
    return Matrix_Proposed



"""Final_Output = impute('.\Logan_data_Smaller.csv',(333, 24, 96), device = 'GPU')
print('Shape : ')
print(Final_Output.shape)
print('\n')
print('NaN : ')
print(((np.isnan(Final_Output)).sum()).sum())
print('Output matrix : ')
print(Final_Output)"""

