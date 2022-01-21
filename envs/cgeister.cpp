#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace std;

constexpr BOARD_SIZE = 6;

struct Unit {
   int x, y;
   char color;
}


class CGeister {
private:
   array<
public:

}



PYBIND11_MODULE(cgeister, m) {
}

