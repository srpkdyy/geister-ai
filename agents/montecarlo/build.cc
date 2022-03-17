#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "mcts.h"


namespace py = pybind11;
using namespace py::literals;


PYBIND11_MODULE(mcts, m) {
   py::class_<MCTS>(m, "MCTS")
      .def(py::init<const float>(), "calc_ms"_a=1000)
      .def("evaluate", &MCTS::evaluate);
}

