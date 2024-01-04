#include <pybind11/pybind11.h>

#include "cmeel/example/adder.hpp"
#include "cmeel/example/config.hh"

PYBIND11_MODULE(cmeel_example, m) {
  m.attr("__version__") = CMEEL_EXAMPLE_VERSION;
  m.def("cmeel_add", &cmeel::example::add);
  m.def("cmeel_sub", &cmeel::example::sub);
}
