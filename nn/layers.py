# -*- coding: utf-8 -*-
"""
Created on 2018/8/19 15:03

@author: mick.yi

定义网络层
"""
import numpy as np


def fc_forword(z, W, b):
    """
    全连接层的前向传播
    :param z: 当前层的输出
    :param W: 当前层的权重
    :param b: 当前层的偏置
    :return: 下一层的输出
    """
    return np.dot(z, W) + b


def fc_backword(next_dz, W, z):
    """
    全连接层的反向传播
    :param next_dz: 下一层的梯度
    :param W: 当前层的权重
    :param z: 当前层的输出
    :return:
    """
    dz = np.dot(next_dz, W.T)  # 当前层的梯度
    dw = np.dot(z.T, next_dz)  # 当前层权重的梯度
    db = np.sum(next_dz, axis=0)  # 当前层偏置的梯度, N个样本的梯度求和
    return dw, db, dz


def _single_channel_conv(z, K, b=0, padding=(0, 0), strides=(1, 1)):
    """
    当通道卷积操作
    :param z: 卷积层矩阵
    :param K: 卷积核
    :param b: 偏置
    :param padding: padding
    :param strides: 步长
    :return: 卷积结果
    """
    padding_z = np.lib.pad(z, ((padding[0], padding[0]), (padding[1], padding[1])), 'constant', constant_values=0)
    height, width = padding_z.shape
    k1, k2 = K.shape
    assert (height - k1) % strides[0] == 0, '步长不为1时，步长必须刚好能够被整除'
    assert (width - k2) % strides[1] == 0, '步长不为1时，步长必须刚好能够被整除'
    conv_z = np.zeros((1 + (height - k1) // strides[0], 1 + (width - k2) // strides[1]))
    for h in np.arange(height - k1 + 1)[::strides[0]]:
        for w in np.arange(width - k2 + 1)[::strides[1]]:
            conv_z[h // strides[0], w // strides[1]] = np.sum(padding_z[h:h + k1, w:w + k2] * K)
    return conv_z + b


def conv_forword(z, K, b, padding=(0, 0), strides=(1, 1)):
    """
    多通道卷积前向过程
    :param z: 卷积层矩阵,形状(N,C,H,W)，N为batch_size，C为通道数
    :param K: 卷积核,形状(C,D,k1,k2), C为输入通道数，D为输出通道数
    :param b: 偏置,形状(D,)
    :param padding: padding
    :param strides: 步长
    :return: 卷积结果
    """
    padding_z = np.lib.pad(z, ((0, 0), (0, 0), (padding[0], padding[0]), (padding[1], padding[1])), 'constant', constant_values=0)
    N, _, height, width = padding_z.shape
    C, D, k1, k2 = K.shape
    assert (height - k1) % strides[0] == 0, '步长不为1时，步长必须刚好能够被整除'
    assert (width - k2) % strides[1] == 0, '步长不为1时，步长必须刚好能够被整除'
    conv_z = np.zeros((N, D, 1 + (height - k1) // strides[0], 1 + (width - k2) // strides[1]))
    for n in np.arange(N):
        for d in np.arange(D):
            for h in np.arange(height - k1 + 1)[::strides[0]]:
                for w in np.arange(width - k2 + 1)[::strides[1]]:
                    conv_z[n, d, h // strides[0], w // strides[1]] = np.sum(padding_z[n, :, h:h + k1, w:w + k2] * K[:, d]) + b[d]
    return conv_z


if __name__ == "__main__":
    z = np.ones((5, 5))
    k = np.ones((3, 3))
    b = 3
    #print(_single_channel_conv(z, k,padding=(1,1)))
    #print(_single_channel_conv(z, k, strides=(2, 2)))
    assert _single_channel_conv(z, k).shape == (3, 3)
    assert _single_channel_conv(z, k, padding=(1, 1)).shape == (5, 5)
    assert _single_channel_conv(z, k, strides=(2, 2)).shape == (2, 2)
    assert _single_channel_conv(z, k, strides=(2, 2), padding=(1, 1)).shape == (3, 3)
    assert _single_channel_conv(z, k, strides=(2, 2), padding=(1, 0)).shape == (3, 2)
    assert _single_channel_conv(z, k, strides=(2, 1), padding=(1, 1)).shape == (3, 5)

    z = np.ones((8, 16, 5, 5))
    k = np.ones((16, 32, 3, 3))
    b = np.ones((32))
    assert conv_forword(z, k, b).shape == (8, 32, 3, 3)
    print(conv_forword(z, k, b)[0, 0])
