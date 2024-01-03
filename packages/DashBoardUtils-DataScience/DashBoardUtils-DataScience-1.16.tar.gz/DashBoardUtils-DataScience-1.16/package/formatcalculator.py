import pandas as pd
from package.keyborddata import *

def get_unique_hashes_from_data(chuncks):
    df = pd.DataFrame.from_records(chuncks).fillna("0")
    cols = df.columns.to_list()
    df_list = []
    for x in cols:
        d = df[df[x] != "0"]
        df_list.append(d[x])

    series_list = []
    for s in df_list:
        lables = []
        for e in s:
            lables += e["lables"]

        unique_lables = []
        for xsa in lables:
            if xsa not in unique_lables:
                unique_lables.append(xsa)
        series_list.append(unique_lables)

    hash_list = []
    for x in series_list:
        hash_lables = []
        for q in x:
            datalen = len(q)
            hash = r""
            for xs in range(datalen):
                if str(q[xs]) in alphabets:
                    hash += "[a-z]{1}"
                elif str(q[xs]) in alphabets_upper:
                    hash += "[A-Z]{1}"
                elif str(q[xs]) in simbols:
                    hash += str(q[xs])
                else:
                    data = None
                    try:
                        data = int(q[xs])
                    except Exception as E:
                        print("data is out of keyboard")
                    if data is not None:
                        hash += "\d{1}"
            hash_lables.append(hash)
        hash_list.append(hash_lables)

    unique_hashes = []
    for i,x in enumerate(hash_list):
        unique_hashes.append({cols[i]:list(set(x))})
    return unique_hashes

def spilt_errors_and_validated_data(chuncks, validation_regex={}):
    pass


def data_error_fixing_procedures(datadf, validated_format):
    pass
