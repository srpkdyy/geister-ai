#include <string>
#include <random>
#include <vector>
#include <chrono>


struct Node {
   int n;
   int w;
   const std::string& state;
   const Node& parent;
   std::vector<shared_ptr<Node>> children;
};


class MCTS {
public:
   MCTS(const int);
   std::vector<int> evaluate(std::string);

private:
   std::mt19937 mt;
   const std::chrono::milliseconds allowedCalcMs;
   const int maxTurn;
   int search(const std::string&);
   int playout(const std::string&);
};

