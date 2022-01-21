#include <string>
#include <vector>
#include <array>
#include "cboard.hpp"


using namespace std;


CBoard::CBoard(const string& state) winner(-1) {
   takenCnt = {{0, 0}, {0, 0}}

   for (int p = 0; p < PlayerNum; p++) {
      for (int i = 0; i < CBoard::UnitNum; i++) {
         int idx = P*UnitNum + i*3

         Unit u;
         u.x = int(state[idx] - '0');
         u.y = int(state[idx+1] - '0');
         char c = state[idx+2];
         u.c = (c == 'R' || c == 'r')? Red : Blue;
         units[p][i] = u;

         if (u.x == 9) takenCnt[p][u.c]++;
      }
   }
}


array<Plane, 19> CBoard::getState() {
   array<Plane, 19> state{};

   for (int p = 0; p < PlayerNum; p++) {
      for (const Unit& u: units[p]) {
         if (!onBoard(u.x, u.y)) continue;
         int idx = p < 1 ? u.c : 2;
         state[idx][u.y][u.x] = 1.0f;
      }
   }

   for (int p = 0; p < PlayerNum; p++) {
      for (int i = 0; i < ColorNum; i++) {
         int idx = p*8 + i*4 + takenCnt[p][i] + 3;
         state[idx].fill(1.0f);
      }
   }

   return state
}
   

vector<int> getLegalActions() {
   vector<int> legalAct{};

   for (const Unit& u: units[0]) {
      for (int d = 0; d < DirectionNum; d++) {
         int x = u.x + dx[d], y = u.y + dy[d];

         if (onBoard(x, y) && find(x, y, 0) == nullptr) {
            int pos = u.x + u.y * Width;
            legalAct.push_back(pos*DirectionNum + d);
         }

         if (y == -1 && (x == 0 || x == Width-1) && u.c == Blue) {
            legalAct.push_back(x * DirectionNum);
         }
      }
   }
   return legalAct;
}


void moveUnit(const int action) {
   int pos = action / DirectionNum, dir = action % DirectionNum;
   int x = pos % Width, y = pos / Width;

   auto unit = find(x, y, 0);
   unit.x += dx[dir], unit.y += dx[dir];

   if (unit.y == -1) {
      unit.x = 8, unit.y = 8;
      return;
   }

   if ((enemy = find(unit.x, unit.y, 1)) != nullptr) {
      enemy.x = 9, enemy.y = 9;
      takenCnt[1][enemy.c]++;
   }
}


void swap() {
   swap(units[0], units[1]);
   swap(takenCnt[0], takenCnt[1]);

   for (int p = 0; p < PlayerNum; p++) {
      for (Unit& u: units[p]) {
         u.x = Width - u.x;
         u.y = Width - u.y;
      }
   }
}


bool gameOver() {
   for (int p = 0; p < PlayerNum; p++) {
      for (const Unit& u: units[p]) {
         if (u.x == 8) {
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

