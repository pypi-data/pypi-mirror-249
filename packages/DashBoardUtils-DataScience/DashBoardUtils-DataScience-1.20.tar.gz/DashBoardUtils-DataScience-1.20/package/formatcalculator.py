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


def split_all_labels_to_words_with_new_cols(df, exer=[" "]):
    numdata = df
    df = df.select_dtypes(include=["object"])
    cols_to_select = set(numdata.columns.to_list()) - set(df.columns.to_list())
    result = df.to_dict("records")
    cols = df.columns.to_list()
    final_df = []
    for v in result:
        for x in cols:
            val = None
            for s in exer:
                if type(v[x]) != list:
                    if s in v[x]:
                        val = v[x].split(s)
                    else:
                        val = v[x]
            v[x] = val
        final_df.append(v)
    df_list = []
    for v in final_df:
        cd = {}
        for d, n in v.items():
            if type(n) == list:
                for i, xs in enumerate(n):
                    if i == 0:
                        cd[d] = xs
                    else:
                        cd["_".join([d, str(i)])] = xs
            else:
                cd[d] = n
        df_list.append(cd)
    return pd.DataFrame.from_records(df_list).join(numdata[list(cols_to_select)])


def hash_df_single_df_column(Series):
    for k, v in Series.items():
        hash = ""
        for x in str(v):
            if str(x) in alphabets:
                hash += "[a-z]{1}"
            elif str(x) in alphabets_upper:
                hash += "[A-Z]{1}"
            elif str(x) in simbols:
                hash += str(x)
            else:
                data = None
                try:
                    data = int(x)
                except Exception as E:
                    print("data is out of keyboard", x)
                if data is not None:
                    hash += "\d{1}"
        yield k, hash


def hash_df_formats(df):
    df_list = []
    for x, s in df.iterrows():
        value = None
        idx = [sa[0] for sa in list(hash_df_single_df_column(s))]
        vals = [sw[1] for sw in list(hash_df_single_df_column(s))]
        value = pd.Series(vals, index=idx)
        df_list.append(value.to_dict())
    return pd.DataFrame.from_records(df_list)


def get_unique_hashes_from_df_columnwise(df):
    for x in df.columns.to_list():
        yield df[x].unique().to_list()
