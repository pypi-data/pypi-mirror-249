# backtracks utility functions. stand on the shoulders of giants, its fun!

import numpy as np
from scipy.stats import norm
from scipy.special import gammainc, gammaincc, gammainccinv, gammaincinv
from astropy.time import Time

def pol2car(sep, pa, seperr, paerr, corr=np.nan):
    ra, dec = seppa2radec(sep, pa)
    raerr, decerr, corr2 = transform_errors(sep, pa, seperr, paerr, corr, seppa2radec)
    return ra, dec, decerr, raerr, corr2


def radec2seppa(ra, dec, mod180=False):
    """
    This function is reproduced here from the orbitize! pacakge, written by S. Blunt et al and distributed under the BSD 3-Clause License
    Convenience function for converting from
    right ascension/declination to separation/
    position angle.
    Args:
        ra (np.array of float): array of RA values, in mas
        dec (np.array of float): array of Dec values, in mas
        mod180 (Bool): if True, output PA values will be given
            in range [180, 540) (useful for plotting short
            arcs with PAs that cross 360 during observations)
            (default: False)
    Returns:
        tuple of float: (separation [mas], position angle [deg])
    """
    sep = np.sqrt((ra**2) + (dec**2))
    pa = np.degrees(np.arctan2(ra, dec)) % 360.

    if mod180:
        pa[pa < 180] += 360

    return sep, pa


def seppa2radec(sep, pa):
    """
    This function is reproduced here from the orbitize! pacakge, written by S. Blunt et al and distributed under the BSD 3-Clause License
    Convenience function to convert sep/pa to ra/dec
    Args:
        sep (np.array of float): array of separation in mas
        pa (np.array of float): array of position angles in degrees
    Returns:
        tuple: (ra [mas], dec [mas])
    """
    ra = sep * np.sin(np.radians(pa))
    dec = sep * np.cos(np.radians(pa))

    return ra, dec


def transform_errors(x1, x2, x1_err, x2_err, x12_corr, transform_func, nsamps=100000):
    """
    This function is reproduced here from the orbitize! pacakge, written by S. Blunt et al and distributed under the BSD 3-Clause License
    Transform errors and covariances from one basis to another using a Monte Carlo
    apporach

   Args:
        x1 (float): planet location in first coordinate (e.g., RA, sep) before
            transformation
        x2 (float): planet location in the second coordinate (e.g., Dec, PA)
            before transformation)
        x1_err (float): error in x1
        x2_err (float): error in x2
        x12_corr (float): correlation between x1 and x2
        transform_func (function): function that transforms between (x1, x2)
            and (x1p, x2p) (the transformed coordinates). The function signature
            should look like: `x1p, x2p = transform_func(x1, x2)`
        nsamps (int): number of samples to draw more the Monte Carlo approach.
            More is slower but more accurate.
    Returns:
        tuple (x1p_err, x2p_err, x12p_corr): the errors and correlations for
            x1p,x2p (the transformed coordinates)
    """

    if np.isnan(x12_corr):
        x12_corr = 0.

    # construct covariance matrix from the terms provided
    cov = np.array([[x1_err**2, x1_err*x2_err*x12_corr], [x1_err*x2_err*x12_corr, x2_err**2]])

    samps = np.random.multivariate_normal([x1, x2], cov, size=nsamps)

    x1p, x2p = transform_func(samps[:,0], samps[:, 1])

    x1p_err = np.std(x1p)
    x2p_err = np.std(x2p)
    x12_corr = np.corrcoef([x1p, x2p])[0,1]

    return x1p_err, x2p_err, x12_corr


def transform_uniform(x,a,b):
    return a + (b-a)*x


def transform_normal(x, mu, sigma):
    return norm.ppf(x, loc=mu, scale=sigma)


def transform_gengamm(x, L=1.35e3, alpha=1, beta=2):
    return L*(gammaincinv((beta+1)/alpha,x)**(1/alpha))

def utc2tt(jd_utc):
    return Time(jd_utc,scale="utc",format="jd").tt.jd

class HostStarPriors(): # stripped version from pints (MultivariateGaussianLogPrior from https://github.com/pints-team/pints/blob/main/pints/_log_priors.py), BSD3-clause
    
    def __init__(self, mean, cov): # setting up distribution, this is done only once so we dont have to bother with a fast Cholesky inversion. Host star parameter distribution doesnt change.
        self._mean = mean
        self._cov = cov
        self._n_parameters = mean.shape[0]
        
        self._sigma12_sigma22_inv_l = []
        self._sigma_bar_l = []
        self._mu1 = []
        self._mu2 = []
        
        for j in range(1, self._n_parameters):
            sigma = self._cov[0:(j + 1), 0:(j + 1)]
            dims = sigma.shape
            sigma11 = sigma[dims[0] - 1, dims[1] - 1]
            sigma22 = sigma[0:(dims[0] - 1), 0:(dims[0] - 1)]
            sigma12 = sigma[dims[0] - 1, 0:(dims[0] - 1)]
            sigma21 = sigma[0:(dims[0] - 1), dims[0] - 1]
            mean = self._mean[0:dims[0]]
            mu2 = mean[0:(dims[0] - 1)]
            mu1 = mean[dims[0] - 1]
            sigma12_sigma22_inv = np.matmul(sigma12,
                                            np.linalg.inv(sigma22))
            sigma_bar = np.sqrt(sigma11 - np.matmul(sigma12_sigma22_inv,
                                                    sigma21))
            self._sigma12_sigma22_inv_l.append(sigma12_sigma22_inv)
            self._sigma_bar_l.append(sigma_bar)
            self._mu1.append(mu1)
            self._mu2.append(mu2)
   
    def transform_normal_multivariate(self, ps): # pulling from distribution with random number between 0 and 1
        
        n_samples = ps.shape[0]
        n_params = ps.shape[1]
        
        icdfs = np.zeros((n_samples, n_params))
        for j in range(n_samples):
            for i in range(self._n_parameters):
                if i == 0: # the first axis just takes the default mean and sigma and draws with a ppf
                    mu = self._mean[0]
                    sigma = np.sqrt(self._cov[0, 0])
                else: # the next axis needs to bias the mean and sigma of the ppf based on the previously drawn numbers
                    sigma = self._sigma_bar_l[i - 1]
                    mu = self._mu1[i - 1] + np.matmul(
                        self._sigma12_sigma22_inv_l[i - 1],
                        (np.array(icdfs[j, 0:i]) - self._mu2[i - 1]))
                icdfs[j, i] = norm.ppf(ps[j, i], mu, sigma) 
        return np.squeeze(np.array_split(icdfs,n_params,axis=1))
