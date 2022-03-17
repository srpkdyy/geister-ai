#include <string>
#include <random>
#include <vector>


struct Node {
   int n;
   int w;
   std::string state;
   std::vector<std::shared_ptr<Node*>> children;
};


class MCTS {
public:
   MCTS(const float);
   std::vector<int> evaluate(std::string);

private:
   std::mt19937 mt;
   const float allowedCalcMs;
   const int maxTurn;
   int search(const std::string&);
   int playout(const std::string&);
};

