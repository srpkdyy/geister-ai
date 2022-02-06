#ifndef _CBOARD_H_
#define _CBOARD_H_


#include <string>
#include <vector>
#include <array>
#include <pybind11/numpy.h>


enum Player {
  Ally,
  Enemy,
  PlayerNum
};

enum Color {
  Red,
  Blue,
  ColorNum,
  Purple
};


struct Unit {
  int x, y;
  Color c;
};


class CBoard {
private:
  static constexpr int Width = 6;
  static constexpr int Escaped = 8;
  static constexpr int Grave = 9;
  static constexpr int UnitNum = 8;
  static constexpr int DirectionNum = 4;
  static constexpr std::array<int, DirectionNum> dx{0, -1, 1, 0},
                                                 dy{-1, 0, 0, 1};

  std::array<std::array<Unit, UnitNum>, PlayerNum> units;
  std::array<std::array<int, ColorNum>, PlayerNum> takenCnt;

  inline bool onBoard(const int x, const int y) const {
    return 0 <= x && x < Width && 0 <= y && y < Width;
  }

  inline int find(const int x, const int y, const int player) const {
    for (int i = 0; i < UnitNum; i++) {
      const Unit& u = units[player][i];
      if (x == u.x && y == u.y) return i;
    }
    return -1;
  }

public:
  static constexpr int ObservationSize = 20 * Width * Width;
  static constexpr std::array<int, 3> ObservationShape{20, Width, Width};

  int winner;

  CBoard(const std::string&);
  pybind11::array_t<float> observe() const;
  std::vector<int> getLegalActions() const;
  void moveUnit(const int);
  void swap();
  bool gameOver();
  std::string makeState(const bool usePurple) const;
  
  inline const auto& getTakenCnt() const {
     return takenCnt;
  }
};


#endif //_CBOARD_H_

