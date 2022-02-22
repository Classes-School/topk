
from bruteforce import time_for_interval_bruteforce
from lskbucket import time_for_interval_lsh
from matplotlib import pyplot as plt
import numpy
from bruteforce import run_bruteforce_on_interval
from lskbucket import build_lsh_from_file_and_given_interval

arr_precision = [0] * 25
arr_recall = [0] * 25

precision_final = []
recall_final = []

def precision_for_query(interval, brute_result, lsh):
    """
    format for both brute_result and lsh
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
        precision_final.append(precision)

        arr_recall[i] = recall
        recall_final.append(recall)
        i = i+1

    print(arr_precision)
    print(arr_recall)
    return comparison_to_baseline


def run_both_then_precision(interval):
    brute_result = run_bruteforce_on_interval(interval)
    lsh_result = build_lsh_from_file_and_given_interval(interval)
    precision_for_query(interval, brute_result, lsh_result)

def plot_recall_prec(arr_recall, arr_precision):
    plt.plot(arr_recall,arr_precision, 'o', color='black'  )

    #add axis labels to plot
    plt.title('Precision-Recall Curve for Interval 1')
    plt.ylabel('Precision')
    plt.xlabel('Recall')
    #display plot
    plt.show()

b_arr = [0]*4
l_arr = [0]*4

def plot():
    avg = 10
    t_bruteforce = {}
    t_lsh = {}
    for i in range(avg):
        run_both_then_precision("0.interval")
        run_both_then_precision("1.interval")
        run_both_then_precision("2.interval")
        run_both_then_precision("3.interval")

        for key, time_br in time_for_interval_bruteforce.items():
            time_lr = time_for_interval_lsh.get(key)
            if t_bruteforce.get(key) != None:
                t_bruteforce.update({key: time_br + t_bruteforce.get(key)})
                t_lsh.update({key: time_lr + t_lsh.get(key)})
            else:
                t_bruteforce.update({key: time_br})
                t_lsh.update({key: time_lr})

    i = 0
    print((t_bruteforce.get("0.interval")))
    for key, time_b in t_bruteforce.items():
        time_l = t_lsh.get(key)
        time_b = time_b/avg
        time_l = time_l/avg
        
        b_arr[i] += time_b
        l_arr[i] += time_l
        i = i+1

    print(b_arr)
    print(l_arr)
    
    interval = [0,1,2,3]
    plt.plot(interval, b_arr, label = "BruteForce")
    plt.plot(interval, l_arr, label = "LSH")
    plt.title('10 Time Average LSH vs. Time Brute Force Curve')
    plt.ylabel('time')
    plt.xlabel('intervals')
    #display plot
    plt.legend()
    plt.show()

run_both_then_precision("0.interval")
run_both_then_precision("1.interval")
run_both_then_precision("2.interval")
run_both_then_precision("3.interval")
plot_recall_prec(recall_final, precision_final)
plot()
