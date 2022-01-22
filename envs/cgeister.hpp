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
   using Observation = std::array<CBoard::Plane, 19>;

   int turn;
   int winner;
   bool done;

   CGeister();

   Observation reset(const std::array<int, 4> red0, const std::array<int, 4> red1);
   Observation update(const std::string& state);
   Observation step(const int action);
   std::string render() const;
   inline auto getLegalActions() const {
      return board.getLegalActions();
   }
};

