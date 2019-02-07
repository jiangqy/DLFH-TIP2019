#!/user/bin/python3
# +++++++++++++++++++++++++++++++++++++++++++++++++++
# @File Name: calc_hamming_ranking.py
# @Author: Qing-Yuan Jiang
# @Mail: qyjiang24 AT gmail.com
# +++++++++++++++++++++++++++++++++++++++++++++++++++

import torch
import numpy as np

from utils.args import args
from utils.logger import logger


def __hamming_dist__(test_binary, database_binary):
    """
    :param test_binary:
        test binary code: \in\{-1, +1\}^{m \times bit}
    :param database_binary:
        database binary code: \in\{-1, +1\}^{m \times bit}
    :return: hamming distance matrix: m \times n
    """
    if isinstance(test_binary, torch.Tensor):
        test_binary = test_binary.cpu().data.numpy()
    if isinstance(database_binary, torch.Tensor):
        database_binary = database_binary.cpu().data.numpy()

    bit = database_binary.shape[1]
    if test_binary.ndim == 1:
        test_binary = test_binary.reshape(-1, bit)

    return (bit - test_binary.dot(database_binary.T)) / 2.


def __calc_label_groundtruth__(test_label, database_label):
    """
    TODO
    :param test_label:
    :param database_label:
    :return:
    """
    if test_label.size == 1:
        gnd = (test_label == database_label).astype(np.float32).squeeze()
    else:
        gnd = (np.dot(test_label, database_label.T) > 0).astype(np.float32)
    return gnd


def __calc_eclidean_groundtruth__(test_feature, database_feature):
    """
    TODO
    :param test_feature:
    :param database_feature:
    :return:
    """
    pass


def calc_eclidean_hamming_ranking(test_binary, database_binary, test_feature, database_feature, param):
    pass


def calc_label_hamming_ranking(test_binary, database_binary, test_label, database_label, param):
    """
    :param test_binary:
    :param database_binary:
    :param test_label:
    :param database_label:
    :param param:
    :return:
    """
    topk = None
    topk_flag = False
    if 'topk' in param:
        topk = param['topk']
        num_topk = len(topk)
        topk_map = np.zeros((num_topk, 1))
        topk_pre = np.zeros((num_topk, 1))
        topk_rec = np.zeros((num_topk, 1))
        topk_flag = True

    bit = database_binary.shape[1]
    if test_binary.ndim == 1:
        test_binary = test_binary.reshape(-1, bit)

    metric = {}
    map = 0.0
    num_test = test_binary.shape[0]
    for ind in range(num_test):
        groundtruth = __calc_label_groundtruth__(test_label[ind], database_label)

        tsum = np.sum(groundtruth)
        if tsum == 0:
            continue
        dist = __hamming_dist__(test_binary[ind], database_binary)
        index = np.argsort(dist)
        groundtruth = groundtruth[index].squeeze()
        count = np.linspace(1, float(tsum), int(tsum))

        tindex = np.asarray(np.where(groundtruth == 1)) + 1.
        # print(count)
        # print(tindex)
        # print('-----------------')
        map_ = np.mean(count / tindex.squeeze())
        # print(map_)
        map += map_
        if topk_flag:
            for ii, topk_ in enumerate(topk):
                tgroundtruth = groundtruth[0: topk_]
                tsum = np.sum(tgroundtruth)
                if tsum == 0:
                    continue

                count = np.linspace(1, float(tsum), int(tsum))
                tindex = np.asarray(np.where(tgroundtruth == 1)) + 1.0
                topkmap_ = np.mean(count / tindex.squeeze())
                topk_map[ii] += topkmap_
                topkpre_ = tsum / topk[ii]
                topkrec_ = tsum / float(np.sum(groundtruth))
                topk_pre[ii] += topkpre_
                topk_rec[ii] += topkrec_
    metric['map'] = map / num_test
    if topk_flag:
        metric['topkmap'] = topk_map / num_test
        metric['topkpre'] = topk_pre / num_test
        metric['topkrec'] = topk_rec / num_test
    return metric


def calc_hamming_ranking(test_binary, database_binary, test_metric, database_metric, param, type='label'):
    if type == "label":
        return calc_label_hamming_ranking(test_binary, database_binary, test_metric, database_metric, param)
    elif type == "eclidean":
        return calc_eclidean_hamming_ranking(test_binary, database_binary, test_metric, database_metric, param)
    else:
        raise NameError('Unsupported groundtruth type: {}'.format(type))

