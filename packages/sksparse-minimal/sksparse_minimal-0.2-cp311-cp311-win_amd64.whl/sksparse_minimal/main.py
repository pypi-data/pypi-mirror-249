import numpy as np
from scipy import sparse
from sksparse_minimal._cholespy_core import CholeskySolver

CHOLMOD_A = 0
CHOLMOD_LDLt = 1
CHOLMOD_LD = 2
CHOLMOD_DLt = 3
CHOLMOD_L = 4
CHOLMOD_Lt = 5
CHOLMOD_D = 6
CHOLMOD_P = 7
CHOLMOD_Pt = 8


class SparseCholesky:
    def __init__(self, A):
        if not sparse.isspmatrix_csc(A):
            raise ValueError("Expected CSC matrix")

        self._shape = A.shape[0]

        self._solver = CholeskySolver(self._shape, A.indptr, A.indices, A.data)

    def _solve(self, b, method):
        res = np.zeros_like(b, dtype=np.float64)
        self._solver.solve(b.astype(np.float64), res, method)
        return res

    def _ensure_L_or_LD_inplace(self, want_L):
        want_super = self._solver.is_super() and want_L
        self._solver.change_factor(want_L, want_super)
        if not bool(self._solver.is_ll()) == want_L:
            raise ValueError("Could not change factorization")

    def solve_A(self, b):
        return self._solve(b, CHOLMOD_A)

    def solve_D(self, b):
        return self._solve(b, CHOLMOD_D)

    def solve_DLt(self, b):
        self._ensure_L_or_LD_inplace(False)
        return self._solve(b, CHOLMOD_DLt)

    def solve_L(self, b, use_LDLt_decomposition=True):
        self._ensure_L_or_LD_inplace(not use_LDLt_decomposition)
        return self._solve(b, CHOLMOD_L)

    def solve_LD(self, b):
        self._ensure_L_or_LD_inplace(False)
        return self._solve(b, CHOLMOD_LD)

    def solve_LDLt(self, b):
        return self._solve(b, CHOLMOD_LDLt)

    def solve_Lt(self, b, use_LDLt_decomposition=True):
        self._ensure_L_or_LD_inplace(not use_LDLt_decomposition)
        return self._solve(b, CHOLMOD_Lt)

    def apply_P(self, b):
        return self._solve(b, CHOLMOD_P)

    def apply_Pt(self, b):
        return self._solve(b, CHOLMOD_Pt)

    def P(self):
        return self.apply_P(np.arange(self._shape))
