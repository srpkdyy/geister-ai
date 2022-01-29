import torch


def get_policy_value(observe, model, device):
    with torch.no_grad():
        s = torch.Tensor(observe)
        s = s.unsqueeze(0).to(device)

        policy, value = model.forward(s)
        policy = policy.cpu().detach().clone().numpy()
        value = value.cpu().detach().clone().numpy()
    return policy, value


def get_legal_policy_value(observe, model, legal_act, device):
    p, v = get_policy_value(observe, model, device)
    legal_p = p[legal_act]
    return legal_p

