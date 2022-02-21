
import heapq
import timeit
from helper import QUERY_DIR, read_all_from_disk, read_file_as_list, write_to_disk

k = 12
each = read_all_from_disk("docj_to_shingle_map.pkl")

def bruteforce_query(docj, each):
    h = []
    docj_shingle_set = each.get(docj)
    for key, value in each.items():
        """
            do we include itself?
        """
        # if key == docj:
        #     continue
        intersection = len(docj_shingle_set.intersection(value))
        union = len(docj_shingle_set.union(value))
        jaccard = intersection/union

        heapq.heappush(h, (jaccard, key))
    return heapq.nlargest(k, h) 




def run_bruteforce_on_interval(interval_name):
    """
        a key,value pair of interval_jaccard_results will look like: {query : [(jaccard, doc), ...(kth_jaccard, kth_doc)]}
    """
    interval_jaccard_results = {} 
    # each =  read_all_from_disk("sig.pkl")
    all_queries = read_file_as_list(interval_name, QUERY_DIR)
    start_bruteforce = timeit.timeit()
    for query in all_queries:
        interval_jaccard_results.update({query : bruteforce_query(query,each) })
    end_bruteforce = timeit.timeit()
    time_for_interval.update({interval_name : end_bruteforce-start_bruteforce})

    write_to_disk(interval_jaccard_results, interval_name+"_brute"+".pkl")
    return interval_jaccard_results, time_for_interval

interval_name = "0.interval"
time_for_interval = {}

# run_bruteforce_on_interval(interval_name)
# for i, j in query_interval.items():
#     print(i, j)
#     print()
print(time_for_interval.get(interval_name))