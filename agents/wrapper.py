from .base_agent import BaseAgent


class AgentWrapper:
    def __init__(self, arch, params, use_info):
        self.agent = arch(**params)
        self.use_info = use_info

    def init_red(self):
        return self.agent.init_red()

    def get_action(self, obsv, state, legal_act):
        args = []

        if 'obsv' in self.use_info:
            args.append(obsv)
        if 'state' in self.use_info:
            args.append(state)
        if 'legal_act' in self.use_info:
            args.append(legal_act)

        return self.agent.get_action(*args)

