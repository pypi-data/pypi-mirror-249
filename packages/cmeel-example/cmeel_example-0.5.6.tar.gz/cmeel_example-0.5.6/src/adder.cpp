#include "cmeel/example/adder.hpp"

namespace cmeel {
namespace example {
auto add(const long a, const long b) -> long { return a + b; }

auto sub(const long a, const long b) -> long { return a - b; }
}  // namespace example
}  // namespace cmeel
