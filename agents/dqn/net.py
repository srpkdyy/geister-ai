import torch
import torch.nn as nn
import torch.nn.functional as F


def conv3x3(inplanes, outplanes, stride=1):
    return nn.Conv2d(inplanes, outplanes, kernel_size=3, stride=stride, padding=1, bias=False)


class ResBlock(nn.Module):
    def __init__(self, inplanes, planes, stride=1):
        super().__init__()
        self.conv1 = conv3x3(inplanes, planes, stride)
        self.bn1 = nn.BatchNorm2d(planes)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = conv3x3(planes, planes)
        self.bn2 = nn.BatchNorm2d(planes)


    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        
        out = self.conv2(out)
        out = self.bn2(out)

        out += identity
        return out


class DQN(nn.Module):
    def __init__(self, n_action=144, layers=6, states=1):
        super().__init__()
        self.planes = 256

        self.conv = conv3x3(19 * states, self.planes)
        self.bn = nn.BatchNorm2d(self.planes)
        self.relu = nn.ReLU(inplace=True)
        self.layer = self._make_layer(ResBlock, self.planes, layers)

        self.conv_v = nn.Conv2d(self.planes, 8, kernel_size=1)
        self.bn_v = nn.BatchNorm2d(8)
        self.relu_v = nn.ReLU(inplace=True)
        self.value = nn.Linear(36*8, n_action)


        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
    

    def _make_layer(self, block, planes, blocks):
        layers = [block(planes, planes) for _ in range(blocks)]
        return nn.Sequential(*layers)


    def forward(self, s):
        out = self.conv(s)
        out = self.bn(out)
        out = self.relu(out)
        out = self.layer(out)

        v = self.conv_v(out)
        v = self.bn_v(v)
        v = self.relu_v(v)
        v = torch.flatten(v, 1)
        value = self.value(v)

        return value


if __name__ == '__main__':
    from torchinfo import summary
    model = DQN()
    summary(
        model,
        input_size=(20, 19, 6, 6),
        col_names=['input_size', 'output_size', 'num_params'])
#    torch.save(model.state_dict(), '../../weights/dqn/head.pth')

