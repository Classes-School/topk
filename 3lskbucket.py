import math
from minhash import read_all_from_disk, write_to_disk



rows = 16
band = 8
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

lsh_band = {}
mod_value = 999983
def lsh_hash_function(value, band_to_go):
    """
        For each band, there is a hash function that takes vectors of 
        r integers and hashes them to a large number of bucketsl
    """
    return  (((value) * (band_to_go + 1)) + 1) % mod_value
  

def lsh_on_single_signature(docj, signaturej):
    """
        for each document signature, iterate the signature column accounting for band_to_go, hash the value according to 
        it's band and generate a hash.
        If the hash does not exist within the band, create a string list, add docj and add <hash, [docj]> to band b
        It the hash exists append the doc to existing list as <existing_hash, [existing_list, docj]> to band b  
    """
    for index, value in enumerate(signaturej):
        band_to_go = math.floor(index / rows)
        hashval = lsh_hash_function(value, band_to_go)
        # map_of_band --> map_of_hash_values --> [append to list of docs that hashed to that value within that band]
        # print(str(hashval), str(band_to_go), docj)
        if hashval in lsh_band.get(band_to_go).keys(): # could be turned to list if necessary
            """
                if hashval is already there: collision: candidate pairs
            """
            lsh_band.get(band_to_go).get(hashval).add(docj)
        else:
            lsh_band.get(band_to_go)[hashval] = {docj}

def lsh(condensed_signaturej):
    """
        Instantiate the lsh bands based on the number of bands given.
        Iterate docj and signaturej of the condensed_signature
            For each document and it's signature: pass to lsh_on_single_signature
        This process builds up the bands dictionary 
        with each band key containing a dictionary of hashes and lists of documents that hashed to them
        Return lsh_band 
    """
    for i in range(band):
        lsh_band.update({i: dict()}) # i band will correspond to a map {of hashvalue: (set of sets that hash to that value)}
    for docj, signaturej in condensed_signaturej.items():
        lsh_on_single_signature(docj, signaturej)
    return lsh_band

def start_from_file():
    """
    """
    condensed_signature_from_file = read_all_from_disk("sig.pkl")
    lsh_band = lsh(condensed_signature_from_file)
    write_to_disk(lsh_band, "lsh_bands.pkl")

    # for i in range(1):
    # print(len(lsh_band.get(6).get(8)))
    # 71 6 3tfu-x2qk#9.txt

def start_from_shingling():
    """
    """

# start_from_file()
lsh_file = read_all_from_disk("lsh_bands.pkl")
print(len(lsh_file.get(6).get(29)))