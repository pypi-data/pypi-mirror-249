#include <cassert>

#include "cmeel/example/adder.hpp"

auto main() -> int {
  assert(cmeel::example::add(1, 2) == 3);
  assert(cmeel::example::add(5, -1) == 4);
  assert(cmeel::example::add(-3, -1) == -4);
  return 0;
}
