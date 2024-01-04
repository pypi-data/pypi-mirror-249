class DataClassifier:
    def __init__(self, algorithm=None) -> None:
        if algorithm is None:
            self.algorithm = [
                {"algorithm": "hist", "Format": ["Catagorical", "Length"]}
            ]
        else:
            self.algorithm = algorithm

    def build_ploats(self, algorithm, groups):
        getalgo = [x for x in self.algorithm if algorithm in list(x.values())][0]
        for name, group in groups:
            catagorical = []
            for x in group.columns.to_list():
                if group[x].nunique() > 1:
                    catagorical.append(
                        {
                            x: {
                                "lables": [str(x) for x in group[x].unique().tolist()],
                                "counts": [
                                    len(group[group[x] == xs])
                                    for xs in group[x].unique().tolist()
                                ],
                            }
                        }
                    )
            if getalgo["algorithm"] == "hist":
                yield catagorical
