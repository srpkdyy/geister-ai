#include <array>
#include <string>
#include <sstream>
#include "cboard.hpp"




class CGeister {
private:
   static constexpr int ActionNum = 144;
   static constexpr char InitState[] = "14B24B34B44B15B25B35B45B41B31B21B11B40B30B20B10B";

   const bool openInfo;
   int nextPlayer;
   CBoard board;

public:
   int turn;
   int winner;
   bool done;

   CGeister(const bool open);

   pybind11::array_t<float> reset(const std::array<int, 4>, const std::array<int, 4>);
   pybind11::array_t<float> update(const std::string&);
   pybind11::array_t<float> step(const int, const bool);
   std::string render() const;
   
   inline void changeSide() {
      nextPlayer ^= 1;
      board.swap();
   }

   inline pybind11::array_t<float> observe() const {
      return board.observe();
   }

   inline auto getLegalActions() const {
      return board.getLegalActions();
   }

   inline auto makeState(const bool usePurple) const {
      return board.makeState(usePurple);
   }
};

