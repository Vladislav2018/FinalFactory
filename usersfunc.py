import scipy as sp

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    from scipy.stats import truncnorm
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)