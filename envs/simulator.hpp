#include <vector>
#include <string>
#include "cgeister.hpp"


class Simulator {
private:
   const std::vector<std::string> possibleStates;

public:
   Simulator(const std::string& state, const int move);
   int playout(const int plays);
};

