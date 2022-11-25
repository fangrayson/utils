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
    cov : np.array (covariance matrix; size (N,N)) [Required]
    lower_bounds: np.array or list (if None, set to a default; size N)
    upper_bounds: np.array or list (if None, set to a default; size N)
    size: int (if None, set to default of 1)
    min_sample_rate: int (minumum number of candidate samples to produce in each iteration of the while loop)

    Outputs
    -------
    sample: np.array of size (N, size) (sampled from truncated MVN distribution)
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





def get_step_interval_distribution(interval_boundaries, interval_ratios, size = None):
    """
    Samples from a set of intervals with uniform distributions.
    Pick an interval specified by the interval_boundaries list with probabilities specified by the (standardised) interval_ratios list,
    and pick a point within that interval with uniform distribution.
    The PDF should look like a (not necessarily monotonic) step function.


    Inputs
    ------
    interval_boundaries : np.array or list (must be strictly monotonic, and correspond to finite interval sizes; say size N)
    interval_ratios : np.array or list (size N-1)

    Outputs
    -------
    sample: np.array of size (size) (sampled from the probability distribution function)
    """
    # Check assertions:
    if not all( x < y for x, y in zip(interval_boundaries[:-1], interval_boundaries[1:])):
        raise Exception("interval_boundaries must be strictly increasing")
    if not (interval_boundaries[0] > -np.inf):
        raise Exception("intervals must be finite")
    if not (interval_boundaries[-1] < np.inf):
        raise Exception("intervals must be finite")
    if not (len(interval_boundaries) - len(interval_ratios) == 1):
        raise Exception("len(interval_boundaries) - 1 != len(interval_ratios)")
    # Convert ratios to probabilities
    interval_probabilities = np.array(interval_ratios) / sum(interval_ratios)
    # Calculate interval sizes
    interval_boundaries = np.array(interval_boundaries)
    interval_sizes = interval_boundaries[1:] - interval_boundaries[:-1]
    # -----------------
    # Randomly choose the interval, with probabilities corresponding to interval_probabilities
    random_interval_indices = np.random.choice([i for i in range(len(interval_probabilities))], size=size, p=interval_probabilities)
    # Select WITHIN interval with uniform probability
    uniform_random_variables = np.random.uniform(low=0.0, high=1.0, size=size)
    # Producing the random variable
    sample = np.multiply(uniform_random_variables, interval_sizes[random_interval_indices]) + interval_boundaries[random_interval_indices]
    
    return sample