from ..utils.code_utils import deprecate_class
from .base import (
    BaseRegularization,
    WeightedLeastSquares,
    BaseSimilarityMeasure,
    Smallness,
    SmoothnessFirstOrder,
    SmoothnessSecondOrder,
)
from .regularization_mesh import RegularizationMesh
from .sparse import BaseSparse, SparseSmallness, SparseSmoothnessFirstOrder, Sparse
from .pgi import PGIsmallness, PGI
from .cross_gradient import CrossGradient
from .correspondence import LinearCorrespondence
from .jtv import JointTotalVariation
from .vector_amplitude import VectorAmplitude


@deprecate_class(removal_version="0.x.0", future_warn=True)
class SimpleSmallness(Smallness):
    """Deprecated class, replaced by Small."""

    def __init__(self, mesh=None, **kwargs):
        super().__init__(mesh=mesh, **kwargs)


@deprecate_class(removal_version="0.x.0", future_warn=True)
class SimpleSmoothnessFirstOrder(SmoothnessFirstOrder):
    """Deprecated class, replaced by SmoothDeriv."""

    def __init__(self, mesh=None, **kwargs):
        super().__init__(mesh=mesh, **kwargs)


@deprecate_class(removal_version="0.x.0", future_warn=True)
class Simple(WeightedLeastSquares):
    """Deprecated class, replaced by WeightedLeastSquares."""

    def __init__(self, mesh=None, alpha_x=1.0, alpha_y=1.0, alpha_z=1.0, **kwargs):
        # These alphas are now refered to as length_scalse in the
        # new WeightedLeastSquares regularization
        super().__init__(
            mesh=mesh,
            length_scale_x=alpha_x,
            length_scale_y=alpha_y,
            length_scale_z=alpha_z,
            **kwargs
        )


@deprecate_class(removal_version="0.x.0", future_warn=True)
class Tikhonov(WeightedLeastSquares):
    """Deprecated class, replaced by WeightedLeastSquares."""

    def __init__(
        self, mesh=None, alpha_s=1e-6, alpha_x=1.0, alpha_y=1.0, alpha_z=1.0, **kwargs
    ):
        super().__init__(
            mesh=mesh,
            alpha_s=alpha_s,
            alpha_x=alpha_x,
            alpha_y=alpha_y,
            alpha_z=alpha_z,
            **kwargs
        )


@deprecate_class(removal_version="0.x.0", future_warn=True)
class PGIwithNonlinearRelationshipsSmallness(PGIsmallness):
    """Deprecated class, replaced by PGIsmallness."""

    def __init__(self, gmm, **kwargs):
        super().__init__(gmm, non_linear_relationships=True, **kwargs)


@deprecate_class(removal_version="0.x.0", future_warn=True)
class PGIwithRelationships(PGI):
    """Deprecated class, replaced by PGI."""

    def __init__(self, mesh, gmmref, **kwargs):
        super().__init__(mesh, gmmref, non_linear_relationships=True, **kwargs)
