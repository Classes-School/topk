import pickle

QUERY_DIR = "200h_A1_datasets/queries/"
DATASET_DIR = "200h_A1_datasets/datasets/"

def write_to_disk(signature_map, name):
    """
    """
    map_file = open(name, "wb")
    pickle.dump(signature_map, map_file)
    map_file.close()
    

def read_all_from_disk(name):
    n = open(name, "rb")
    output = pickle.load(n)
    return output


def read_file_as_list(file_name = "0.interval", directory=""):
    """
    """
    inside_file = []
    with open(directory+"/"+file_name) as f:
        for line in f:
            inside_file.append(line.strip())
    return inside_file

def read_file_as_set(doc_txt, dir):
    """
        will think about how to access doc data sets here given doc_txt
        Using a shingle set at first in order to remove duplicates in document.
        Also doing same with all_shingles_sorted in order to remove duplicates.
    """
    shingles = set()
    with open(dir+"/"+doc_txt) as doc:
        for line in doc:
            shingles.add(line.strip())