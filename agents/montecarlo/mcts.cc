#include <string>
#include <limits>
#include <random>
#include <vector>
#include "cboard.hpp"
#include "mcts.h"


using namespace std;


MCTS::MCTS(const float calc_ms)
   :mt{random_device{}()},
   allowedCalcMs(calc_ms),
   maxTurn(200){}


vector<int> MCTS::evaluate(string state) {
   auto root = CBoard(state, false);
   auto legalActions = root.getLegalActions();
   auto n = legalActions.size();

   vector<int> scores(n);

   for (size_t i = 0; i < n; i++) {
      auto next = root;
      next.moveUnit(legalActions[i]);
      next.swap();
      auto nextState = next.makeState(false);

      for (int j = 0; j < 1000; j++) {
         scores[i] += -playout(nextState);
      }
   }
   return scores;
}


int MCTS::search(const string& state) {
   return 0;
}


int MCTS::playout(const string& state) {
   int nextPlayer = 0;
   auto board = CBoard(state, false);

   for (int i = 0; i < maxTurn; i++) {
      if (board.gameOver()) {
         int winner = nextPlayer ^ board.winner;
         return (winner == 0)? 1 : -1;
      }

      auto legalActions = board.getLegalActions();
      int act = legalActions[mt() % legalActions.size()];

      board.moveUnit(act);

      board.swap();
      nextPlayer ^= 1;
   }
   return 0;
}

