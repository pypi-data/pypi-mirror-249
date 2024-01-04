import pandas as pd
from package.keyborddata import *
from typing import Dict


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
    for i, x in enumerate(hash_list):
        unique_hashes.append({cols[i]: list(set(x))})
    return unique_hashes


def split_all_labels_to_words(df, exer=[" "]):
    cols = df.columns.to_list()
    final_df = []
    for k, v in df.iterrows():
        for x in cols:
            val = None
            for s in exer:
                if type(v[x]) != list:
                    if s in v[x]:
                        val = v[x].split(s)
                    else:
                        val = v[x]
                else:
                    rowval = []
                    for ix, sz in enumerate(v[x]):
                        if s in sz:
                            rowval += sz.split(s)
                        else:
                            rowval.append(sz)
                    val = rowval
            v[x] = val
        final_df.append(v.to_dict())
    return pd.DataFrame.from_records(final_df)


def FindMaxLength(lst):
    maxList = max((x) for x in lst)
    maxLength = max(len(x) for x in lst)
    return maxList, maxLength


def unpack_values_to_new_columns(dataframe, types=None):
    cols = dataframe.columns.to_list()
    datalist = []
    for x in cols:
        filter_types = dataframe[dataframe[x].astype(types) == True]
        maxindex = filter_types[x].values.to_list()
        datalist.append(((maxindex[1], x), filter_types))
    raise NotImplementedError("function work in progress")
