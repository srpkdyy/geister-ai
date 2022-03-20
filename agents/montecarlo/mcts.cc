#include <string>
#include <limits>
#include <random>
#include <vector>
#include <memory>
#include "cboard.hpp"
#include "mcts.h"


using namespace std;
using namespace std::chrono;


MCTS::MCTS(const int calc_ms)
   :mt{random_device{}()},
   allowedCalcMs{calc_ms},
   maxTurn(200){}


vector<int> MCTS::evaluate(const string& state, const vector<int>& legalActions) {
   auto root = unique_ptr<Node>(
       new Node{100, 0, state, nullptr, {}, {}}
       );
   auto start = system_clock::now();

   while (system_clock::now() - start < allowedCalcMs) {
      auto node = root.get();
      
      while (node->untriedActions.empty() && !node->children.empty()) {
         Node* selected = nullptr; 
         double best = -10000000.0;
         auto t = 0;
         for (const auto& mc : node->children) t += mc.second->n;
         for (const auto& mc : node->children) {
            const auto& c = mc.second;
            auto score = -1*(c->w/c->n) + 2*sqrt(2*log(t)/c->n);
            if (score > best) {
               best = score;
               selected = c.get();
            }
         }
         node = selected;
      }

      if (node->children.empty() && node->n >= 100) {
         auto now = CBoard(node->state, false);
         if (!now.gameOver()) {
            auto actions = now.getLegalActions();
            node->untriedActions = actions;
            for (const auto& act : actions) {
               auto next = now;
               next.moveUnit(act); next.swap();
               node->children.emplace( 
                  act, new Node{0, 0, next.makeState(false), node, {}, {}}
                  );
            }
         }
      }

      if (!node->untriedActions.empty()) {
         auto act = node->untriedActions[mt() % node->untriedActions.size()];
         auto itr = node->untriedActions.begin();
         for(; itr != node->untriedActions.end() && *itr != act; itr++);
         iter_swap(itr, node->untriedActions.end() - 1);
         node->untriedActions.resize(node->untriedActions.size() - 1);
         node = node->children[act].get();
      }

      auto result = playout(node->state);

      while (node != nullptr) {
         node->n++; node->w += result;
         result = -result;
         node = node->parent;
      }
   }

   vector<int> scores{};
   for (const auto& a : legalActions) {
      scores.push_back(root.get()->children[a].get()->n);
   }
   return scores;
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

