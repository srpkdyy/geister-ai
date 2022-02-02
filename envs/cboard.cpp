#include <string>
#include <vector>
#include <array>
#include <sstream>
#include <pybind11/numpy.h>
#include "cboard.hpp"


namespace py = pybind11;
using namespace std;


CBoard::CBoard(const string& state) : takenCnt{}, winner{-1} {

   for (int p = 0; p < PlayerNum; p++) {
      for (int i = 0; i < CBoard::UnitNum; i++) {
         int idx = (p*UnitNum + i) * 3;

         Unit u;

         u.x = int(state[idx] - '0');
         u.y = int(state[idx+1] - '0');

         char c = state[idx+2];
         if (c == 'R' || c == 'r') u.c = Red;
         else if (c == 'B' || c == 'B') u.c = Blue;
         else u.c = Purple;

         units[p][i] = u;

         if (u.x == Grave) takenCnt[p][u.c]++;
      }
   }
}


py::array_t<float> CBoard::observe() const {
   py::array_t<float> obsv{ObservationShape};

   auto begin = obsv.mutable_data(0, 0, 0);
   fill(begin, begin + ObservationSize, 0.0f);

   // Board
   for (int p = 0; p < PlayerNum; p++) {
      for (const Unit& u: units[p]) {
         if (!onBoard(u.x, u.y)) continue;
         int idx;
         if (p == Enemy) idx = 2;
         else idx = (u.c == Blue)? Blue : Red;
         *obsv.mutable_data(idx, u.y, u.x) = 1.0f;
      }
   }

   // one-hot planes of taken
   for (int p = 0; p < PlayerNum; p++) {
      for (int i = 0; i < ColorNum; i++) {
         int n = takenCnt[p][i];
         if (n == 4) continue;

         int idx = p*8 + i*4 + n;
         auto begin = obsv.mutable_data(idx + 3, 0, 0);
         fill(begin, begin + ObservationSize/ObservationShape[0], 1.0f);
      }
   }
   return obsv;
}
   

vector<int> CBoard::getLegalActions() const {
   vector<int> legalAct{};

   for (const Unit& u: units[Ally]) {
      if (!onBoard(u.x, u.y)) continue;

      for (int d = 0; d < DirectionNum; d++) {
         int x = u.x + dx[d], y = u.y + dy[d];

         if (onBoard(x, y) && find(x, y, Ally) == -1 ) {
            int pos = u.x + u.y * Width;
            legalAct.push_back(pos*DirectionNum + d);
         }
      }

      // if unit can escape. include Purple
      if (u.y == 0 && (u.x == 0 || u.x == 5) && u.c != Red) {
         legalAct.push_back(u.x * DirectionNum);
      }
   }
   return legalAct;
}


void CBoard::moveUnit(const int action) {
   int pos = action / DirectionNum, dir = action % DirectionNum;
   int x = pos % Width, y = pos / Width;

   Unit& ally = units[Ally][find(x, y, Ally)];
   ally.x += dx[dir], ally.y += dy[dir];

   if (ally.y == -1) {
      ally.x = Escaped, ally.y = Escaped;
      return;
   }

   int e = find(ally.x, ally.y, Enemy);
   if (e != -1) {
      Unit& enemy = units[Enemy][e];
      enemy.x = Grave, enemy.y = Grave;
      // include Purple into red
      Color c = (enemy.c == Blue)? Blue: Red;
      takenCnt[Enemy][c]++;
   }
}


void CBoard::swap() {
   std::swap(units[Ally], units[Enemy]);
   std::swap(takenCnt[Ally], takenCnt[Enemy]);

   for (int p = 0; p < PlayerNum; p++) {
      for (Unit& u: units[p]) {
         if (!onBoard(u.x, u.y)) continue;
         u.x = Width - u.x - 1;
         u.y = Width - u.y - 1;
      }
   }
}


bool CBoard::gameOver() {
   for (int p = 0; p < PlayerNum; p++) {
      for (const Unit& u: units[p]) {
         if (u.x == Escaped) {
            winner = p;
            return true;
         }
      }
      for (int i = 0; i < ColorNum; i++) {
         if (takenCnt[p][i] == UnitNum / 2) {
            winner = p ^ i;
            return true;
         }
      }
   }
   return false;
}


string CBoard::makeState() const {
   stringstream ss;
   for (int p = 0; p < PlayerNum; p++) {
      for (const Unit& u: units[p]) {
         ss << u.x << u.y;
         if (u.c == Red) ss << 'R';
         else if (u.c == Blue) ss << 'B';
         else ss << 'U';
      }
   }
   return ss.str();
}

