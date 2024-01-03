"""
Linear dimensionality reduction methods used by
    matsketch, projectframe_base modules.
"""
import logging
import warnings

import numpy as np
from jax.scipy.linalg import svd

from ..utils import get_randomstate

logger = logging.getLogger(__name__)


def linear_combi_basis(basis):
    """
    Produce a basis that is a linear combination,
        by multiplying with a random orthonormal matrix.
    """
    rand_arr = np.random.rand(basis.shape[0], basis.shape[0])
    orthonorm = np.array(svd(rand_arr)[0])
    new_basis = orthonorm @ basis
    return new_basis


def compose_sketch(svals, basis):
    """
    Compose sketch from singular values and basis vectors

    Parameters
    ----------
    svals: 1d (D,)

    basis: 2d float array of shape (D, D0)
        Each row is a singular vector

    Returns
    ---------
    sketch: 2d float array of shape (D, D0)
        Each row is a weighted singular vector
    """
    return svals.reshape((-1, 1)) * basis


def svd_flip(basis, projections):
    """
    Ensure that SVD returns sign-consistent vectors

    Parameters
    ----------
    basis: 2d float array
    projections: 2d float array

    Returns
    -------
    basis: 2d float array
    projections: 2d float array

    Example
    -------

    """
    max_abs_rows = np.argmax(np.abs(basis), axis=1)
    signs = np.sign(basis[range(basis.shape[0]), max_abs_rows])
    basis *= signs[:, np.newaxis]
    if isinstance(projections, np.ndarray):
        projections *= signs
    return basis, projections


def _sorted_svd(X, k, tol):
    """
    Dense SVD with the appropriate sorting and signs:
        Singular values are monotonically increasing,
        Polarity ensured by svd_flip()

    Parameters
    ----------
    X: 2d float array of shape (N, D0)
        Features

    k: int
        Rank of SVD

    tol: float
        Tolerance for singular values computed by SVD.
        Ignores extremely small singular values below the specified tolerance.

    Returns
    -------
    svals: 1d float array of shape (k,)
        Singular values

    rsvecs: 2d float array of shape (k, D0)
        Right singular vectors
    """
    _, svals, rsvecs = svd(X, full_matrices=False)
    svals = np.array(svals[:k])
    rsvecs = np.array(rsvecs[:k])
    # jax.scipy.linalg.svd returns svals in descending order by default
    rsvecs, _ = svd_flip(rsvecs, None)  # Ensure consistent polarity
    svals[svals < tol] = 0.  # Ignore extremely small singular values
    return svals, rsvecs


def dense_svd(features, k=None, tol=0.):
    """
    SVD with the appropriate sorting and signs:
        Singular values are monotonically increasing,
        Polarity ensured by svd_flip()

    Parameters
    ----------
    (Positional)
    features: 2d float array of shape (N, D0)
        Features

    (Keyword)
    k: int, required, default=None
        Rank of SVD. If None, use rank of input: as min(N, D0)
    tol: float, optional, default=0.
        Tolerance for singular values computed by SVD.
        Ignores extremely small singular values below the specified tolerance.

    Returns
    -------
    svals: 1d float array of shape (k,)
        Singular values

    rsvecs: 2d float array of shape (k, D0)
        Right singular vectors
    """
    n_samples, n_features = features.shape
    if k is None:
        k = min(n_samples, n_features)  # Use max rank if k is not specified

    try:
        svals, rsvecs = _sorted_svd(features, k, tol)
    except Exception as svd_error:
        raise RuntimeError(
            f"Dense SVD failed during sketching with error {str(svd_error)}")

    return svals, rsvecs


def _is_non_ascending(svals, atol=1.e-6, rtol=1.e-4):
    """
    Return True if svals are not monotonically increasing
    """
    threshold = atol + rtol * svals[0]
    diff_svals = svals[1:] - svals[:-1]
    return (diff_svals <= threshold).all()


def _is_orthonormal_like(basis, tol=5.e-4):
    """
    Returns True if basis vectors are all nearly orthonormal
    """
    covariance = basis @ basis.T
    # Diagonal elements as norm of each vector:
    diag_values = np.diag(covariance).copy()
    # To account for rank deficiency, set zeros to ones
    diag_values[diag_values <= tol] = 1.

    # Check diag values are all almost 1
    diag_diff = diag_values - 1.
    has_zero_or_unit_norm = np.allclose(
        diag_diff, np.zeros(diag_diff.shape), atol=tol)
    # We check elementwise instead of norm so that, in large arrays,
    #   even a single element doesn't become too large

    # Set diagonal elements to zero to compare orthogonality:
    np.fill_diagonal(covariance, 0.)

    # Check that all elements are near zero
    is_orthogonal = np.allclose(
        covariance, np.zeros(covariance.shape), atol=tol)

    return (has_zero_or_unit_norm and is_orthogonal)


def merge_sketches_projections(
        sketch_list, project_list, n_components=None):
    """
    Merge sketches from different partitions and produce a
        merged sketch as well as projections on this sketch

    Parameters
    ----------
    sketch_list: list/array of 2d-arrays, each of shape (D_i, D0)
        Each entry is a sketch for a partition
    project_list: list/array of 2d float arrays, each of shape (N_i, D_i)
        Each entry has projections for a single partition
    n_components: int, optional, default=None
        Number of components to use for merged sketch.
        If None, use largest sketch size in input.

    Returns
    -------
    sketch_global: 2d float array of shape (D, D0)
        Merged sketch
    projections_global: 2d float array of shape (N_total, D)
        Concatenated projections defined on merged sketch
    Note: Size of svals and basis can be less than D,
        if the input has rank less than D.
    """
    svals_global, basis_global = merge_sketches(sketch_list, n_components=n_components)
    # if project_list is a 3d array instead of lists of 2d arrays,
    #   convert to lists for consistency
    if isinstance(project_list, np.ndarray) and project_list.ndim in [3, 5]:
        project_list = list(project_list)
    # Later operations assume these objects are lists of 2D arrays,
    #     and will fail for other types

    project_list_global = []

    # Create list of global projections
    for (ind, projections) in enumerate(project_list):
        # Local basis for each partition
        _, basis_local = decompose_sketch(sketch_list[ind])

        # Append global projections for each partition to list
        project_list_global.append(rotate_by_basis(
            projections, basis_local, basis_global))

    projections_global = np.concatenate(project_list_global, axis=0)
    sketch_global = compose_sketch(svals_global, basis_global)
    return sketch_global, projections_global


def merge_sketches(sketch_list, n_components):
    """
    Merge a list of sketches to produce a new sketch;
        the row-norms of the merged sketch is cumulative on input sketches

    Parameters
    ----------
    sketch_list: list of 2d-arrays, each of shape (D_i, D0)
        Each entry is a sketch for a partition
    n_components: int
        Size (num. of rows) of merged sketch.
        If None, set to twice the size of first sketch.

    Returns
    -------
    svals: 1d float array of shape (D,)
        Singular values for merged sketch
    basis: 2d float array of shape (D, D0)
        Basis vectors for merged sketch

    Note: Size of svals and basis can be less than D,
        if the input has rank less than D.
    """
    # Prepare sketch list for sparse svd
    if isinstance(sketch_list, np.ndarray):
        if sketch_list.ndim == 3:
            n_c = max([len(sketch) for sketch in sketch_list])
            sketch_concat = sketch_list.reshape((-1, sketch_list.shape[-1]))
        elif sketch_list.ndim == 2:
            sketch_concat = sketch_list
            n_c = len(sketch_list)
            # Input sketches weren't separated.
            # Pretend there are 2 sketches of equal size
        else:
            raise ValueError

    elif isinstance(sketch_list, list):
        n_c = max([len(sketch) for sketch in sketch_list])
        sketch_concat = np.concatenate(sketch_list, axis=0)

    else:
        raise ValueError

    # if D is not specified, use twice the 'D' of the first sketch
    if n_components is None:
        n_components = n_c

    # SVD
    svals, basis = dense_svd(sketch_concat, k=n_components)
    return svals, basis


def svals_from_projections(projections):
    """
    Calculate singular values as the component-wise gains;
        the assumption is that the projections are already along the
        directions that are singular vectors.

    Parameters
    ----------
    projections: numpy array of shape (..., n_components)
        2d or 4d numpy array containing projections to a basis

    Returns
    -------
    svals: numpy array of shape (n_components,)
        Singular values for the components associated with current projections,
            produced for the dataset that has these projections.

    Examples
    --------
    >>> proj = np.array([[3., 0.], [4., 0.], [0., 1.]])
    >>> svals_from_projections(proj)
    array([5., 1.])
    >>> # Returns svals in projection space.
    """
    # Reshape to 2d (for UNIFORM PCA sketch type),
    #   so that each patch is considered its own sample.
    projections = projections.reshape((-1, projections.shape[-1]))
    compwise_gains = np.linalg.norm(projections, axis=0)
    return compwise_gains


def compose_sketch_from_projections(projections, basis):
    """
    Create sketch from projections and basis,
        by computing gains from projection array.

    Parameters
    ----------
    projections: numpy array of shape (..., n_components)
        2d or 4d numpy array containing projections to a basis

    basis: numpy array of shape (n_components, n_features)
        Basis over which above projections are defined.

    Returns
    -------
    sketch: numpy array of shape (n_components, n_features)
        Sketch that scales the basis by the gains along each
            direction, as relevant for the current projections.

    Examples
    --------
    >>> # Projections where first component should gain 5 (RSS) and second 1,
    >>> #   here, 'gain' refers to the svals: root of sum of squares
    >>> proj = np.array([[3., 0.], [4., 0.], [0., 2.]]).reshape(3, 1, 1, 2)
    >>> # And basis is just (shuffled) standard basis of rank 2 in 3d.
    >>> basis = np.array([[0., 1., 0.], [1., 0., 0.]])
    >>> compose_sketch_from_projections(proj, basis)
    array([[0., 5., 0.],
           [2., 0., 0.]])
    >>> # First basis has a gain (sval) of 5, second has 2.
    """
    # First, check that shapes are consistent.
    n_components, _ = basis.shape
    if projections.shape[-1] != n_components:
        raise ValueError(
            "The projections have inconsistent shape w.r.t. basis. "
            f"Shapes are {projections.shape} and {basis.shape}.")

    # Gains along each component in basis are,
    compwise_gains = svals_from_projections(projections)
    #   and the sketch is defined by scaling basis with gains as,
    sketch = compwise_gains.reshape((n_components, 1)) * basis
    return sketch


def project_to_basis(X, basis):
    """
    Project features to low-rank basis

    Parameters
    ----------
    X: 4d array of shape (n_samples, n_rows, n_cols, per_patch_features)
        Patchwise features provided by some featurizer.

    basis: 2d array of shape (n_components, per_patch_features)
        Low-rank basis for dimensionality reduction.

    Returns
    ---------
    projections: 2d array of shape (n_samples, n_rows, n_cols, n_components)
        Projections to the low-rank basis.

    Examples
    --------
    >>> X = np.array([[3., 2., 1., 0.], [3., 4., 5., 6.]]).reshape(2, 1, 1, 4)
    >>> # A simple standard basis subset of low-rank:
    >>> basis = np.array([[0., 0., 1., 0.], [0., 1., 0., 0.]])
    >>> projections = project_to_basis(X, basis)
    >>> # Projections be to 2 components per patch:
    >>> projections.shape
    (2, 1, 1, 2)
    >>> # And should be for the 2th and 1th features in original array,
    >>> projections.reshape(2, 2)
    array([[1., 2.],
           [5., 4.]])
    """
    return X @ basis.T


def reconstruct_from_basis(projections, basis):
    """
    Reconstruct original features from low-rank projections.

    Parameters
    ----------
    projections: 4d array of shape (n_samples, n_rows, n_cols, n_components)
        Projections to the below low-rank basis.

    basis: 2d array of shape (n_components, per_patch_features)
        Low-rank basis used to define above projections

    Returns
    ---------
    reconstruction: 4d array of shape (n_samples, n_rows, n_cols,
                                                per_patch_features)
        Reconstructed feature component in original feature space.

    Examples
    --------
    >>> # Using the same data as `project_to_basis` to start with.
    >>> X = np.array([[3., 2., 1., 0.], [3., 4., 5., 6.]]).reshape(2, 1, 1, 4)
    >>> # A simple standard basis subset of low-rank:
    >>> basis = np.array([[0., 0., 1., 0.], [0., 1., 0., 0.]])
    >>> projections = project_to_basis(X, basis)
    >>> # Projections be to 2 components per patch:
    >>> projections.shape
    (2, 1, 1, 2)
    >>> # And should be for the 2th and 1th features in original array,
    >>> projections.reshape(2, 2)
    array([[1., 2.],
           [5., 4.]])
    >>> # Now we reconstruct,
    >>> X_recons = reconstruct_from_basis(projections, basis)
    >>> X_recons.shape
    (2, 1, 1, 4)
    >>> # Will be back to original space, but will lose info
    >>> X_recons.reshape(2, 4)
    array([[0., 2., 1., 0.],
           [0., 4., 5., 0.]])
    """
    return projections @ basis


def decompose_sketch(sketch):
    """
    Decompose sketch into singular values and basis vectors

    Parameters
    ----------
    sketch: 2d float array

    Returns
    -------
    svals: 1d array (D,)
    basis: 2d float array of shape (D, D0)

    Examples
    --------
    >>> # Simple sketch
    >>> sketch = np.array([[2., 0.], [0., 1.]])
    >>> svals, basis = decompose_sketch(sketch)
    >>> svals
    array([2., 1.])
    >>> basis
    array([[1., 0.],
           [0., 1.]])
    """
    assert sketch.ndim == 2
    svals = np.linalg.norm(sketch, axis=1)
    if not _is_non_ascending(svals):
        warnings.warn("Components of sketch are not ranked according to importance.")

    if svals[-1] == 0:
        svals_tmp = svals.copy()
        svals_tmp[svals == 0] = 1.  # Avoid divide by zero
        basis = sketch / svals_tmp.reshape((-1, 1))
        # Some vectors in basis will be zero. But that's okay.
        # Retaining these directions is irrelevant anyway.
    else:
        basis = sketch / svals.reshape((-1, 1))

    # We also have to worry about numerical tolerances when svals are tiny
    # So that (sketch[ix]/svals[ix]) is a unit vector, which may not
    #   be the case when svals[ix] <<<<< 1
    tol = 1.e-15  # We'll modify basis when sval < tol
    for ix, sval in enumerate(svals):
        if sval ** 2 < tol:
            basis[ix] = basis[ix] / (tol + np.linalg.norm(basis[ix]))

    return svals, basis


def rotate_by_basis(projections, orig_basis, new_basis, check_basis=True):
    """
    Transform projections from one basis to another

    Parameters
    ----------
    (Positional)
    projections: 4d array of shape (n_samples, n_rows, n_cols, n_components_0)
        Patchwise projections for a feature component, defined for the
            following basis.
    orig_basis: 2d array of shape (n_components_0, per_patch_features)
        Basis in which 'projections' are defined.
    new_basis: 2d array of shape (n_components_1, per_patch_features)
        Basis to transform to.

    Returns
    --------
    new_projections: 4d array of shape
                        (n_samples, n_rows, n_cols, n_components_1)
        Projections after transforming to the new basis.

    Examples
    --------
    >>> proj = np.array([[3., 2.], [2., 1.], [1., 0.]]).reshape(3, 1, 1, 2)
    >>> # Original basis is a shuffled, rank-deficient standard basis,
    >>> basis0 = np.array([[0., 1., 0.], [1., 0., 0.]])
    >>> # And the new basis is a full-rank, standard basis.
    >>> basis1 = np.identity(3)
    >>> rotated_proj = rotate_by_basis(proj, basis0, basis1)
    >>> # Output should be a 4d array, with one extra feature in last one.
    >>> rotated_proj.shape
    (3, 1, 1, 3)
    >>> # Rotating should just change coords, and add zeros for last feat.
    >>> rotated_proj.reshape(3, 3)
    array([[2., 3., 0.],
           [1., 2., 0.],
           [0., 1., 0.]])
    """
    if projections.ndim == 2:
        n_samples, n_features = projections.shape
        projections = projections.reshape((n_samples, 1, 1, n_features))
        flattened = True
    else:
        flattened = False

    assert projections.ndim == 4, (
        "Projections must be a 4d array (3d per sample)")
    assert orig_basis.ndim == 2, (
        "Basis must have shape (n_basis_dimensions, n_features)")
    assert new_basis.ndim == 2, (
        "Basis must have shape (n_basis_dimensions, n_features)")
    # Ensure orthonormality of both bases
    # Just in case we accidentally call them on sketches instead of bases
    if check_basis:
        assert _is_orthonormal_like(orig_basis)
        assert _is_orthonormal_like(new_basis)

    # Uniform PCA treats each patch as an individual sample,
    #   and does the rotation along only the last axis.
    # This can be done directly using the following matrix multiplication,
    #   after the rotation matrix is defined by the two bases.
    new_projections = projections @ (orig_basis @ new_basis.T)
    # We didn't have to flatten the first three axes into a single one here.

    if flattened:
        new_projections = new_projections.reshape(n_samples, -1)
    return new_projections


def _sparse_project(X, n_components, frac=0.3, tol=0., random_state=0):
    """
    Use SVD and projection-based corrections for cheap decomposition

    Parameters
    ---------
    (Positional)
    X: 2d float array of shape (N, n_features)
        Features

    n_components: int
        Target number of components for projections

    (Keyword)
    frac: float, required, default=0.3
        Number of rows of X to use for sparse-SVD

    tol: float, optional, default=0.
        Tolerance for singular values computed by SVD.
        Ignores extremely small singular values below the specified tolerance.

    Returns
    -------
    sketch: 2d float array of shape (n_components, n_features)
        Sketch (weighted right singular vectors)

    projections: 4d float array of shape (N, n_components)
        Projections of features 'X' to the above sketch
    """
    # pylint: disable = too-many-locals
    # pylint: disable = too-many-arguments
    n_patches, _ = X.shape
    frac = max(0., min(frac, 1.))

    # Create mask to choose a uniform subsample
    random_state = get_randomstate(random_state)
    mask = random_state.rand(n_patches) < frac
    # It is possible that not enough points are selected by the mask,
    #   when the data is tiny.
    X_to_use = X[mask]
    if len(X_to_use) < n_components:
        X_to_use = X[:min(n_components, len(X))]

    # SVD on subsample
    svals, basis = dense_svd(X_to_use, k=n_components, tol=tol)

    assert len(svals) > 0, "SVD must produce at least 1 singular value"

    # Project points excluding the subsample
    Y = X[~mask] @ basis.T
    Y_sq = np.sum(Y ** 2, axis=0)
    svals = np.sqrt(svals ** 2 + Y_sq)

    # Reorder rows according to svals
    sval_order = np.argsort(svals)[::-1]
    svals = svals[sval_order]
    basis = basis[sval_order]

    # Finally, calculate sketch, projections, and error
    projections = project_to_basis(X, basis)
    sketch = compose_sketch(svals, basis)
    return sketch, projections


# If there are too many rows, sparse_project may start being slow/inaccurate
# Break the partition up into blocks and sketch on each block separately
# Merge blocks in the end
def block_sparse_project(
        features, n_components,
        frac=0.3, n_blocks=1, tol=0., random_state=0):
    """
    Use sparse-SVD and projection-based corrections for cheap decomposition,
        along with blocks to improve accuracy

    Parameters
    ---------
    (Positional)
    features: 2d float array of shape (N, n_features)
        Features

    n_components: int
        Target number of components for projections

    (Keyword)
    frac: float, required, default=0.3
        Number of rows of X to use for SVD

    n_blocks: int, required, default=1
        Number of blocks to split input data into

    tol: float, optional, default=0.
        Tolerance for sparse SVD

    random_state: int or np.random.RandomState, default=0
        Random state to used for selecting fraction of samples

    Returns
    -------
    sketch: 2d float array of shape (n_components, n_features)
        Sketch (weighted right singular vectors)

    projections: 2d float array of shape (N, n_components)
        Projections of features 'X' to the above sketch
    """
    # pylint: disable=too-many-locals
    # pylint: disable = too-many-arguments

    if n_blocks > 1:
        logger.warning("When n_blocks>1 the results obtained may not be perfectly "
                       "reproducible.")

    # Split data into multiple blocks for blockwise sketching,
    #   and merge sketches in the end.
    n_samples, n_rows, n_cols, n_features = features.shape
    features = features.reshape(-1, n_features)
    n_patches = len(features)
    block_size = int(np.ceil(n_patches / n_blocks))
    i1 = 0
    sketch_list = []
    project_list = []
    for block_num in range(n_blocks):
        i0 = i1
        i1 = min(i0 + block_size, n_patches)
        X = features[i0:i1]
        # break the loop if there aren't enough rows(>0) in the data to
        # continue.
        if not (len(X) > 0):
            logger.debug(f"Breaking... Not enough rows in input data to "
                         f"continue _block_sparse_project iteration. "
                         f"block_size: {block_size}, block_no: {block_num}.")
            break
        # Sketch separately for each block
        sketch, projections = _sparse_project(X, n_components,
                                              frac=frac, tol=tol,
                                              random_state=random_state)

        sketch_list.append(sketch)
        project_list.append(projections)

    if n_blocks > 1:
        sketch_global, projections_global = merge_sketches_projections(
            sketch_list, project_list, n_components=n_components)
    else:
        sketch_global = sketch_list[0]
        projections_global = project_list[0]

    projections_global = projections_global.reshape(
        n_samples, n_rows, n_cols, len(sketch_global))

    return sketch_global, projections_global
