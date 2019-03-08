# Using PyTorch to automatically calculate gradient
import numpy as np 
import torch


def LiveMatrix(t, shape=(3, 3), x=None):
    '''
    Generate a time varianted matrix W with specific defination. This version use pytorch to define a time-varianted matrix
    which can automatically calculate his gradient with time. The W_tensor below is an example show you how to define your 
    specific matrix .

    Input
    t: time step
    shape: the shape of your defined matrix
    x: ???

    Return
    W: the time-varied matrix at timestep t
    W_grad: the gradient of the time-varied matrix at timestep t
    t: current timestep
    '''
    t_tensor = torch.tensor([[t] * shape[1]] * shape[0], dtype=torch.float, requires_grad=True)
    W_tensor = [None] * (shape[0] * shape[1])

    #-------Edit your matrix here-------#
    W_tensor[0] = torch.sin(2 * t_tensor[0, 0]) + 2
    W_tensor[1] = torch.cos(2 * t_tensor[0, 1])
    W_tensor[2] = torch.sin(4 * t_tensor[0, 2])
    W_tensor[3] = torch.cos(2 * t_tensor[1, 0])
    W_tensor[4] = torch.sin(2 * t_tensor[1, 1]) + 2
    W_tensor[5] = torch.cos(4 * t_tensor[1, 2])
    W_tensor[6] = torch.sin(4 * t_tensor[2, 0])
    W_tensor[7] = torch.cos(4 * t_tensor[2, 1])
    W_tensor[8] = torch.zeros(1) * t_tensor[2, 2]
    #-----------------------------------#

    W_tensor = torch.cat([i.reshape(-1, 1) for i in W_tensor]).view(*shape)
    W = W_tensor.detach().numpy()
    J = torch.sum(W_tensor)
    J.backward()
    W_grad = t_tensor.grad.data.detach().numpy()
    
    return (W, W_grad, t)


def LiveMatrix2(t, x=None):
    '''
    Generate a time varianted matrix W with specific defination. This version use pytorch to define a time-varianted matrix
    which can automatically calculate his gradient with time.  

    Input
    t: time step
    x: ???

    Return
    output: Tensor
    '''
    t_tensor = torch.tensor(t, dtype=torch.float, requires_grad=True)

    #-------Edit your matrix here-------#
    W_tensor = [[torch.sin(2*t_tensor) + 2, torch.cos(2*t_tensor), torch.sin(4*t_tensor)], 
        [torch.cos(2*t_tensor), torch.sin(2*t_tensor) + 2, torch.cos(4*t_tensor)], 
        [torch.sin(4*t_tensor), torch.cos(4*t_tensor), torch.zeros(1)]]
    #-----------------------------------#

    W = torch.tensor(W_tensor).detach().numpy()
    return (W, W_tensor, t_tensor)


def calculate_grad(W_tensor, t_tensor):
    row = len(W_tensor)
    col = len(W_tensor[row - 1])
    W_grad = np.zeros((row, col))

    for i in range(row):
        for j in range(col):
            if t_tensor.grad is not None:
                t_tensor.grad.data.zero_()
            if W_tensor[i][j].requires_grad:
                W_tensor[i][j].backward()
            gradient = t_tensor.grad.data.item()
            W_grad[i, j] = gradient            
    
    return W_grad


if __name__ == "__main__":
    def test():
        # recomended using method
        W, W_gradient, t = LiveMatrix(t=2)
        print('t:', t, 'W:', W, 'W_gradient:', W_gradient, sep='\n')

        # another method when you want to better control
        W, W_tensor, t_tensor = LiveMatrix2(t=2)
        W_gradient = calculate_grad(W_tensor, t_tensor)
        print('t:', t_tensor.item(), 'W:', W, 'W_gradient:', W_gradient, sep='\n')
    
    test()