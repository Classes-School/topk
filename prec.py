
from bruteforce import time_for_interval_bruteforce
from lskbucket import time_for_interval_lsh
from matplotlib import pyplot as plt
import numpy as np
from bruteforce import run_bruteforce_on_interval
from lskbucket import build_lsh_from_file_and_given_interval

arr_precision = np.empty(shape=(25,1))
arr_recall = np.empty(shape=(25,1))

precision_final = np.empty(shape=(100,1))
recall_final = np.empty(shape=(100,1))

def precision_for_query(interval, brute_result, lsh):
    """
    2b3m-wnm2#3.txt [(1.0, '2b3m-wnm2#3.txt'), (0.05454545454545454, '3fcn-e5dk#23.txt'), 
                     (0.040268456375838924, '2mtu-ysnw#1.txt'), (0.04, '265m-q8pf#1.txt'), 
                     (0.03773584905660377, '2zaf-wufx#0.txt'), (0.033962264150943396, '2ft4-4uik#1.txt'), 
                     (0.03271028037383177, '2g5r-pikx#1.txt'), (0.030716723549488054, '5d79-9xqr#4.txt'), 
                     (0.0273972602739726, '4fd4-wqps#22.txt'), (0.02702702702702703, '3mxm-hwme#0.txt'), 
                     (0.024390243902439025, '3h9x-7bvm#51.txt'), (0.024390243902439025, '3h9x-7bvm#19.txt')
                     ]
    """
    comparison_to_baseline = {}
    i = 0
    for key, inner_jaccard_map in brute_result.items():
        brute_key_jaccard_docs = set(inner_jaccard_map)
        lsh_key_jaccard_docs = set((lsh.get(key)))

        tp = len(lsh_key_jaccard_docs.intersection(brute_key_jaccard_docs))
        fp = len(lsh_key_jaccard_docs.difference(brute_key_jaccard_docs)) 
        fn = len(brute_key_jaccard_docs.difference(lsh_key_jaccard_docs))

        precision = tp/(tp + fp)        
        recall = tp/(tp + fn)
        arr_precision[i] = precision
        arr_recall[i] = recall
        i = i+1
    precision_final = np.concatenate (precision_final,arr_precision)
    recall_final = np.concatenate (recall_final,arr_recall)
    return comparison_to_baseline


def run_both_then_precision(interval):
    brute_result = run_bruteforce_on_interval(interval)
    lsh_result = build_lsh_from_file_and_given_interval(interval)
    comparison_res = precision_for_query(interval, brute_result, lsh_result)
    # interval_comparison.update(in)
    print(comparison_res)

def plot1(recall_final, precision_final):
    plt.plot(recall_final,precision_final, 'o', color='black' )
    #add axis labels to plot
    plt.title('Precision-Recall Curve')
    plt.ylabel('Precision')
    plt.xlabel('Recall')
    #display plot
    plt.show()

def plot():
    run_both_then_precision("0.interval")
    run_both_then_precision("1.interval")
    run_both_then_precision("2.interval")
    run_both_then_precision("3.interval")

    t_bruteforce = time_for_interval_bruteforce
    t_lsh = time_for_interval_lsh
    # extract(t_bruteforce, t_lsh)
    b_arr = [0]*4
    l_arr = [0]*4
    i = 0
    for key, time_b in t_bruteforce.items():
        time_l = t_lsh.get(key)
        b_arr[i] = time_b
        l_arr[i] = time_l
        i = i+1

    interval = [0,1,2,3]
    plt.plot(interval, b_arr, label = "BruteForce")
    plt.plot(interval, l_arr, label = "LSH")
    plt.title('Time LSH vs. Time Brute Force Curve')
    plt.ylabel('time')
    plt.xlabel('intervals')
    #display plot
    plt.legend()
    plt.show()

# {int: time,  int:time}
# plot(t_bruteforce.get("0.interval"), t_lsh.get("0.interval"))

# print(recall_final)
print(arr_precision)
# plot1)
# plot()