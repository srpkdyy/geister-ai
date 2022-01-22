#include <array>
#include <string>
#include <sstream>
#include "cboard.hpp"
#include "cgeister.hpp"


using namespace std;


CGeister::CGeister()
   :nextPlayer(0),
    board{InitState},
    turn(0),
    winner(-1),
    done(false) {}


CGeister::Observation CGeister::reset(const array<int, 4> red0, const array<int, 4> red1) {
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


CGeister::Observation CGeister::update(const string& state) {
   nextPlayer = turn = 0;
   winner = -1;
   done = false;
   board = CBoard(state);
   return board.observe();
}


CGeister::Observation CGeister::step(const int action) {
   turn++;
   board.moveUnit(action);

   if (board.gameOver()) {
      winner = nextPlayer ^ board.winner;
      done = true;
   }
   else {
      changeSide();
   }

   return board.observe();
}


string CGeister::render() const {
   stringstream ss;
   ss << "Turn: " << turn << " Done: " << done << endl;
   ss << board.render() << endl;
   return ss.str();
}

