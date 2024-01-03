const char *doc_constructor= R"(
Precompute a sparse Cholesky factor for the given input sparse matrix in CSC format.

Parameters
----------

- n_rows - The number of rows in the (sparse) matrix.
- ii - The first array of indices in the sparse matrix representation.
       The array of column (resp. row) indices, such that row
       (resp. column) indices for column (resp. row) k are stored in
       jj[ii[k]:ii[k+1]] and the corresponding entries are in x[ii[k]:ii[k+1]].
- jj - The second array of indices in the sparse matrix representation.
       The array of row (resp. column) indices.
- x - The array of nonzero entries.
)";

const char *doc_cholesky_d =
    "Double-precision solver implementation";

const char *doc_solve = R"(

Solve the linear system for a given set of right-hand sides.

Parameters
----------

- `b` - Right-hand side of the equation to solve. Can be a vector or a matrix.
        If it is a matrix, it must be of shape `(n_rows, n_rhs)`. It must be on the
        same device as the tensors passed to the solver constructor.
- `x` - Placeholder for the solution. It must be on the same device and have the
          same shape as `b`.
)";


const char *doc_is_ll = R"(
Returns 1 if the factorization is LL, 0 if it is LDL.
)";

const char *doc_is_super = R"(
Returns 1 if the factorization is supernodal, 0 if it is simplicial.
)";

const char *doc_is_monotonic = R"(
Returns 1 if the factorization is monotonic, 0 if it is not.
)";

const char *doc_change_factor = R"(
Change the type of the factorization. These are the valid combinations:

simplicial LDL':  (is_ll 0, is_super 0).  Stored in compressed
     column form, using the simplicial components above (nzmax, p, i,
     x, z, nz, next, and prev).  The unit diagonal of L is not stored,
     and D is stored in its place.  There are no supernodes.

simplicial LL': (is_ll 1, is_super 0).  Uses the same storage
     scheme as the simplicial LDL', except that D does not appear.
     The first entry of each column of L is the diagonal entry of
     that column of L.

supernodal LL': (is_ll 1, is_super 1).  A supernodal factor,
     using the supernodal components described above (nsuper, ssize,
     xsize, maxcsize, maxesize, super, pi, px, s, x, and z).
     A supernodal factorization is never zomplex.

- `to_ll` - If 1, the factorization will be LL, if 0 it will be LDL.
- `to_super` - If 1, the factorization will be supernodal, if 0 it will be simplicial.
)";