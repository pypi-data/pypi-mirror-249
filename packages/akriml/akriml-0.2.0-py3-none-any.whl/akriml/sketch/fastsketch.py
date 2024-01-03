"""
fastsketch.py
Defines `FastSketch` that provides a PCA-like estimator for linear dimensionality reduction,
with similar functionality, but works much faster. The speed-up is achieved by running SVD
on nested subsets of a dataset.
Supports 4d arrays as input, to handle grid-based features for an image.
When sketching, the grid is flattened,
    from (n_samples, n_rows, n_cols, n_features) to (-1, n_features)
"""
import logging
from typing import Union, Tuple

import numpy as np
from numpy.typing import NDArray
from sklearn.decomposition import PCA

from .sketch_utils import (block_sparse_project, compose_sketch,
                           decompose_sketch, get_randomstate,
                           merge_sketches, project_to_basis,
                           reconstruct_from_basis)

logger = logging.getLogger(__name__)

TINY_VAL = 1.e-16


class FastSketch(PCA):
    """
    Sketching to make (linear) reduced dimeinsional representations cheaper to compute.
    Inherits sklearn.decomposition.PCA

    Parameters
    ----------
    (Keyword)
    n_components: int (=64)
        Proxy for 'D' to allow for pandas' notation
    frac: float (=0.2)
        Fraction of rows to use for SVD.
        The rest are projected to modify singular values.
        Only valid for algorithm='custom'
    tol: float, (=0)
        Tolerance for singular values computed by SVD.
        Ignores extremely small singular values below the specified tolerance.
    n_blocks: int  (=1)
        Number of blocks to split fitting data into.
    overwrite: bool (=True)
        If False, subsequent calls of .fit and .fit_transform
            incrementally train the model.
        If True, subsequent calls overwrite previous components.
    skip_rotate: bool, default=False)
        If True and n_components=n_features, do not rotate the basis by energy content.
        This is used to skip the sketching process when no dimensionality reduction is needed.
        Default is set to False for backwards compatibility.
    random_state: int or np.random.RandomState, default=0
        Random state to use for SVD and block calculations
    **kwargs : All keyword arguments accepted by sklearn.decomposition.PCA,
        except for n_components

    Attributes
    ----------
    (Modified from source for `sklearn.decomposition.PCA`)

    skip_rotate: bool
        Copied from input param
    components_ : array, shape (n_components, n_features)
        Principal axes in feature space, representing the directions of
        maximum variance in the data. The components are sorted by
        ``explained_variance_``.
    explained_variance_ : array, shape (n_components,)
        The amount of variance explained by each of the selected components.
        Equal to n_components largest eigenvalues of X X^T (X is a 2d array).
        We don't do mean correction, so it's not exactly a covariance matrix.
    explained_variance_ratio_ : array, shape (n_components,)
        Percentage of variance explained by each of the selected components.
    singular_values_ : array, shape (n_components,)
        The singular values corresponding to each of the selected components.
        The singular values are equal to the 2-norms of the ``n_components``
        variables in the lower-dimensional space.
    mean_ : array, shape (n_features,)
        Per-feature empirical mean, estimated from the training set.
        It's set to zero because we do not do mean correction in FastSketch.
    n_components_ : int
        The number of components, as specified during init.
    noise_variance_ : float
        The estimated noise covariance following the Probabilistic PCA model from Tipping
        and Bishop 1999. See "Pattern Recognition and Machine Learning" by C. Bishop,
        12.2.1 p. 574 or
        http://www.miketipping.com/papers/met-mppca.pdf. It is required to compute the
        estimated data covariance and score samples.
        Equal to the average of (min(n_features, n_samples) - n_components) smallest
        eigenvalues of the covariance matrix of X.

    Notes
    -----
    If the input 'X' is a 4d tensor of shape:
        (n_samples, n_row_patches, n_col_patches, n_features).
        where, n_features corresponds to n_features per patch
    Then, the 4d input X is converted to a 2d array for internal svd operations
    and has shape: (total_patches, n_features)
        where, total_patches = n_samples * n_row_patches * n_col_patches
        ie; Each patch is considered like an individual sample.

    The output is again reshaped back to a 4d tensor of shape:
        (n_samples, n_row_patches, n_col_patches, n_components_)

    References
    ----------
    TODO: Add notes on the original paper, and link to our own at some point

    Examples
    --------
    Create a simple dataset in 3d, but with data along only two directions:
    [1, 1, 0] and [-1, 1, 0]. Sketching to 2d projects the data along these directions.

    >>> X = np.array([[1., 1., 0.], [2., 2., 0.], [3., 3., 0.],
    ...               [-0.5, 0.5, 0.], [1., -1., 0.]])
    >>> sketcher = FastSketch(n_components=2)
    >>> rt2 = np.sqrt(2.)
    >>> exp_basis = np.array([[1., 1., 0.], [1., -1., 0.]])/rt2
    >>> exp_proj = rt2 * np.array([[1., 2, 3, 0, 0], [0, 0, 0, -0.5, 1]]).T
    >>> np.round(exp_basis, 2)  # We expect this basis (components)...
    array([[ 0.71,  0.71,  0.  ],
           [ 0.71, -0.71,  0.  ]])
    >>> np.round(exp_proj, 2)  # And these projections along the (unit-) bases.
    array([[ 1.41,  0.  ],
           [ 2.83,  0.  ],
           [ 4.24,  0.  ],
           [ 0.  , -0.71],
           [ 0.  ,  1.41]])
    >>> proj = sketcher.fit_transform(X)
    >>> proj.shape  # For each sample, n_components projections.
    (5, 2)
    >>> # Compare abs values to avoid sign issues
    >>> np.allclose(np.abs(proj), np.abs(exp_proj), atol=1.e-5, rtol=1.e-5)
    True
    >>> np.allclose(np.abs(sketcher.components_), np.abs(exp_basis), atol=1.e-5, rtol=1.e-5)
    True

    For the same data, if input is a 4d tensor, output is also 4d.

    >>> X4d = X.reshape((5, 1, 1, 3))
    >>> proj4d = sketcher.fit_transform(X4d)
    >>> proj4d.shape
    (5, 1, 1, 2)
    >>> np.allclose(np.abs(proj4d.reshape(5, 2)), np.abs(exp_proj), atol=1.e-5, rtol=1.e-5)
    True

    When dimensionality reduction is not needed, the samples can either be rotated to align
    with the components ranked by energy, or just left as they are. Consider a 3d dataset
    with a clear ranking of components by energy.

    >>> features = np.array([
    ...        [2., 2., 0.],  # Most energetic direction
    ...        [1., -1., 0.],  # Second most energetic, orthogonal to the first.
    ...        [0., 0., 1.],  # And the 3rd orthogonal direction
    ...        ])

    By default, the sketching will rotate the components to align by energy.

    >>> sketcher_rotate = FastSketch(n_components=3)  # Defaults to rotating.
    >>> np.round(sketcher_rotate.fit_transform(features), 2)  # Along the rotated directions
    array([[ 2.83,  0.  ,  0.  ],
           [ 0.  , -1.41,  0.  ],
           [ 0.  ,  0.  ,  1.  ]])
    >>> np.round(sketcher_rotate.components_, 2)  # The dominant directions by rotation
    array([[ 0.71,  0.71,  0.  ],
           [-0.71,  0.71,  0.  ],
           [ 0.  ,  0.  ,  1.  ]])

    To skip the rotation, the `skip_rotate` param must be passed. The projections will be
    the same as the input features, and the basis (components_) will be identity.

    >>> sketcher_no_rotate = FastSketch(n_components=3, skip_rotate=True)
    >>> np.array_equal(sketcher_no_rotate.fit_transform(features), features)
    True
    >>> np.array_equal(sketcher_no_rotate.components_, np.identity(3))
    True
    >>> sketcher_no_rotate.noise_variance_ < TINY_VAL
    True
    """

    # pylint: disable = too-many-instance-attributes
    # pylint: disable = too-many-arguments
    # Because for these classes, it's better to clearly define all
    #   the nice little params

    def __init__(self, n_components: int = 64,
                 tol: float = 0., frac: float = 0.2, n_blocks: int = 1,
                 overwrite: bool = True, skip_rotate: bool = False,
                 random_state: Union[int, np.random.RandomState] = 0,
                 **kwargs):

        super().__init__(n_components=n_components,
                         random_state=get_randomstate(random_state),
                         **kwargs)

        if len(kwargs):
            logger.debug(f'Initialized self as PCA subclass, '
                         f"with PCA kwargs keys: {kwargs.keys()}")
            logger.debug(
                "The kwargs' functionality is likely overridden. "
                "Have a look into this.")

        self.frac = frac
        self.n_blocks = n_blocks
        self.overwrite = overwrite
        self.tol = tol
        self.random_state = random_state
        self.skip_rotate = bool(skip_rotate)

        # pylint complains about attributes defined outside init,
        #   We'll list all attributes assigned during fit here, and assign dummy values.
        self.mean_ = np.empty(0)
        # We don't do mean-correction, but assigning it for PCA-compatibility
        self.n_features_in_ = -1
        self.n_samples_ = -1
        self.n_samples_seen_ = 0  # This will be a running counter
        self.components_ = np.empty(0)
        self.n_components_ = -1
        self.explained_variance_ = np.empty(0)
        self.explained_variance_ratio_ = np.empty(0)
        self.noise_variance_ = np.empty(0)
        self.singular_values_ = np.empty(0)
        self.sketch_ = np.empty(0)
        return

    def fit(self, X: NDArray[np.floating], y: None = None):
        """
        Create sketch on the data and return the matsketch instance.

        Parameters
        ----------
        (Positional)
        X: NDArray[np.floating] of ndim = 2 or 4
            Features for dataset,
            If 2d, has shape: (n_samples, n_features)
            If 4d, has shape: (n_samples, n_row_patches, n_col_patches, n_features)
        y: None, default=None
            Dummy variable for consistency with estimator

        Returns
        -------
        self: FastSketch
            Fitted instance
        """
        if X.ndim == 2:
            X = X.reshape((X.shape[0], 1, 1, X.shape[1]))
        elif X.ndim != 4:
            raise ValueError("Input 'X' must be a 2d or 4d array.")

        self._fit_custom(X, self.n_components)

        logger.debug(f"Trained FastSketch on {len(X)} rows.")
        return self

    def _fit_custom(self, features: NDArray[np.floating], n_components: int
                    ) -> Tuple[NDArray, NDArray, NDArray]:
        """
        Implements SVD via a divide-and-conquer approach,
            by sketching smaller blocks, and merging them all together.

        Parameters
        ----------
        features: NDArray[np.floating]
                        of shape (n_samples, n_row_patches, n_col_patches, n_features)
            Features for dataset
        n_components: int
            Number of components in sketch

        Returns
        -------
        svals: NDArray of shape (n_components,)
            Singular values; importance of the dominant directions returned as `basis`
        basis: NDArray of shape (n_components, n_features)
            Orthonormal basis (equivalent of PCA.components_),
                without mean correction or normalization
        projections: NDArray of shape (n_samples, n_row_patches, n_col_patches, n_components_)
            Projections of input features to the dominant directions given by `basis`.
        """
        n_samples, n_row_patches, n_col_patches, n_features = features.shape
        # All dominant direction information will be captured in the sketch.
        # Centering data before SVD pushes some of this information away
        #    from the sketch, and into the mean.
        # When sketching different partitions of the data separately and merging later,
        #   the mean-correction becomes a bit messy to handle. Instead, without
        #   mean-correction, it's always just a matrix multiplication.

        self.mean_ = np.zeros(n_features)
        # Set mean to zero, because we haven't done any mean correction

        if getattr(self, 'skip_rotate', False):
            # Allow the data to pass through without any SVD,
            #   for cases when no dimensionality reduction is requested.
            # This is supported so that the data ingest filters don't have to be removed
            # completely from ingest pipelines that want to preserve the original feature
            # space without any reduction.
            if self.n_components != n_features:
                raise ValueError(
                    "Rotating the basis cannot be skipped when reduction is requested.")

            basis = np.identity(n_features)
            projections = features.copy()
            # svals is a proxy for the energy/importance of a feature dimension.
            svals = np.sum(projections.reshape(-1, n_features) ** 2, axis=0)
        else:
            sketch, projections = block_sparse_project(
                features, n_components=n_components, tol=self.tol,
                frac=self.frac, n_blocks=self.n_blocks, random_state=self.random_state)

            svals, basis = decompose_sketch(sketch)
            assert len(sketch) > 0, "Sketch should not be empty."

        svals, basis, projections = self._update_or_overwrite_sketch(
            features, svals, basis, projections, n_components)
        assert projections.ndim == 4

        # n_samples and n_features(n_features per patch) in the data.
        n_patches = n_samples * n_row_patches * n_col_patches
        self.n_samples_, self.n_features_in_ = n_patches, n_features  # type: ignore
        self.n_samples_seen_ = getattr(self, 'n_samples_seen_', 0) + n_patches

        self.components_ = basis
        self.n_components_ = len(basis)

        # Calculate relevant scores.........
        # But before that, a few basic checks to avoid invalid values.
        # In case n_rows = 1,
        n_patches_minus_1 = max(1., n_patches - 1.)
        # And in case the largest singular value is 0,
        svals[0] = max(svals[0], np.finfo(np.double).tiny)
        #   a tiny tolerance to avoid non-finite values.

        # Variance explained by singular values
        self.explained_variance_ = (svals ** 2) / n_patches_minus_1
        total_var = np.linalg.norm(features.reshape(n_patches, n_features),
                                   ord='fro') ** 2 / n_patches_minus_1
        # It is possible that total_var is 0, for zero input, so,
        total_var = max(total_var, np.finfo(np.double).tiny)
        # This total_var is different from sklearn's,
        #    because we don't center the data.
        self.explained_variance_ratio_ = self.explained_variance_ / total_var  # type: ignore
        self.singular_values_ = svals.copy()

        self.noise_variance_ = (total_var - self.explained_variance_.sum()) / (
                (min(n_patches, n_samples) - n_components) + TINY_VAL)

        # Also create an attribute called 'sketch_'
        self.sketch_ = compose_sketch(svals, basis)

        # reshape the projections back to a 4d tensor.
        assert projections.shape == (n_samples, n_row_patches,
                                     n_col_patches, self.n_components_), (
            "Projections are shaped incorrectly.")

        # This return is different from sklearn's method returns.
        # They return U, S, V
        #   while we're returning S, V, (U@S).
        #   (projections(U@S) are reshaped to a 4d tensor.)
        return svals, basis, projections

    def _update_or_overwrite_sketch(self, features, svals, basis,
                                    projections, n_components):
        """
        Update existing sketch or overwrite as appropriate.
        Projections aren't needed, but are supplied to avoid re-computing.
        Return svals, basis, and projections w.r.t. latest or updated sketch
        """
        fitted_already = len(self.components_) > 0
        if fitted_already and not self.overwrite:
            # For pre-trained models with overwrite set to False,
            #   merge the previous sketch with the current sketch,
            #   and recompute projections
            prev_sketch = self.singular_values_.reshape((-1, 1)) * self.components_
            curr_sketch = compose_sketch(svals, basis)
            svals, basis = merge_sketches([prev_sketch, curr_sketch],
                                          n_components=n_components)
            projections = project_to_basis(features, basis)

        # When overwriting, or when the model wasn't fitted previously,
        #   return the inputs as they are with no changes.
        return svals, basis, projections

    def score_samples(self, X: NDArray[np.floating]) -> float:
        if X.ndim == 2:
            X = X.reshape((X.shape[0], 1, 1, X.shape[1]))

        assert X.ndim == 4, "Input 'X' must be a 4d tensor."

        # reshape input data to 2d array for internal operations.
        # Each patch is considered like an individual sample.
        X = X.reshape((-1, X.shape[-1]))

        logger.debug(
            "score_samples method is defined for centered data, "
            "but we're applying it to uncentered data. "
            "Be careful about how you interpret this.")
        return super().score_samples(X)

    def fit_transform(self,
                      X: NDArray[np.floating], y: None = None
                      ) -> NDArray[np.floating]:
        """
        Create sketch on data and produce ProjectFrame

        Parameters
        ----------
        (Positional)
        X: NDArray[np.floating] of ndim = 2 or 4
            Features for dataset,
            If 2d has shape:
             (n_samples, n_features)
            If 4d has shape:
             (n_samples, n_row_patches, n_col_patches, n_features)

        y: None, default=None
            Dummy variable for consistency

        Returns
        -------
        array_or_pf: NDArray(2d or 4d depending on the input) of
            projections having shape:
            - (n_samples, n_components_), if input was 2d.
            - (n_samples, n_row_patches, n_col_patches, n_components_),
            if input was 4d
        """
        # pylint: disable = arguments-differ
        if X.ndim == 2:
            was_2d = True
            X = X.reshape((X.shape[0], 1, 1, X.shape[1]))
        else:
            was_2d = False

        assert X.ndim == 4, "Input 'X' must be a 4d tensor."

        _, _, projections = self._fit_custom(X, self.n_components)

        logger.debug(f"Trained FastSketch and transformed on {len(X)} rows")

        if was_2d:
            projections = projections.reshape(-1, projections.shape[-1])
        return projections

    def transform(self, X, y=None):
        """
        Compute projections for data using pre-fitted sketch,
            and produce ProjectFrame (or array)

        Parameters
        ----------
        (Positional)
        X: np.ndarray of ndim = 2 or 4
            Features for dataset,
            If 2d has shape:
             (n_samples, n_features)
            If 4d has shape:
             (n_samples, n_row_patches, n_col_patches, n_features)
        y: dummy variable for API consistency
            Not used

        Returns
        -------
        array_or_pf: ProjectFrame or float array
            If self.out_pf is True, returns ProjectFrame.
            Else, returns np.ndarray(2d or 4d depending on the input) of
            projections having shape:
            - (n_samples, n_components_), if input was 2d.
            - (n_samples, n_row_patches, n_col_patches, n_components_),
            if input was 4d
        """
        # pylint: disable = arguments-differ
        # pylint: disable = unused-argument
        # Because y is a dummy variable

        if X.ndim == 2:
            X = X.reshape(X.shape[0], 1, 1, X.shape[1])
            was_2d = True
        else:
            was_2d = False

        assert X.ndim == 4, "Input 'X' must be a 4d tensor."
        # original shape of X
        n_samples, n_row_patches, n_col_patches, n_features = X.shape

        # reshape input data to 2d array for internal operations.
        # Each patch is considered like an individual sample.
        X = X.reshape((-1, n_features))

        projections = project_to_basis(X, self.components_)

        # reshape the projections back to a 4d tensor.
        projections = projections.reshape(
            n_samples, n_row_patches, n_col_patches, projections.shape[-1])
        assert projections.shape == (n_samples, n_row_patches,
                                     n_col_patches, self.n_components_), \
            "Projections are shaped incorrectly."

        if was_2d:
            projections = projections.reshape(-1, projections.shape[-1])
        return projections

    # Sketch is not allowed to be set directly. So no setter for this.
    @property
    def sketch(self):
        """
        Sketch that has been fitted
        """
        return compose_sketch(self.singular_values_, self.components_)

    @property
    def n_features_(self):
        """ Because newer versions of sklearn's PCA do it this way."""
        return self.n_features_in_

    def inverse_transform(self, X):
        """
        Transform projections back to original feature space

        Parameters
        ----------
        X: ProjectFrame or float array
            Projections that need to be transformed to original feature space.
            If projections are np.ndarray, they must have any of the below
            shapes:-
            - (n_samples, n_components_)
            - (n_samples, n_row_patches, n_col_patches, n_components_)

        Returns
        ---------
        reconstruction: np.ndarray(2d or 4d depending on the input)
            Points in original feature space having shape:
            - (n_samples, n_features), if input was 2d np.ndarray.
            - (n_samples, n_row_patches, n_col_patches, n_features),
            if input was 4d np.ndarray or ProjectFrame.
        """
        if X.ndim == 2:
            X = X.reshape(X.shape[0], 1, 1, X.shape[1])
            was_2d = True
        else:
            was_2d = False

        if not X.shape[-1] == self.n_components_:
            raise ValueError

        projections = X

        # original shape of the projections
        n_samples, n_row_patches, n_col_patches, _ = projections.shape

        # reconstruct projections back to original feature space
        reconstructions = reconstruct_from_basis(projections, self.components_)
        assert reconstructions.shape == (n_samples, n_row_patches,
                                         n_col_patches, self.n_features_), \
            "Reconstructions are shaped incorrectly."

        if was_2d:
            reconstructions = reconstructions.reshape(
                -1, reconstructions.shape[-1])
        return reconstructions


if __name__ == "__main__":
    import doctest
    import os

    print(f"Running doctests for {os.path.basename(__file__)}...")
    doctest.testmod()
