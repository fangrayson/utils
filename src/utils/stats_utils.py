"""
Module containing sampling and other statistics functions
"""

import numpy as np

def get_trunc_multivariate_normal(
    mean, 
    cov, 
    lower_bounds = None, 
    upper_bounds = None,
    size = None,
    min_sample_rate = 100
    ):
    """
    Generates a sample from a truncated multivariate normal distribution,
    by sampling a candidate from MVN(mean, cov) and resampling if the candidate is outside of the lower and upper bounds.
    ---

    Inputs
    ------
    mean : np.array or list (mean array; say size N) [Required]
    cov : np.array (covariance matrix; size NxN) [Required]
    lower_bounds: np.array or list (if None, set to a default; size N)
    upper_bounds: np.array or list (if None, set to a default; size N)
    size: int (if None, set to default of 1)
    min_sample_rate: int (minumum number of candidate samples to produce in each iteration of the while loop)

    Outputs
    -------
    sample: np.array of size N (sample from truncated MVN distribution)
    """
    # Setting defaults
    if lower_bounds is None: lower_bounds = [-np.inf for x in range(len(mean))];
    if upper_bounds is None: upper_bounds = [ np.inf for x in range(len(mean))];
    if size is None: size = 1;
    # Initialising the output sample
    sample = np.array([])
    # --------------------
    while len(sample) < size:
        num_to_sample = max(min_sample_rate , int(size - len(sample))) # sample at least the min_sample_rate each time
        # Produce candidate sample
        candidate_sample = np.random.multivariate_normal(
            mean = mean,
            cov = cov,
            size = num_to_sample
            )
        # Check that the candidate_sample is within the upper and lower bounds
        above_lower_bounds_bool_array = np.min( candidate_sample >= lower_bounds , axis = 1).reshape(1, -1)
        below_upper_bounds_bool_array = np.min( candidate_sample <= upper_bounds , axis = 1).reshape(1, -1)
        within_both_bounds_bool_array = np.min( np.concatenate( [above_lower_bounds_bool_array, below_upper_bounds_bool_array], axis = 0), axis = 0)
        # Filtering out 'bad' candidate samples and adding to the output
        sample = np.concatenate([sample.reshape(-1, len(mean)), candidate_sample[within_both_bounds_bool_array]])
    
    return np.random.permutation(sample[:size])