#ifndef _CBOARD_H_
#define _CBOARD_H_


#include <string>
#include <vector>
#include <array>


using Plane = std::array<std::array<float, CBoard::Width>, CBoard::Width>;

enum Color {
  Red,
  Blue,
  ColorNum
};


struct Unit {
  int x, y;
  Color c;
};


class CBoard {
public:
  int winner;

  CBoard(std::string);
  ~CBoard() {}

  std::array<Plane, 19> getState() const;
  std::vector<int> getLegalActions() const;
  void moveUnit(const int);
  void swap();
  bool gameOver() const;


private:
  static constexpr int PlayerNum = 2;
  static constexpr int UnitNum = 8;
  static constexpr int AllUnitNum = PlayerNum * UnitNum;
  static constexpr int Width = 6;
  static constexpr int DirectionNum = 4;
  static constexpr array<int, DirectionNum> dx = {0, -1, 1, 0}, dy = {-1, 0, 0, 1};

  std::array<std::array<Unit, UnitNum>, PlayerNum> units;
  std::array<std::array<int, ColorNum>, PlayerNum> takenCnt;

  inline bool onBoard(const int x, const int y) const {
    return 0 <= x && x < Width && 0 <= y && y < Width;
  }

  inline Unit& find(const int x, const int y, const int player) const {
    for (const Unit& u: units[player]) {
      if (x == u.x && y == u.y) return u;
    }
    return nullptr;
  }
}


#endif //_CBOARD_H_

