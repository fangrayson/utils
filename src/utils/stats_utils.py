"""
Module containing sampling and other statistics functions
"""

import numpy as np

def trunc_multivariate_normal(
    mean, 
    cov, 
    lower_bounds = None, 
    upper_bounds = None,
    size = None,
    min_sample_rate = 100
    ):
    """
    Generates samples from a truncated multivariate normal distribution,
    by generating candidate samples from an MVN(mean, cov) distribution,
    then discarding and resampling candidates that are outside of the lower and upper bounds.

    Inputs
    ------
    :mean:              list   List of means for each variate.
    :cov:               list   Covariance matrix. Must be symmetric positive definite.
    :lower_bounds:      list   List of lower bounds for each variate. If None, no lower bound applied.
    :upper_bounds:      list   List of upper bounds for each variate. If None, no upper bound applied.
    :size:              int    Number of samples to produce. If None, a single sample produced.
    :min_sample_rate:   int    Minumum number of candidate samples to produce in each iteration of the while loop.

    Outputs
    -------
    :sample:   np.array   Samples from a truncated multivariate normal distribution. Float is generated if size is None.
    """
    # Setting defaults
    if lower_bounds is None: lower_bounds = [-np.inf for x in range(len(mean))];
    if upper_bounds is None: upper_bounds = [ np.inf for x in range(len(mean))];
    if size is None:
        sample_size = 1
    else:
        sample_size = size
    # Initialising the output sample
    sample = np.array([])
    # --------------------
    while len(sample) < sample_size:
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
    
    if size is None:
        return sample[:sample_size].reshape(-1,)
    else:
        return np.random.permutation(sample[:sample_size])





def step_distribution(steps, p, size = None):
    """
    Generates samples from a continuous step distribution: this is a collection of intervals each uniformly distributed,
    so that the probability mass function is a step function.

    Inputs
    ------
    :steps:   list   Strictly monotonic list corresponding to where step boundaries occur.
    :p:       list   List corresponding to probabilities of each step. We require that len(p) = len(steps) - 1. If sum(p) != 1, p is treated as ratios of occurrence instead.
    :size:    int    Number of samples to produce. If None, produce 1 sample.

    Outputs
    -------
    :sample:   np.array   Samples from a step distribution. Float is generated if size is None.
    """
    # Check assertions:
    if not all( x < y for x, y in zip(steps[:-1], steps[1:])):
        raise Exception("steps must be strictly increasing")
    if not (steps[0] > -np.inf):
        raise Exception("intervals must be finite")
    if not (steps[-1] < np.inf):
        raise Exception("intervals must be finite")
    if not (len(steps) - len(p) == 1):
        raise Exception("len(steps) - 1 != len(p)")
    # Convert ratios to probabilities
    interval_probabilities = np.array(p) / sum(p)
    # Calculate interval sizes
    steps = np.array(steps) # Convert to np.array
    interval_sizes = steps[1:] - steps[:-1]
    # -----------------
    # Randomly choose the interval, with probabilities corresponding to interval_probabilities
    random_interval_indices = np.random.choice([i for i in range(len(interval_probabilities))], size=size, p=interval_probabilities)
    # Select WITHIN interval with uniform probability
    uniform_random_variables = np.random.uniform(low=0.0, high=1.0, size=size)
    # Producing the random variable
    sample = np.multiply(uniform_random_variables, interval_sizes[random_interval_indices]) + steps[random_interval_indices]
    
    return sample