import os
from random import randint
from random import random as randfloat

import numpy as np
import pytest

from akriml.sketch.fastsketch import FastSketch
from akriml.sketch.sketch_utils import dense_svd, _is_orthonormal_like
from akriml.utils import deco_repeat as repeat
from akriml.utils import rep_error_mean
from tests.test_sketch_utils import random_tall_arr

# =============================================================================
#                   Tests using flat feature representations.
# =============================================================================

# Test representation errors on subsamples of a 10k sample dataset;
#       the sample dataset contains flattened pixel brightness value from MNIST-digits.
# But first, locate feature matrix file...
# Paths should be like so..
# Tests are in repo_root/tests
# While feature matrix is in repo_root/data
curr_path = os.path.dirname(os.path.abspath(__file__))  # tests dir
repo_root = os.path.dirname(curr_path)
data_path = os.path.join(repo_root, 'data')
X0_flat_feat = np.load(os.path.join(data_path, 'mnist_digits_flattened.npy'))[:5000] / 255.
# Expected upper bounds on errors for different sketch sizes:
exp_err_flat_feat = [(32, .22), (64, .18), (128, .15)]
min_rows = 100
max_rows = 400
min_cols = 16
max_cols = 48


def _representation_error_flat_feat(sketcher, feature_matrix):
    projections = sketcher.fit_transform(feature_matrix)
    reconstruction = sketcher.inverse_transform(projections)
    return rep_error_mean(reconstruction, feature_matrix)


def get_random_parameters_flat_feat():
    """
        Define parameters for simple fastsketch
    """
    n_rows = randint(min_rows, max_rows)  # Number of rows in feature matrix
    n_cols = randint(min_cols, max_cols)  # Number of original features
    n_components = randint(1, n_cols)  # Sketch dimensionality
    frac = max(randfloat(), 0.05)  # Subsample size for svd
    feature_matrix = random_tall_arr(n_rows=n_rows, n_cols=n_cols)
    return feature_matrix, n_components, frac


@repeat(3)
def test_shapes_flat_feat():
    """
    Verify output shapes for 2d feature array input
    """
    # ===============Given,
    features, n_comp, frac = get_random_parameters_flat_feat()
    N, D0 = features.shape
    features_test = random_tall_arr(n_cols=D0,
                                    n_rows=randint(D0, max_rows))
    N_t = len(features_test)
    # ===============When,
    sketcher = FastSketch(n_components=n_comp, frac=frac, overwrite=False)
    projections = sketcher.fit_transform(features)
    D = sketcher.n_components_
    reconstruction = sketcher.inverse_transform(projections).reshape(-1, D0)
    proj_test = sketcher.transform(features_test)
    reconstruction_test = sketcher.inverse_transform(proj_test).reshape(-1, D0)

    # ===============Then...
    assert sketcher.components_.shape == (D, D0)
    assert sketcher.singular_values_.shape == (D,)
    assert sketcher.sketch.shape == (D, D0)
    assert projections.shape == (N, D)
    assert proj_test.shape == (N_t, D)
    assert reconstruction.shape == features.shape
    assert reconstruction_test.shape == features_test.shape
    return


@repeat(3)
def test_single_dir_flat_feat():
    """
    When all datapoints lie along a single direction,
        then sketch should have just a single dominant direction.
    And the reconstruction should be near-perfect.
    """
    # ===============Given,
    # Define random matrix
    features, n_comp, frac = get_random_parameters_flat_feat()
    # Choose first direction as the only direction
    features[1:] = features[:1]
    # Scale each row, because why not?
    features = np.random.rand(len(features), 1) * features

    # ===============When,
    sketcher = FastSketch(n_components=n_comp, frac=frac)
    projections = sketcher.fit_transform(features)
    basis = sketcher.components_
    reconstruction = sketcher.inverse_transform(projections).reshape(features.shape)
    error = rep_error_mean(reconstruction, features)

    # ===============Then...
    if len(basis) > 1:
        # In case the tolerances don't discard other directions
        assert (np.linalg.norm(projections[:, 1:], ord='fro') /
                np.linalg.norm(projections, ord='fro')) <= 1.e-5
    assert 0 <= error <= 1.e-5
    return


@repeat(3)
def test_multi_dir_exact_flat_feat():
    """
    When all datapoints lie along just a few directions,
        then sketch should have just these dominant directions.
    And the reconstruction should be near-perfect.
    Note that sketch dimensionality should be sufficiently large for this.
    """
    # ===============Given,
    n_cols = randint(min_cols, max_cols)
    n_dom_dir = randint(1, min(n_cols, 6))
    # Create set of dominant directions
    non_orth_dir = np.random.rand(n_dom_dir, n_cols)
    _, basis = dense_svd(non_orth_dir, k=n_dom_dir)
    # Create feature matrix as linear combinations of basis
    n_rows = randint(min_rows, max_rows)
    basis_combi = np.random.rand(n_rows, n_dom_dir)
    features = basis_combi @ basis

    # ===============When,
    n_comp = randint(n_dom_dir, n_cols)  # Sketch dimensionality
    # Since n_comp >= n_dom_dir, reconstruction should be near-perfect
    frac = max(randfloat(), 0.2)  # At least 20% rows for svd
    sketcher = FastSketch(n_components=n_comp, frac=frac)
    projections = sketcher.fit_transform(features)
    basis = sketcher.components_
    reconstruction = sketcher.inverse_transform(projections).reshape(features.shape)
    error = rep_error_mean(reconstruction, features)

    # ===============Then...
    # pdb.set_trace()
    if len(basis) > n_dom_dir:
        assert (sketcher.singular_values_[n_dom_dir:] <= 1.e-5).all()
        # In case the tolerances don't discard other directions
        assert (np.linalg.norm(projections[:, n_dom_dir:], ord='fro') /
                np.linalg.norm(projections, ord='fro')) <= 1.e-5
    assert 0 <= error <= 1.e-5
    return


@pytest.mark.parametrize('overwrite', [True, False])
@repeat(3)
def test_update_or_overwrite_sketch_flat_feat(overwrite):
    """
    When overwrite param is set to False subsequent calls of .fit or
    .fit_transform incrementally trains the model.
    If it's True, subsequent calls should just overwrite previous components.
    """
    # ===============Given,
    n_cols = randint(min_cols, max_cols)
    # Define data in 2 different directions for testing
    n_dom_dir = 2  # Select number of dominant directions
    # Create set of dominant directions
    non_orth_dir = np.random.rand(n_dom_dir, n_cols)
    _, basis = dense_svd(non_orth_dir, k=n_dom_dir)
    # Create feature matrix as linear combinations of basis
    # features in first direction
    n_rows = randint(min_rows, max_rows)
    basis_combi = np.random.rand(n_rows, 1)
    features_set1 = basis_combi @ basis[0].reshape((1, -1))
    # features in second direction
    n_rows = randint(min_rows, max_rows)
    basis_combi = np.random.rand(n_rows, 1)
    features_set2 = basis_combi @ basis[1].reshape((1, -1))

    n_comp = randint(1, n_cols)  # Sketch dimensionality
    # If n_comp >= n_dom_dir, reconstruction should be near-perfect
    # "overwrite" param is supplied from pytest.mark.parametrize
    sketcher = FastSketch(n_components=n_comp, overwrite=overwrite)

    # ===============When,
    # .fit_transform is called on features_set1 for the first time.
    projections_set1 = sketcher.fit_transform(features_set1)
    basis_set1 = sketcher.components_
    reconstruction_set1 = sketcher.inverse_transform(projections_set1)
    error_set1 = rep_error_mean(reconstruction_set1, features_set1)
    # ===============Then
    # there should be one dominant direction.
    if len(basis_set1) > 1:
        # In case the tolerances don't discard other directions
        assert (np.linalg.norm(projections_set1[:, 1:], ord='fro') /
                np.linalg.norm(projections_set1, ord='fro')) <= 1.e-5
    assert 0 <= error_set1 <= 1.e-5

    # ===============When,
    # .fit_transform or .fit is called for the second time, now on
    # features_set2 using the same previous sketcher instance.
    sketcher = sketcher.fit(features_set2)
    projections_set2 = sketcher.transform(features_set2)
    reconstruction_set2 = sketcher.inverse_transform(projections_set2)
    basis_set2 = sketcher.components_
    error_set2 = rep_error_mean(reconstruction_set2, features_set2)

    # transforming features_set1 using the new sketcher instance
    proj_set1_new = sketcher.transform(features_set1)
    recon_set1_new = sketcher.inverse_transform(proj_set1_new)
    error_set1_new = rep_error_mean(recon_set1_new, features_set1)

    error_combined = rep_error_mean(np.concatenate((recon_set1_new,
                                                    reconstruction_set2),
                                                   axis=0),
                                    np.concatenate((features_set1,
                                                    features_set2), axis=0))
    # ===============Then
    if overwrite:
        # if overwrite=True, there should be one dominant direction.
        assert 0 <= error_set2 <= 1.e-5
        if len(basis_set2) > 1:
            # In case the tolerances don't discard other directions
            assert (np.linalg.norm(projections_set2[:, 1:], ord='fro') /
                    np.linalg.norm(projections_set2, ord='fro')) <= 1.e-5
        if len(basis_set2) == 1:
            # since overwrite is True, the second call to .fit or
            # .fit_transform should overwrite the previous information of
            # features_set1
            assert error_set1_new > 1.e-5
    else:
        # overwrite = False
        # there will be more than one dominant directions, since trained
        # incrementally on data that's in two different directions.
        if len(basis_set2) > 2:
            # In case the tolerances don't discard other directions
            assert (np.linalg.norm(projections_set2[:, 2:], ord='fro') /
                    np.linalg.norm(projections_set2, ord='fro')) <= 1.e-5
            assert (np.linalg.norm(proj_set1_new[:, 2:], ord='fro') /
                    np.linalg.norm(proj_set1_new, ord='fro')) <= 1.e-5
            assert 0 <= error_combined <= 1.e-5


@pytest.mark.parametrize('n_blocks', [1, 3, 5])
def test_loads_of_instances_flat_feat(n_blocks):
    """
    Verify that sketching works for a lot of subsets of feature array
    """
    rstate = np.random.RandomState(0)
    n_trials = 10
    # ====================== Given,
    # The larger feature matrix X0_flat_feat,
    for trial in range(n_trials):
        # Pick a smaller subset of features,
        n_features = rstate.randint(1, 16)
        # Because sketch dimensionality can't be larger than n_features,
        D_sketch = min(n_features, rstate.randint(1, max(2, n_features)))
        X1 = X0_flat_feat[:, rstate.randint(X0_flat_feat.shape[1],
                                            size=n_features)]
        assert X1.shape == (len(X0_flat_feat), n_features)

        #   as well as a smaller subset of points,
        n_samples = rstate.randint(1, 50)
        X = X1[rstate.choice(len(X1), size=n_samples)]

        # ========================== When,
        # We sketch,
        sketcher = FastSketch(n_components=D_sketch, n_blocks=n_blocks)
        sketcher.fit(X)
        basis = sketcher.components_

        # ======================== Then,
        assert _is_orthonormal_like(basis), "The output must have an orthonormal basis."

    return


@pytest.mark.parametrize('seed', range(5))
def test_sketch_reproducibility_tiny_flat_feat(seed):
    """
    Ensure reproducible outcomes for FastSketch on tiny datasets
    """
    rstate = np.random.RandomState(seed)
    n_trials = 3
    # ====================== Given,
    # A specific subset 'X' of the larger feature matrix X0_flat_feat,
    n_features = rstate.randint(1, 16)
    X1 = X0_flat_feat[:, rstate.randint(X0_flat_feat.shape[1], size=n_features)]
    n_samples = rstate.randint(1, 50)
    X = X1[rstate.choice(len(X1), size=n_samples)]

    # D_sketch0 with n_comp>min(N, D)/2 and D_sketch1 with n_comp<min(N, D)/2 for dense_svd
    D_sketch0 = rstate.randint(min(n_samples, n_features) / 2., n_features)
    D_sketch1 = rstate.randint(1, max(2, min(n_samples, n_features) / 2.))
    proj_list0 = []
    proj_list1 = []
    basis_list0 = []
    basis_list1 = []

    for trial in range(n_trials):
        # ========================== When,
        # We sketch, using a frozen random_state,
        sketcher0 = FastSketch(n_components=D_sketch0, random_state=0)
        sketcher1 = FastSketch(n_components=D_sketch1, random_state=0)
        proj_list0.append(sketcher0.fit_transform(X))
        proj_list1.append(sketcher1.fit_transform(X))
        basis_list0.append(sketcher0.components_)
        basis_list1.append(sketcher1.components_)

    # ======================== Then,
    assert all([np.allclose(proj_list0[0], proj) for proj in proj_list0[1:]]), (
        "All trials must produce the same projections for dense SVD")
    assert all([np.allclose(proj_list1[0], proj) for proj in proj_list1[1:]]), (
        "All trials must produce the same projections for dense SVD")
    return


def test_sketch_reproducibility_large_flat_feat():
    """
    Ensure reproducible outcomes for FastSketch on large datasets
    """
    rstate = np.random.RandomState(0)
    n_trials = 3
    # ====================== Given,
    # large feature matrix X0_flat_feat,
    X = X0_flat_feat
    n_samples, n_features = X.shape
    # D_sketch0 with n_comp>min(N, D)/2 and D_sketch1 with n_comp<min(N, D)/2 for dense_svd
    D_sketch0 = rstate.randint(min(n_samples, n_features) / 2., n_features)
    D_sketch1 = rstate.randint(1, max(2, min(n_samples, n_features) / 2.))
    proj_list0 = []
    proj_list1 = []
    basis_list0 = []
    basis_list1 = []

    for trial in range(n_trials):
        # ========================== When,
        # We sketch, using a frozen random_state,
        sketcher0 = FastSketch(n_components=D_sketch0, random_state=0)
        sketcher1 = FastSketch(n_components=D_sketch1, random_state=0)
        proj_list0.append(sketcher0.fit_transform(X))
        proj_list1.append(sketcher1.fit_transform(X))
        basis_list0.append(sketcher0.components_)
        basis_list1.append(sketcher1.components_)

    # ======================== Then,
    assert all([np.allclose(proj_list0[0], proj) for proj in proj_list0[1:]]), (
        "All trials must produce the same projections for dense SVD")
    assert all([np.allclose(proj_list1[0], proj) for proj in proj_list1[1:]]), (
        "All trials must produce the same projections for dense SVD")
    return

# TODO: Add tests for grid-features using tiled MNIST
