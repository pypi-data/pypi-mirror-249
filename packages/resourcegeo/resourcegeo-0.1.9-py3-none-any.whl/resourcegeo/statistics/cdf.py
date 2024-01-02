import numpy as np

#Function obtained from pygeostat www.ccgalberta.com
def cdf(var, weights=None, lower=None, upper=None):
    """
    Calculates an experimental CDF using the standard method of the midpoint of a
    histogram bin. It uses all points as in GSLIB. 
    
    This function requires that var and weights are of same length and already
    cleaned (no null values), to avoid unexpected behavior.

    Notes:
    'lower' and 'upper' limits for the CDF may be supplied independently.

    Parameters:
        var (np.array): 1D array of values
        weights (np.array): weights for values in var
        lower (float): Lower limit
        upper (float): Upper Limit

    Returns:
        midpoints(np.ndarray): bin midpoints
        cdf(np.ndarray): cdf values for each midpoint value
    """
    # Ensure weights sum to 1
    if weights is None:
        weights = np.ones(len(var)) / len(var)
    else:
        weights = weights / np.sum(weights)

    # Conversion to numpy arrays
    if not isinstance(weights, np.ndarray):
        weights = np.array(weights)
    if not isinstance(var, np.ndarray):
        var = np.array(var)
    else:
        # Transpose if var is column array 
        if var.shape[0] > 1:
            var = var.transpose()
            
    # GSLIB-style all-values experimental CDF
    order = var.argsort()
    midpoints = var[order]
    cdf = np.cumsum(weights[order])
    #subtract half the first cdf. Upper limit is never 1. Length cdf = Length midpoints
    cdf = cdf - cdf[0] / 2.0

    # Add lower and upper values if desired
    if lower is not None:
        #check lower < than min(midpoint)
        if lower >= midpoints.min(): 
            raise ValueError('Lower limit must be < minimum calculated midpoint')
        cdf = np.append([0.0], cdf)
        midpoints = np.append([lower], midpoints)
    if upper is not None:
        if upper <= midpoints.max(): 
            raise ValueError('Upper limit must be > maximum calculated midpoint')
        cdf = np.append(cdf, [1.0])
        midpoints = np.append(midpoints, [upper])

    return(midpoints, cdf)