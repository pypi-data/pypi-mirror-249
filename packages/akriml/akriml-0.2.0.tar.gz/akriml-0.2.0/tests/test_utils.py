"""
test_utils.py
Pytests for akriml.utils
"""

from random import randint

import numpy as np
import pytest

from akriml.utils import deco_repeat as repeat
from akriml.utils import get_randomstate, rep_error_mean

MAX_ARR_DIM = 20


def random_arr(**kwargs):
    n_rows = kwargs.get('n_rows', randint(1, MAX_ARR_DIM))
    n_cols = kwargs.get('n_cols', randint(1, MAX_ARR_DIM))
    random_state = kwargs.get('random_state', randint(0, 42))
    np.random.seed(random_state)
    return np.random.rand(n_rows, n_cols)


@pytest.mark.parametrize('random_state', [5, 11, 21, 42])
def test_get_randomstate(random_state):
    # ========== Given
    # ========== When
    r = get_randomstate(random_state)
    output1 = r.rand(5, 4)

    r = get_randomstate(random_state)
    output2 = r.rand(5, 4)

    # =========== Then
    if random_state is not None:
        np.testing.assert_array_equal(output1, output2)
    return


@repeat()
def test_rep_err():
    """
    Ensure the representation error is adequately accurate
    Need to pay more attention to how the expectation relates
        to the mean over vector norm that is used in rep_error_mean
    """
    # Error for the same feature matrix
    features = random_arr(n_rows=500, n_cols=32)
    error = rep_error_mean(features, features)
    assert error <= 1.e-12

    # Error when different magnitudes of white noise is introduced
    noise_arr = 10 ** np.arange(-3, -1.1, 0.5)
    feat_norm = np.linalg.norm(features, ord='fro')
    for noise in noise_arr:
        noisy_features = features + feat_norm * noise * (
                -0.5 + np.random.rand(*features.shape))
        error = rep_error_mean(noisy_features, features)
        # Ensure error is within a couple orders of magnitude of noise
        assert (noise / 100.) <= error <= (100. * noise)
    return
