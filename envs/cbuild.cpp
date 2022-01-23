#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "cgeister.hpp"


namespace py = pybind11;


PYBIND11_MODULE(cgeister, m) {
   py::class_<CGeister>(m, "cGeister")
      .def(py::init())
      .def("reset", &CGeister::reset)
      .def("update", &CGeister::update)
      .def("step", &CGeister::step)
      .def("render", &CGeister::render)
      .def("get_legal_actions", &CGeister::getLegalActions)
      .def("make_state", &CGeister::makeState)
      .def_readwrite("turn", &CGeister::turn)
      .def_readwrite("winner", &CGeister::winner)
      .def_readwrite("done", &CGeister::done);
}

