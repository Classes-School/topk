from helper import write_to_disk
import kshingle
import timeit

modvalue = 999983
def update_denselist(d_list, sparse_index):
    """
    iterate through all 128 hash functions using B sparse's index as independent variable.
        for each (i to 128) hash function l, if the computed hash value is less than the value at index l of G
        of condesned array G, update. 
        else continue to next hash function. 
    """
    for dense_index, val in enumerate(d_list):
        hash_value = (((dense_index) * (sparse_index + 1)) + 1) % modvalue
        if hash_value < val:
            d_list[dense_index] = hash_value
    return d_list
    
def sparse_condenser(key,  sparse_list):
    """
    create an array dense_list of length n= 128
    set all values to infinity
    iterate array sparse by index
        if the value is True, update it's dense_list column value based on the hash function value corresponding to the current index.
    """
    dense_list = []
    for i in range(128):
        dense_list.append(float('inf'))

    for ind, val in enumerate(sparse_list):
        if (val):
            dense_list = update_denselist(dense_list, ind)
    return {key: dense_list}


def minhash_fun():
    """
    """
    map_from_shingle = kshingle.k_shingling()
    signature = {}
    all_shingle_set  = map_from_shingle.get("each")
    all_shingles_sorted = map_from_shingle.get("all")

    start = timeit.timeit()
    for docj in list(all_shingle_set.keys()):
        """
        """
        docj_shingles = all_shingle_set.get(docj)
        sparse_list_for_docj = [False] * len(all_shingles_sorted)
        for ind, shingle in enumerate(all_shingles_sorted): 
            if shingle in docj_shingles:
                # print("yeah" + str(i))
                sparse_list_for_docj[ind] = True
        docj_condensed = sparse_condenser(docj, sparse_list_for_docj)
        signature.update(docj_condensed)
    end = timeit.timeit()

    print(end-start)
    # not as shingles anymore but as sorted (according to all_shingles_sorted) and condensed signature matrix
    write_to_disk(signature, "sig.pkl")

minhash_fun()