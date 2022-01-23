#include <array>
#include <string>
#include <sstream>
#include "cboard.hpp"




class CGeister {
private:
   static constexpr int ActionNum = 144;
   static constexpr char InitState[] = "14B24B34B44B15B25B35B45B41B31B21B11B40B30B20B10B";

   int nextPlayer;
   CBoard board;

   inline void changeSide() {
      nextPlayer ^= 1;
      board.swap();
   }

public:
   int turn;
   int winner;
   bool done;

   CGeister();

   pybind11::array_t<float> reset(const std::array<int, 4> red0, const std::array<int, 4> red1);
   pybind11::array_t<float> update(const std::string& state);
   pybind11::array_t<float> step(const int action);
   std::string render() const;
   inline auto getLegalActions() const {
      return board.getLegalActions();
   }
};

