#include "cholesky_solver.h"
#include "docstr.h"
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace nb = nanobind;

template <typename Float>
void declare_cholesky(nb::module_ &m, const char *docstr) {
    using Class = CholeskySolver<Float>;
    std::string class_name = std::string("CholeskySolver");
    nb::class_<Class>(m, class_name.c_str(), docstr)
        .def("__init__", [](Class *self,
                            uint32_t n_rows,
                            nb::ndarray<int32_t, nb::shape<nb::any>, nb::c_contig> ii,
                            nb::ndarray<int32_t, nb::shape<nb::any>, nb::c_contig> jj,
                            nb::ndarray<double, nb::shape<nb::any>, nb::c_contig> x) {
            if (jj.shape(0) != x.shape(0))
                throw std::invalid_argument("Sparse CSC matrix: the row index and data arrays should have the same size.");
            if (ii.shape(0) != n_rows+1)
                throw std::invalid_argument("Sparse CSC matrix: Invalid size for column pointer array.");

            if (ii.device_type() != jj.device_type() || ii.device_type() != x.device_type())
                throw std::invalid_argument("All input tensors should be on the same device!");

            if (ii.device_type() == nb::device::cpu::value) {
                new (self) Class(n_rows, x.shape(0), (int *) ii.data(), (int *) jj.data(), (double *) x.data());
            } else
                throw std::invalid_argument("Unsupported input device! Only CPU supported.");
        },
        nb::arg("n_rows"),
        nb::arg("ii"),
        nb::arg("jj"),
        nb::arg("x"),
        doc_constructor)
        .def("solve", [](Class &self,
                        nb::ndarray<Float, nb::c_contig> b,
                        nb::ndarray<Float, nb::c_contig> x,
                        int mode){
            if (b.ndim() != 1 && b.ndim() != 2)
                throw std::invalid_argument("Expected 1D or 2D tensors as input.");
            if (b.shape(0) != x.shape(0) || (b.ndim() == 2 && b.shape(1) != x.shape(1)))
                throw std::invalid_argument("x and b should have the same dimensions.");
            if (b.device_type() != x.device_type())
                throw std::invalid_argument("x and b should be on the same device.");

            if (mode < 0 || mode > 8)
                throw std::invalid_argument("Invalid mode.");
            // CPU solve
            if (b.device_type() == nb::device::cpu::value) {
                self.solve_cpu(b.ndim()==2 ? b.shape(1) : 1, (Float *) b.data(), (Float *) x.data(), mode);
            } else
                throw std::invalid_argument("Unsupported input device! Only CPU supported.");
        },
        nb::arg("b").noconvert(),
        nb::arg("x").noconvert(),
        nb::arg("mode") = 0,
        doc_solve)
        .def("is_ll", &Class::is_ll, doc_is_ll)
        .def("is_super", &Class::is_super, doc_is_super)
        .def("is_monotonic", &Class::is_monotonic, doc_is_monotonic)
        .def("change_factor", [](Class &self, int to_ll, int to_super) {
            self.change_factor(to_ll, to_super);
        },
        nb::arg("to_ll"),
        nb::arg("to_super"),
        doc_change_factor)
        ;
}

NB_MODULE(_cholespy_core, m) {
    declare_cholesky<double>(m, doc_cholesky_d);
}
