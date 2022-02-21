

from bruteforce import run_bruteforce_on_interval
from lskbucket import build_lsh_from_file_and_given_interval


def precision_for_query(brute_result, lsh):
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
    for key, inner_jaccard_map in brute_result.items():
        brute_key_jaccard_docs = set(inner_jaccard_map.values())
        lsh_key_jaccard_docs = set((lsh.get(key)).values())

        tp = len(lsh_key_jaccard_docs.intersection(brute_key_jaccard_docs))
        fp = len(lsh_key_jaccard_docs.difference(brute_key_jaccard_docs)) 
        fn = len(brute_key_jaccard_docs.difference(lsh_key_jaccard_docs))

        precision = tp/(tp + fp)        
        recall = tp/(tp + fn)
        comparison_to_baseline.update({key: [precision,recall]})
    return comparison_to_baseline


def run_both_then_precision(interval):
    brute_result = run_bruteforce_on_interval(interval)
    print(brute_result)
    # lsh_result = build_lsh_from_file_and_given_interval(interval)
    # comparison_res = precision_for_query(brute_result, lsh_result)
    # print(lsh_result)

run_both_then_precision("2.interval")