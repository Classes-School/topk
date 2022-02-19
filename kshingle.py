from os import listdir
from os.path import isfile, join

"""
input: Document
output: Map including each doc and it's shingles, and all shingles sorted
"""

k = 4
map_each_doc_and_shingle  = {}
all_shingles_sorted = set()

def get_shingles(doc_txt, dir):
    """
        will think about how to access doc data sets here given doc_txt
        Using a shingle set at first in order to remove duplicates in document.
        Also doing same with all_shingles_sorted in order to remove duplicates.
    """
    shingles = set()
    with open(dir+"/"+doc_txt) as doc:
        for line in doc:
            shingles.add(line.strip())
    shingles_list = list(shingles)
    map_each_doc_and_shingle.update({doc_txt: shingles_list})
 
    global all_shingles_sorted 
    all_shingles_sorted =  all_shingles_sorted.union(shingles)

def on_to_minhash():
    """
        Converts all_shingles_sorted to a sorted list.
        Creates a map and adds {map of doc and it's shingles} as 'each' and {all_shingles_sorted}  as 'all'
        Returns the map for minhashing.
    """
    all_shingles_listed = list(all_shingles_sorted)
    all_shingles_listed.sort()

    map_for_minhash = {'each': map_each_doc_and_shingle, 'all': all_shingles_listed}
    return map_for_minhash


def k_shingling(datasets_dir = "200h_A1_datasets/datasets"):
    """
        maps each shingles as a list to a document
    """
    for f in listdir(datasets_dir):
         if isfile(join(datasets_dir, f)):
             get_shingles(f, datasets_dir)
    return on_to_minhash()

