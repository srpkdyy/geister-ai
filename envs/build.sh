c++ -O3 -Wall -shared -std=c++17 -fPIC `python -m pybind11 --includes` cboard.cpp cgeister.cpp cbuild.cpp -o cgeister.so

