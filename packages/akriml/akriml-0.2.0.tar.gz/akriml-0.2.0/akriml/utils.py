"""
utils.py
Simple utility functions
"""

import functools

import numpy as np


def get_randomstate(random_state=42):
    """
    Convert int or RandomState to np.random.RandomState instances
    """
    if isinstance(random_state, np.random.RandomState):
        return random_state

    if random_state is None:
        return np.random.RandomState()

    return np.random.RandomState(int(random_state))


def deco_repeat(n_times=5):
    """
    Parametrized decorator to repeat functions, especially in tests.
    """

    def orig_repeat(some_func):
        """
        Repeats execution 'n_times' times
        """

        @functools.wraps(some_func)
        def wrapper_repeat(*args, **kwargs):
            for _ in range(n_times):
                some_func(*args, **kwargs)

        return wrapper_repeat

    return orig_repeat


def rep_error_pointwise(X_orig, X_reconst):
    """
    Pointwise representation error for low-rank projections

    Parameters
    ----------
    X_orig: 2d float array of shape (N, D0)
        Original features

    X_reconst: 2d float array of shape (N, D0)
        Reconstruction of low-rank projections.
        Obtain this as reconstruct_from_basis(projections, basis)

    Returns
    -------
    pointwise_error: 1d float array of shape (N,)
        Relative error in representation due to low-rank projection
    """
    if X_orig.shape != X_reconst.shape:
        raise ValueError("Inputs should have same shape")

    if X_orig.ndim == 4:
        n_samples = len(X_orig)
        X_orig = X_orig.reshape(n_samples, -1)
        X_reconst = X_reconst.reshape(n_samples, -1)
    elif X_orig.ndim != 2:
        raise ValueError

    abs_error = np.linalg.norm(X_orig - X_reconst, axis=1)
    denominator = np.linalg.norm(X_orig, axis=1)
    # Add a tiny tolerance in case of degenerate data
    pointwise_error = abs_error / (denominator + 1.e-16)
    return pointwise_error


def rep_error_mean(X_orig, X_reconst):
    """
    Average representation error for low-rank projections

    Parameters
    ----------
    X_orig: 2d float array of shape (N, D0)
        Original features

    X_reconst: 2d float array of shape (N, D0)
        Reconstruction of low-rank projections.
        Obtain this as reconstruct_from_basis(projections, basis)

    Returns
    -------
    mean_error: float
        Mean relative error in representation due to low-rank projection
    """
    return np.mean(rep_error_pointwise(X_orig, X_reconst))
