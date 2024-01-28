import argparse
import multiprocessing
from collections import defaultdict
from operator import index
from random import random
from tkinter import ON

import numpy as np
from six import iteritems
from sklearn.metrics import (auc, f1_score, precision_recall_curve,
                             roc_auc_score)
from tqdm import tqdm
from sklearn.preprocessing import OneHotEncoder, LabelEncoder


from data_test import *


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--epoch', type=int, default=100,
                        help='Number of epoch. Default is 100.')

    parser.add_argument('--batch-size', type=int, default=64,
                        help='Number of batch_size. Default is 64.')

    parser.add_argument('--eval-type', type=str, default='all',
                        help='The edge type(s) for evaluation.')
    
    parser.add_argument('--schema', type=str, default=None,
                        help='The metapath schema (e.g., U-I-U,I-U-I).')

    parser.add_argument('--dimensions', type=int, default=8,
                        help='Number of node dimensions. Default is 200.')

    parser.add_argument('--edge-dim', type=int, default=4,
                        help='Number of edge embedding dimensions. Default is 10.')
    
    parser.add_argument('--att-dim', type=int, default=4,
                        help='Number of attention dimensions. Default is 20.')

    parser.add_argument('--window-size', type=int, default=2,
                        help='Context size for optimization. Default is 5.')
    
    parser.add_argument('--negative-samples', type=int, default=5,
                        help='Negative samples for optimization. Default is 5.')
    
    parser.add_argument('--neighbor-samples', type=int, default=10,
                        help='Neighbor samples for aggregation. Default is 10.') 

    parser.add_argument('--patience', type=int, default=5,
                        help='Early stopping patience. Default is 5.') 

    return parser.parse_args()

def load_train_data():
    print('loading training data!!!')
    dict_edge = get_edge()
    all_nodes = list()
    edge_data_by_type = dict()
    for i in range(len(dict_edge)):
        if dict_edge[i][1] not in edge_data_by_type:
            edge_data_by_type[dict_edge[i][1]] = list()
        x , y = dict_edge[i][0] , dict_edge[i][2]
        edge_data_by_type[dict_edge[i][1]].append((x , y))
        all_nodes.append(x)
        all_nodes.append(y)
    all_nodes = list(set(all_nodes))
    return all_nodes, edge_data_by_type


def get_SDC(features):
    feature_y = {} 
    keys = list(features.keys())

    for i in range(len(keys)):
        feature_y[keys[i]] = features[keys[i]][-1]
        features[keys[i]].pop()

    return features, feature_y

def get_adj():
    all_nodes, edge_data_by_type = load_train_data()
    num_node = len(all_nodes)
    keys = list(edge_data_by_type.keys())
    num_type_edge = len(list(keys)) 

    adj = []
    for i in range(num_type_edge):
        r_adj = np.zeros((num_node,num_node), dtype = float) 
        for j in range(len(edge_data_by_type[keys[i]])):
            r_adj[int(edge_data_by_type[keys[i]][j][0])][int(edge_data_by_type[keys[i]][j][1])] = 1
        print(r_adj)
        break

    return 
def load_edge_data():

    return get_edge()

def load_feature_data():
    print("load node features!!!")
    features = get_features()
    all_feature = []
    for key , value in features.items():
        all_feature.append(np.array(value))
    all_feature = np.array(all_feature)
    lc = LabelEncoder()

    for i in range(4,len(all_feature[0])-1):
        all_feature[:,i] = lc.fit_transform(all_feature[:,i])

    labels = all_feature[:, -1]


    return all_feature[:, :-1] , labels

def load_BB_info():
    dict_BB , edge = get_BB_info()
    nodes = list(dict_BB.keys()) 

    features = []
    for i in range(len(nodes)):
        features.append(dict_BB[str(i)])

    return nodes, features, edge

if __name__ == '__main__':
    nodes, edge = load_train_data()

    load_BB_info()
