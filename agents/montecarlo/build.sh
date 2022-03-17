c++ -O3 -Wall -shared -std=c++17 -fPIC `python -m pybind11 --includes` ../../envs/cboard.cpp mcts.cc build.cc -o mcts.so -I../../envs

