"""
Test new sketch utils introduced for v2 (patchwise features)
"""
from random import randint

import numpy as np
import pytest

from akriml.sketch.sketch_utils import (
    _is_non_ascending,
    _is_orthonormal_like, compose_sketch,
    decompose_sketch, linear_combi_basis,
    project_to_basis, reconstruct_from_basis,
    rotate_by_basis, dense_svd, svd_flip)
from akriml.utils import deco_repeat as repeat
from akriml.utils import get_randomstate, rep_error_mean, rep_error_pointwise
from tests.test_utils import random_arr, MAX_ARR_DIM


def random_wide_arr(**kwargs):
    n_rows = kwargs.get('n_rows', randint(1, MAX_ARR_DIM))
    max_cols = max(n_rows + 1, MAX_ARR_DIM)
    n_cols = kwargs.get('n_cols', randint(n_rows, max_cols))
    random_state = kwargs.get('random_state', randint(0, 42))
    np.random.seed(random_state)
    return np.random.rand(n_rows, n_cols)


def random_tall_arr(**kwargs):
    n_cols = kwargs.get('n_cols', randint(1, MAX_ARR_DIM))
    max_rows = max(n_cols + 1, MAX_ARR_DIM)
    n_rows = kwargs.get('n_rows', randint(n_cols, max_rows))
    random_state = kwargs.get('random_state', randint(0, 42))
    np.random.seed(random_state)
    return np.random.rand(n_rows, n_cols)


def random_square_arr(**kwargs):
    n_rows = kwargs.get('n_rows', randint(1, MAX_ARR_DIM))
    random_state = kwargs.get('random_state', randint(0, 42))
    np.random.seed(random_state)
    return np.random.rand(n_rows, n_rows)


class TestDecomposeSketch:
    rtol = 1.e-6
    atol = 1.e-6

    @repeat()
    def test_eye(self):
        # ============Given,
        n_rows = randint(1, MAX_ARR_DIM)
        n_cols = randint(n_rows, MAX_ARR_DIM)  # Sketch should be wide
        # Sample unit vectors from identity matrix
        eye = np.identity(n_cols)
        basis = eye[np.random.choice(n_cols, size=n_rows)]

        # Multiply basis by random, decreasing numbers
        svals = 100. * np.random.rand(n_rows)
        svals = np.sort(svals)[::-1]
        sketch = svals.reshape((-1, 1)) * basis

        # ============When,
        # decompose_sketch should recover svals and basis from sketch
        # default sketch_type=SketchTypes.UNIFORM_PCA
        out_svals, out_basis = decompose_sketch(sketch)

        # ============Then...
        np.testing.assert_allclose(
            out_svals, svals, rtol=self.rtol, atol=self.atol)
        np.testing.assert_allclose(
            out_basis, basis, rtol=self.rtol, atol=self.atol)
        return

    @repeat()
    def test_rand(self):
        # ============Given,
        n_rows = randint(1, MAX_ARR_DIM)
        n_cols = randint(n_rows, MAX_ARR_DIM)  # Sketch should be wide
        # Sample basis vectors as right singular vectors of random matrix
        tmpArr = 10. * np.random.rand(n_rows, n_cols)
        _, basis = dense_svd(tmpArr, k=n_rows)
        basis, _ = svd_flip(basis, None)

        # Multiply basis by random, decreasing numbers
        svals = 100. * np.random.rand(n_rows)
        svals = np.sort(svals)[::-1]
        sketch = svals.reshape((-1, 1)) * basis

        # ============When,
        # decompose_sketch should recover svals and basis from sketch
        # default sketch_type=SketchTypes.UNIFORM_PCA
        out_svals, out_basis = decompose_sketch(sketch)

        # ============Then...
        np.testing.assert_allclose(
            out_svals, svals, rtol=self.rtol, atol=self.atol)
        np.testing.assert_allclose(
            out_basis, basis, rtol=self.rtol, atol=self.atol)
        return


@pytest.mark.parametrize('seed', range(5))
def test_decompose_sketch_zero_dimensions(seed):
    """
    decompose_sketch should produce an orthonormal basis even for directions
        with near-zero norms.
    """
    rstate = get_randomstate(seed)
    # ============================ Given,
    # A sketch computed using SVD or some random data,
    # Data:
    n_features = rstate.randint(4, 24)
    n_samples = rstate.randint(n_features, 100)
    n_components = rstate.randint(4, n_features)
    datapoints = rstate.rand(n_samples, n_features)
    svals0, basis0 = dense_svd(datapoints, k=n_components)
    # But with last few dimensions deliberately made to have tiny norms,
    sketch = compose_sketch(svals0, basis0)
    sketch[-3] *= 1.e-10
    sketch[-2] *= 1.e-20
    sketch[-1] *= 1.e-22

    # ========================= When,
    # We decompose this sketch,
    # default sketch_type=SketchTypes.UNIFORM_PCA
    svals, basis = decompose_sketch(sketch)

    # ========================== Then,
    assert _is_orthonormal_like(basis), (
        "Basis from sketch should be orthonormal")
    assert np.allclose(sketch, compose_sketch(svals, basis)), (
        "The sketch should be recovered except for trivial diffs")
    return


# ====================================================
# svd_flip
@pytest.mark.parametrize('counter', [(5, 7, 3), (11, 6, 6), (13, 13, 4)])
def fun_flip(wide_arr, tall_arr):
    # ============Given,
    d_sketch = min(wide_arr.shape[0], tall_arr.shape[1])
    # svd_flip doesn't care about orthonormality
    basis0 = -0.5 + wide_arr[:d_sketch]
    projections0 = -0.5 + tall_arr[:, :d_sketch]

    # ============When,
    basis, projections = svd_flip(basis0, projections0)  # Flips only signs

    # ============Then...
    # Row-wise norms shouldn't change
    np.testing.assert_array_equal(
        np.diag(basis @ basis.T), np.diag(basis0 @ basis0.T))

    # Test shapes
    assert basis.shape == basis0.shape
    assert projections.shape == projections0.shape

    # ============When,
    # Subsequent applications of svd_flip shouldn't change anything
    basis1, projections1 = svd_flip(basis, projections)

    # ============Then...
    np.testing.assert_array_equal(basis1, basis)
    np.testing.assert_array_equal(projections1, projections)

    # ============When,
    # Even if we multiply some basis vectors by -1
    randomRows = np.random.randint(d_sketch, size=int(d_sketch / 2))
    basis1[randomRows] *= -1.
    projections1[:, randomRows] *= -1.
    basis2, projections2 = svd_flip(basis1, projections1)

    # ============Then...
    np.testing.assert_array_equal(basis2, basis)
    np.testing.assert_array_equal(projections2, projections)

    return


@repeat()
def test_flip():
    basis = random_wide_arr()
    projections = random_tall_arr(n_cols=basis.shape[0])
    fun_flip(basis, projections)
    return


class TestDenseSVD:
    rtol = 1.e-5
    atol = 1.e-5

    @repeat()
    def test_diag(self):
        # ============Given,
        n_rows = randint(1, MAX_ARR_DIM)
        svals = 1.5 ** (np.arange(n_rows)[::-1])
        X = np.diag(svals)
        eye = np.identity(svals.size)
        k = randint(1, n_rows)

        # ============When,
        out_svals, out_rsvecs = dense_svd(X, k=k, tol=0.)

        # ============Then...
        np.testing.assert_allclose(out_svals, svals[:k],
                                   rtol=self.rtol, atol=self.atol)
        np.testing.assert_allclose(out_rsvecs, eye[:k],
                                   rtol=self.rtol, atol=self.atol)
        return

    @repeat()
    def test_random(self):
        # ============Given,
        X = random_arr()
        d_sketch = randint(1, min(X.shape))

        # Compare against standard dense SVD
        _, svals, rsvecs = np.linalg.svd(X, full_matrices=False)
        svals = svals[:d_sketch]
        rsvecs = rsvecs[:d_sketch]
        rsvecs, _ = svd_flip(rsvecs, None)

        # ============When,
        out_svals, out_rsvecs = dense_svd(X, k=d_sketch, tol=0.)

        # ============Then...
        assert out_svals.shape == (d_sketch,)
        assert out_rsvecs.shape == (d_sketch, X.shape[1])

        np.testing.assert_allclose(out_svals, svals,
                                   rtol=self.rtol, atol=self.atol)
        np.testing.assert_allclose(out_rsvecs, rsvecs,
                                   rtol=self.rtol, atol=self.atol)
        return


class TestSketchOps:
    n_trials = 5
    atol = 1.e-6
    rtol = 1.e-6

    def _reconstruct_by_rank_basis(self, tmpArr, rank):
        rank = min(rank, min(tmpArr.shape))
        svals, basis = dense_svd(tmpArr, k=rank)
        projections = project_to_basis(tmpArr, basis)
        reconstruction = reconstruct_from_basis(
            projections, basis)
        return reconstruction

    @repeat()
    def test_full_reconstruct(self):
        # ============Given,
        tmpArr = random_square_arr()

        # ============When,
        svals, basis = dense_svd(tmpArr, k=len(tmpArr))

        projections_b = project_to_basis(tmpArr, basis)
        reconstruction_b = reconstruct_from_basis(
            projections_b, basis)

        # ============Then...
        assert np.allclose(
            tmpArr, reconstruction_b,
            rtol=self.rtol, atol=self.atol)
        return

    @repeat()
    def test_partial_reconst_err(self):
        """ Ensure reconstruction error decreases
                as sketch dimensionality decreases.
        """
        num_ranks = 4  # Check for so many ranks/dimensionalities
        # ============Given,
        tmpArr = random_tall_arr(n_rows=100, n_cols=16)

        error_list = []
        max_rank = min(tmpArr.shape)
        trial_ranks = np.random.choice(max_rank - 1, size=num_ranks)
        trial_ranks = np.insert(trial_ranks, num_ranks, max_rank)
        # Include max rank
        trial_ranks = np.sort(trial_ranks)  # Rank in ascending order

        # ============When,
        for rank in trial_ranks:
            reconstruction = self._reconstruct_by_rank_basis(
                tmpArr, rank)
            error_list.append(rep_error_mean(
                tmpArr, reconstruction))

        # ============Then...
        # As rank increases, error must decrease (or remain constant)
        assert _is_non_ascending(np.array(error_list))
        # And error for full rank should be near-zero
        assert error_list[-1] <= self.atol
        # In fact, the relative error can be directly compared
        #     against rank...
        # In a hand-wavy way, worst case errors are 1-(rank)/max_rank
        up_bound_error = 1. - trial_ranks / max_rank
        # Allow for some numerical tolerance
        up_bound_error = self.atol + (1. + self.rtol) * up_bound_error
        assert (np.array(error_list) <= up_bound_error).all()

        return


class TestRotate:
    rtol = 1.e-5
    atol = 1.e-5

    def approx_equal(self, arr1, arr2):
        np.testing.assert_allclose(
            arr1, arr2,
            atol=self.atol, rtol=self.rtol)
        return

    @repeat()
    def test_identity_basis(self):
        """ Ensure projections are invariant when the same basis is used"""
        # ============Given,
        tmpArr = random_tall_arr(n_rows=100, n_cols=16)
        k = randint(1, min(tmpArr.shape))
        svals, basis = dense_svd(tmpArr, k=k)
        projections = project_to_basis(tmpArr, basis)

        # ============When,
        # Project to the same basis
        new_basis = basis
        new_projections = rotate_by_basis(projections, basis, new_basis)

        # ============Then...
        self.approx_equal(projections, new_projections)
        return

    @repeat()
    def test_linear_combi(self):
        """ Ensure reconstruction is invariant for same sketch subspace"""
        # ============Given,
        tmpArr = random_tall_arr(n_rows=100, n_cols=16)
        k = randint(1, min(tmpArr.shape))
        svals, basis = dense_svd(tmpArr, k=k)
        projections = project_to_basis(tmpArr, basis)

        # ============When,
        new_basis = linear_combi_basis(basis)
        # Rotate to new basis
        new_projections = rotate_by_basis(
            projections, basis, new_basis)

        # ============Then...
        # Ensure reconstructions are the same
        reconstruction = reconstruct_from_basis(projections, basis)
        new_reconstruction = reconstruct_from_basis(
            new_projections, new_basis)
        self.approx_equal(reconstruction, new_reconstruction)

        # =============When,
        # Rotate back to original basis
        final_projections = rotate_by_basis(
            new_projections, new_basis, basis)
        final_reconstruction = reconstruct_from_basis(
            final_projections, basis)

        # ==============Then...
        self.approx_equal(final_projections, projections)
        self.approx_equal(final_reconstruction, reconstruction)
        return

    @repeat()
    def test_ortho_basis(self):
        """ Ensure rotations to orthogonal basis produces zeroes"""
        # ============Given,
        tmpArr = random_tall_arr(n_rows=100, n_cols=16)
        k = randint(1, min(tmpArr.shape) - 1)
        # Obtain more than 'k' basis vectors
        k1 = min(2 * k, min(tmpArr.shape))
        svals, basis0 = dense_svd(tmpArr, k=k1)
        # Project to first 'k' out of 'k1' basis vectors
        basis = basis0[:k]
        projections = project_to_basis(tmpArr, basis)

        # ============When,
        # Rotate by remaining orthogonal vectors
        new_basis = basis0[k:k1]
        new_projections = rotate_by_basis(
            projections, basis, new_basis)

        # ============Then,
        # Check that new projections are all zeroes
        self.approx_equal(new_projections, np.zeros(new_projections.shape))
        return

    @repeat()
    def test_energy_loss(self):
        """ Ensure error due to partial basis is proportional to svals"""
        # ============Given,
        # Project to optimal basis
        tmpArr = random_tall_arr(n_rows=100, n_cols=24)  # Array of interest
        k = randint(8, 24)  # Keep at least 8 basis vectors
        svals, basis = dense_svd(tmpArr, k=k)
        projections = project_to_basis(tmpArr, basis)
        # Drop 3 basis vectors
        indices_drop = np.random.choice(k, size=3)
        mask_drop = np.in1d(np.arange(k), indices_drop)
        mask_retain = ~mask_drop
        new_basis = basis[mask_retain]

        # ============When,
        # Rotate to a subset of basis vectors
        new_projections = rotate_by_basis(
            projections, basis, new_basis)

        # ============Then...
        # Reconstructions
        reconstruction = reconstruct_from_basis(
            projections, basis)
        new_reconstruction = reconstruct_from_basis(
            new_projections, new_basis)
        # The error for new_reconstruction (compared to 'reconstruction')
        #     should be proportional to svals[mask_drop]
        error_pointwise = rep_error_pointwise(
            reconstruction, new_reconstruction)
        expected_error = (np.linalg.norm(projections[:, mask_drop], axis=1) /
                          np.linalg.norm(projections, axis=1))
        self.approx_equal(error_pointwise, expected_error)
        return


class TestMerge:
    n_rows = 100
    n_cols = 24
    rtol = 1.e-9
    atol = 1.e-11

    def approx_equal(self, arr1, arr2, atol=None, rtol=None):
        if atol is None:
            atol = self.atol
        if rtol is None:
            rtol = self.rtol
        np.testing.assert_allclose(
            arr1, arr2,
            atol=atol, rtol=rtol)
        return
