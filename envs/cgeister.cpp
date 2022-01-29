#include <array>
#include <string>
#include <sstream>
#include "cboard.hpp"
#include "cgeister.hpp"


namespace py = pybind11;
using namespace std;


CGeister::CGeister()
   :nextPlayer(0),
    board{InitState},
    turn(0),
    winner(-1),
    done(false) {}


py::array_t<float> CGeister::reset(const array<int, 4> red0, const array<int, 4> red1) {
   nextPlayer = turn = 0;
   winner = -1;
   done = false;

   string state{InitState};
   for (int i=0; i<4; i++) {
      state[red0[i] * 3 + 2] = 'R';
      state[red1[i] * 3 + 26] = 'R';
   }
   board = CBoard(state);

   return board.observe();
}


py::array_t<float> CGeister::update(const string& state) {
   nextPlayer = turn = 0;
   winner = -1;
   done = false;
   board = CBoard(state);
   return board.observe();
}


py::array_t<float> CGeister::step(const int action, bool swap) {
   turn++;
   board.moveUnit(action);

   if (board.gameOver()) {
      winner = nextPlayer ^ board.winner;
      done = true;
   }

   if (swap) changeSide();

   return board.observe();
}


string CGeister::render() const {
   auto obsv = board.observe();

   stringstream ss;
   ss << "Turn: " << turn << " Done: " << done << " Winner: " << winner << endl;

   ss << "Board: \n";
   for (int h = 0; h < CBoard::ObservationShape[1]; h++) {
      for (int p = 0; p < 3; p++) {
         for (int w = 0; w < CBoard::ObservationShape[2]; w++) {
            ss << *obsv.data(p, h, w);
         }
         ss << " ";
      }
      ss << endl;
   }

   ss << "Taken: R B r b\n       ";
   const auto& cnt = board.getTakenCnt();
   for (const auto& p: cnt)
      for (const auto& n: p)
         ss << n << " ";
   ss << endl;
   return ss.str();
}

