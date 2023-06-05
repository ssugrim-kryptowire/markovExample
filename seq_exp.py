#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 15:46:31 2020

@author: ssugrim
"""

import logging

logging.basicConfig(format='%(asctime)s - %(filename)s -  %(levelname)s - %(message)s',
                    level=logging.INFO)



from random import randint
import numpy as np
import matplotlib.pyplot as plt

RUNS=10000
BINS=100

def sample():
    return randint(0,9)

def one_run_seq(target):
    ''' Sequential draws of the integers.
    '''
    current = [sample(),sample(), sample()]
    
    samples = 3
    
    while ''.join([str(i) for i in current]) != target:
#        print(''.join([str(i) for i in current]))
        samples +=1
        current[2] = current[1] #shift the window to the right
        current[1] = current[0]
        current[0] = sample()
    
    return samples #what we want is the number of draws until 


def one_run_sim(target):
    ''' Simultaneous draws of the integers (3 at a time)
    '''
    current = [sample(),sample(), sample()]
    
    samples = 1
    
    while ''.join([str(i) for i in current]) != target:
#        print(''.join([str(i) for i in current]))
        samples +=1
        current = [sample(),sample(), sample()]
    
    return samples


def get_data(target, runs=RUNS, mode="sim"):

    retval = None
    if mode == "sim":
        data_points = []
        for i in range(runs):
            data_points.append(one_run_seq(target))
        retval = np.array(data_points)
    elif mode == "seq":
        data_points = []
        for i in range(runs):
            data_points.append(one_run_sim(target))
        retval = np.array(data_points)
    else: 
        logging.error("Bad get data mode: {}".format(mode))

    if retval is not None:
        logging.debug("Sample count was: {}".format(len(retval)))
    return retval
    
def get_stats(arr):

    summary_5 = [np.min(arr), 
                 np.quantile(arr, 0.25),
                 np.quantile(arr, 0.5),
                 np.quantile(arr, 0.75),
                 np.max(arr)]
    return summary_5

if __name__ == '__main__':
    ''' Simulation code to test the markov chain hypothesis. Should log stats and draw a graph. 
    '''
    
    logging.info('111 case:')
    one_one_one_data = get_data('111')
    logging.info(get_stats(one_one_one_data))

    logging.info('121 case:')
    one_two_one_data = get_data('121')    
    logging.info(get_stats(one_two_one_data))
    
    logging.info('123 case:')
    one_two_three_data = get_data('123')    
    logging.info(get_stats(one_two_three_data))
    
    fig, axes = plt.subplots(2,2,figsize=(10,10))
    
    axes[0][0].hist(one_two_three_data, bins=BINS, label='123 case')    
    axes[0][0].hist(one_two_one_data, bins=BINS, label='121 case', alpha=0.5)
    axes[0][0].legend()
    
    axes[0][1].hist(one_two_three_data, bins=BINS, label='123 case')    
    axes[0][1].hist(one_one_one_data, bins=BINS, label='111 case', alpha=0.5)
    axes[0][1].legend()
    
    axes[1][0].hist(one_two_one_data, bins=BINS, label='121 case')
    axes[1][0].hist(one_one_one_data, bins=BINS, label='111 case', alpha=0.5)    
    
    axes[1][0].legend()
    
    axes[1][1].boxplot([one_two_one_data, one_two_three_data, one_one_one_data])
    axes[1][1].set_xticklabels(['121 case','123 case','111 case'])
    axes[1][1].set_ylim(0,3500)
    for tick in axes[1][1].get_xticklabels():
        tick.set_rotation(90)
