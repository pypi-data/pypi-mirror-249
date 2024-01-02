// Copyright 2023 Ryan Moore
//
// If the implementation is easy to explain, it may be a good idea.
//
// Tim Peters

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <sstream>

#include "tensor.hpp"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

PYBIND11_MODULE(tensor, m) {
  m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: cudagrad

        .. autosummary::
           :toctree: _generate

        hello
        tensor
        Tensor
    )pbdoc";

  #ifdef __CUDACC__
  m.def("hello", &cg::hello, R"pbdoc(
        Can has CUDA?

        Hello!
    )pbdoc");
  #endif
  
  py::class_<cg::DataProxy>(m, "_DataProxy")
      .def("__getitem__", &cg::DataProxy::get)
      .def("__setitem__", &cg::DataProxy::set);

  py::class_<cg::GradProxy>(m, "_GradProxy")
      .def("__getitem__", &cg::GradProxy::get)
      .def("__setitem__", &cg::GradProxy::set);

  // TODO(yrmo): When doing C++ bindings does repr
  //              override str when no str present?
  py::class_<cg::Tensor, std::shared_ptr<cg::Tensor>>(m, "Tensor")
      .def(py::init<std::vector<int>, std::vector<float>>())
      .def("get_shared", &cg::Tensor::get_shared)
      .def("backward", &cg::Tensor::backward)
      .def("zero_grad", &cg::Tensor::zero_grad)
      .def("sum", &cg::Tensor::sum)
      .def("relu", &cg::Tensor::relu)
      .def("sigmoid", &cg::Tensor::sigmoid)
      .def_property_readonly("data", &cg::Tensor::data_proxy)
      .def_property_readonly("grad", &cg::Tensor::grad_proxy)
      // .def("__getitem__", &cg::Tensor::select)
      // .def("__setitem__", &cg::Tensor::put)
      .def("item", &cg::Tensor::item)
      .def_property_readonly("size",
                             &cg::Tensor::get_size)  // do something about this
      .def("graph", &cg::Tensor::graph)
      .def_static("ones", &cg::Tensor::ones)
      .def_static("zeros", &cg::Tensor::zeros)
      .def_static("explode", &cg::Tensor::explode)
      .def_static("rand", &cg::Tensor::rand)
      .def("__add__", [](std::shared_ptr<cg::Tensor> a,
                         std::shared_ptr<cg::Tensor> b) { return a + b; })
      .def("__sub__", [](std::shared_ptr<cg::Tensor> a,
                         std::shared_ptr<cg::Tensor> b) { return a - b; })
      .def("__mul__", [](std::shared_ptr<cg::Tensor> a,
                         std::shared_ptr<cg::Tensor> b) { return a * b; })
      .def("__truediv__", [](std::shared_ptr<cg::Tensor> a,
                             std::shared_ptr<cg::Tensor> b) { return a / b; })
      .def("__matmul__",
           [](std::shared_ptr<cg::Tensor> a, std::shared_ptr<cg::Tensor> b) {
             return a.get()->matmul(b);
           })
      .def("__str__",
           [](std::shared_ptr<cg::Tensor> t) {
             std::ostringstream os;
             os << t;
             return os.str();
           })
      .def("__repr__",
           [](std::shared_ptr<cg::Tensor> t) { return t.get()->repr(); })
      .attr("__module__") = "cudagrad";

#ifdef VERSION_INFO
  m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
  m.attr("__version__") = "dev";
#endif
}
