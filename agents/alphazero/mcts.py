from ...envs.cgeister import cGeister


class Node:
    def __init__(self, state, p, predict):
        self.state = state
        self.p = p
        self.w = 0
        self.n = 0
        self.children = None

        self.predict = predict


    def evaluate(self):
        env = cGeister().update(self.state)

        if env.done:
            value = 1 if env.winner == 0 else -1

            self.w += value
            self.n += 1
            return value

        if not self.children:
            p, v = self.predict(





class MCTS:
    def __init__(self, env_state, model, evaluates):
        self.root = env_state
        self.model = model
        self.evaluates = evaluates


    def predict(observe, legal_act):
        with torch.no_grad():
            s = torch.Tensor(observe)
            s = s.unsqueeze(0).to(self.device)

            policy, value = self.model.forward(s)
            policy = policy.cpu().detach().clone().numpy()
            value = value.cpu().detach().clone().numpy()

        policy = policy[legal_act]
        policy /= policy.sum() if policy.sum() else 1
        return policy, value


    def nodes_to_scores(nodes):
        return [c.n for c in nodes]


    def evaluate(self):
        if 
        

        


