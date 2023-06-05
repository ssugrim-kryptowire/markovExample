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
    '''When drawing digits sequentially, 123 has a slight advnatage over 111
    because of the ability to transition back to an intermediate state.
    
    Consider the markov chains, in the 11 mid state of the 111 seuqence, 
    there is only once digit that will give you a complete sequece (namely 1)
    
    In the 123 case when you reach 12, if you get a one, you have only 
    regressed a single step as opposed to starting from the None state.
    
    Mutating the problem a little bit, you can see that 121 should have the
    same property as 111 but it does not, when you check in simulation the 121 
    case looks more like the 123 case. 
    
    The 121 case is iteresting, it's breaks the symetry but at the front.
    The have seen a 1 case has a 1/10 probablity of not going all the way
    back to None. It's only the 3 sequences that will fail linearly.
    
    When drawn simultaneously (3 at a time), the drawing is done from the 
    (1/10)^3 probablity space, and the "they should be the same" answer is
    returned.
    
    Graphs:
    
    digraph one_two_one {
	rankdir=LR;
        None -> None [ label = "9/10" ];
        None -> 1 [ label = "1/10" ];
        1 -> None [ label = "8/10" ];
	1 -> 1 [ label = "1/10" ];
	1 -> 12 [ label = "1/10" ];
	12 -> None [ label = "9/10" ];
	12 -> 121 [ label = "1/10" ];
    }
 
    digraph one_two_three {
	rankdir=LR;
        None -> None [ label = "9/10" ];
        None -> 1 [ label = "1/10" ];
	1 -> 12 [ label = "1/10" ];
	1 -> 1 [ label = "1/10" ];
	1 -> None [ label = "8/10" ];
	12 -> 123 [ label = "1/10" ];
	12 -> 1 [ label = "1/10" ];
	12 -> None [ label = "8/10" ];
    }
    
    digraph one_one_one {
	rankdir=LR;
        None -> 1 [ label = "1/10" ];
        None -> None [ label = "9/10" ];
	1 -> 11 [ label = "1/10" ];
	1 -> None [ label = "9/10" ];
	11 -> 111 [ label = "1/10" ];
	11 -> None [ label = "9/10" ];
    }

    Mermaid version:
      graph TD
      
      subgraph one-two-one
          None -->|9/10| None
          12 -->|9/10| None
          1 -->|8/10| None 
          None -->|1/10| 1
          1 -->|1/10| 1 
          1 -->|1/10| 12
          12 -->|1/10| 121
           
      end
      
      subgraph one-two-three
          n1(none) -->|9/10| n1
          b -->|8/10| n1
          a -->|8/10| n1
          n1 -->|1/10| a[1]
          a -->|1/10| a
          b -->|1/10| a
          a -->|1/10| b[12]
          b -->|1/10| c[123]    
      end
      
      subgraph one-one-one
          n2(none) -->|9/10| n2
          d -->|9/10| n2
          e -->|9/10| n2
          n2 -->|1/10| d[1]
          d -->|1/10| e[11]
          e -->|1/10| f[111]    
      end
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
