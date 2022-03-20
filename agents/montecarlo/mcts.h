#include <string>
#include <random>
#include <vector>
#include <map>
#include <chrono>


struct Node {
   int n;
   float w;
   std::string state;
   Node* const parent;
   std::vector<int> untriedActions;
   std::map<int, std::shared_ptr<Node>> children;
};


class MCTS {
public:
   MCTS(const int);
   std::vector<int> evaluate(const std::string&, const std::vector<int>&);

private:
   std::mt19937 mt;
   const std::chrono::milliseconds allowedCalcMs;
   const int maxTurn;
   int playout(const std::string&);
};

