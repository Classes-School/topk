import math
import timeit
import heapq

from helper import QUERY_DIR, read_all_from_disk, read_file_as_list, write_to_disk



rows = 16
band = 8
k = 12
time_for_interval_lsh = {}

"""

buckets b r 
input: a map of jdocs as keys and 128 hash functions as rows/signatures
    {doci: [signature],  docj: [signature], dock: [signature], ......}
    should I combine them to form a table? 
    WHat do I do?
"""

"""
    wait. DO WE NEED MULTIPLE HASH FUNCTIONS FOR LSH?????????
"""

mod_value = 9999983
def lsh_hash_function(value, band_to_go):
    return  (((value) * (band_to_go + 1)) + 1) % mod_value

def compute_jaccard_by_signature(docj, candidate_pairs):
    h = []
    shingle_map = read_all_from_disk("docj_to_shingle_map.pkl")
    docj_shingle = shingle_map.get(docj)
    for file in candidate_pairs:
        shingle = shingle_map.get(file)

        intersection = len(docj_shingle.intersection(shingle))
        union = len(docj_shingle.union(shingle))
        jaccard = intersection/union

        heapq.heappush(h, (jaccard, file))
    return heapq.nlargest(k, h) 

def lsh_on_single_signature(docj, signaturej, lsh_band, querying):
    """
        for each document signature, iterate the signature column accounting for band_to_go, hash the value according to 
        it's band and generate a hash.
        If the hash does not exist within the band, create a string list, add docj and add <hash, [docj]> to band b
        It the hash exists append the doc to existing list as <existing_hash, [existing_list, docj]> to band b  
    """
    candidate_pairs = set()
    for index, value in enumerate(signaturej):
        band_to_go = math.floor(index / rows)
        hashval = lsh_hash_function(value, band_to_go)
        
        if querying:
            g = lsh_band.get(band_to_go).get(hashval)

            if len(g) != 2000:
                candidate_pairs = candidate_pairs.union(lsh_band.get(band_to_go).get(hashval))
        else:
            # map_of_band --> map_of_hash_values --> [append to list of docs that hashed to that value within that band]
            # print(str(hashval), str(band_to_go), docj)
            if hashval in lsh_band.get(band_to_go).keys():
                """
                    if hashval is already there: collision: candidate pairs
                """
                lsh_band.get(band_to_go).get(hashval).add(docj)
            else:
                lsh_band.get(band_to_go)[hashval] = {docj}
    if querying:
        # return compute_jaccard_by_signature(docj, candidate_pairs)
        return compute_jaccard_by_signature(docj, candidate_pairs)
        # print(len(candidate_pairs) ,docj, ":" , (candidate_pairs))
        # print()

def lsh():
    """
        Instantiate the lsh bands based on the number of bands given.
        Iterate docj and signaturej of the condensed_signature
            For each document and it's signature: pass to lsh_on_single_signature
        This process builds up the bands dictionary 
        with each band key containing a dictionary of hashes and lists of documents that hashed to them
        Return lsh_band 
    """
    lsh_band = {}
    condensed_signaturej = read_all_from_disk("sig.pkl")
    for i in range(band):
        lsh_band.update({i: dict()}) # i band will correspond to a map {of hashvalue: (set of sets that hash to that value)}
    for docj, signaturej in condensed_signaturej.items():
        lsh_on_single_signature(docj, signaturej, lsh_band, querying=False)
    write_to_disk(lsh_band, "lsh_bands_result.pkl")


def build_lsh_from_file_and_given_interval(interval):
    """
    """
    querying_lsh_bands = read_all_from_disk("lsh_bands_result.pkl")
    all_sig = read_all_from_disk("sig.pkl")

    all_queries = read_file_as_list(interval, QUERY_DIR)
    interval_lsh_jaccard_results = {}

    start_lshtopk = timeit.timeit()
    for docj in all_queries:
        """
            QUESTION: what to do from here.
        """
        interval_lsh_jaccard_results.update( {docj : lsh_on_single_signature(docj, all_sig.get(docj), querying_lsh_bands, True) })
    end_lshtopk = timeit.timeit()
    time_for_interval_lsh.update({interval : end_lshtopk-start_lshtopk})

    write_to_disk(interval_lsh_jaccard_results, interval+"_lsh"+".pkl")
    return interval_lsh_jaccard_results

lsh()

