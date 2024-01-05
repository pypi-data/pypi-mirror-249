# SPRINT

SPRINT is a missing traffic data imputation algorithm based on the integration of a novel Stochastic informed non-negative tensor decomposition algorithm and uniform natural cubic spline regression, developed by Shubham Sharma, Prof Richi Nayak, and Prof Ashish Bhaskar, QUT. The manuscript is under review in the journal Transportation Research Part-C. The Packaging of the algorithm is done by Gunjan Shinde, QUT.

# Installation

You can install the package using below command 


```bash
pip install SPRINT_imputations

```

# Usage 

## First import the package 

```{python}
from SPRINT_imputations import impute 
```
## Call the function 'SPRINT'

```{python}
impute(arg1, arg2)
```
## Agruments for impute() with discription:




- Mandatory
    - Original_Dataframe : Address of the dataframe dataframe with NaN values.
    - Tens_shape : Signifying (Number of days, number of links, time intervals per day)

- Optional
    - **device**: Options are 'CPU' or 'GPU'. The GPU version uses 'cupy' library, so do complete the required installation steps. Default is 'CPU'.
    - **zero_as_missing**: True (if 0 as well as NaN in Original_Dataframe are to be considered as a missing datapoint), False (if 0 is to be considered as an observed value).
    - **miss_type**: ('RM', 'NM', 'MM', 'BM', 'MM2') Types of missing values to be introduced in the dataset (to classify the validation dataset or define testing scenarios). Four types of missing values to be introduced. Use 'RM' for Random missing, 'NM' for fiber-like non-random missing, 'BM' for Block missing, 'MM' for Mixed-Missing, and 'MM2' for Mixed-missing type-2. Default miss type is set as 'MM2'.
    - **missing_rate**: A scalar value (range 0-1) representing the fraction of cells to be classified as missing for 'RM', 'NM', and 'BM' scenarios. A list with two fractions, e.g., [0.2, 0.3], representing the fraction of ['RM', 'NM'] for 'MM' scenario, and a list of three fractions [0.1, 0.3, 0.2] for ['RM', 'NM', 'BM'] for MM2 scenario. Used only to introduce dummy missing data to create different testing scenarios. Default value is [0.001, 0.001, 0.001].
    - **missing_rate_val**: Fraction of dummy missing cells to be introduced to the dataset to classify the validation set. Input is a scalar value (range 0-1) for 'RM', 'NM', and 'BM' scenarios. A list with two fractions, e.g., [0.2, 0.3], representing the fraction of ['RM', 'NM'] for 'MM' scenario, and a list of three fractions [0.1, 0.3, 0.2] for ['RM', 'NM', 'BM'] for MM2 scenario. Default values for 'RM', 'NM', and 'BM' are 0.5, 'MM' is [0.3, 0.3], and 'MM2' is [0.2, 0.2, 0.2].
    - **block_window**: The size of the square missing block for BM scenario. The default value is 6.
    - **Ranks**: A list constituting iterative stepwise increase in ranks of factorization of SINTD [10, 15, 20].
    - **max_iter**: Maximum number of iterations in SINTD. The default value is 4000.
    - **hy1_list**: List of hyperparameters for L2 norm. Default value is [0.1, 0.01, 0.001]. Each SINTD is performed for every hyperparameter in hy1_list, and the best hyperparameter is selected based on the minimum RMSE of reconstruction calculated for the validation dataset defined by missing_rate_val.
    - **hyp_prior_list**: A list representing the hyperparameters to assign weightage to the prior values in SINTD. The number of elements in the list should be equal to the total number of iterations in the framework, equal to the length of the Ranks.
    - **hyper_smooth**: Hyperparameter for the smoothing regularization term. Default value = 0.00001.
    - **Batch_per**: A list defining the batch sizes (0 to 100%) in the Stepwise batch increment strategy. Important for the efficiency of the SINTD algorithm. The list works from the last element towards the first element, e.g., in Batch_per = [100, 70, 50], the first 50% of the batch size will be used, followed by 70% and then 100%.
    - **Batch_iter**: Number of within SINTD iterations where batch size in Batch_per is to be changed. For example, if Batch_per = [100, 70, 50] and Batch_iter = [4000, 1500, 1000], for the first 1000 iterations, a batch size of 50 will be used, followed by 70% batch size from 1000 to 1500 iterations and 100% from 1500 to 4000.
    - **p**: Parameter to control the learning rate of SINTD. Default value = 1.
 
## Output
An imputed pandas DataFrame of the same shape as Original_Dataframe.

## :bulb:TIP: Regarding CUPY library 

- Do note that the CUPY library is not mentioned in the 'requirements.txt' and hence is needed to be installed sperately whose detials steps are mentioned here.

- The CUPY library is suppose to be install as per the GPU's driver version more info can be found [here](https://docs.cupy.dev/en/stable/install.html)
    
- If  there is any CUDA PATH issue, one can explictly set the PATH by the following command.
```python
    
    import os 
    os.environ['CUDA_PATH'] = "C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v11.7"
```
### :heavy_exclamation_mark: Warning
> Don't forgot to change the CUDA version in the above code as per your system.

# Contact

Shubham Sharma | Higher Degree Research Scholar (Ph.D.)\
School of Civil and Environmental Engineering\
Faculty of Engineering | Queensland University of Technology\
Mail ID : s55.sharma@hdr.qut.edu.au
