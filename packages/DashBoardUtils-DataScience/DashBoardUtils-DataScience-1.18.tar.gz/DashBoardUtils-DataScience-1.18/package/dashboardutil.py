from datetime import datetime
from typing import List
import pandas as pd


class DashboardElementsBuilder:
    def __init__(self, data, DataClassifier) -> None:
        if isinstance(data, pd.DataFrame):
            self.data = data
        else:
            raise ValueError("data should be instance of Dataframe")
        self.classifier = DataClassifier

    def prepare_sections(self, columns):
        filters = self.data[columns]
        return filters

    def get_columns_groups(self, columns):
        alldata_groups = []
        for x in columns:
            if type(self.prepare_sections(columns)[x]) != datetime:
                alldata_groups.append(self.prepare_sections(columns).groupby([x]))
            else:
                alldata_groups.append(
                    self.prepare_sections(columns).groupby(
                        by=[
                            getattr(self.prepare_sections(columns), x).month,
                            getattr(self.prepare_sections(columns), x).year,
                        ]
                    )
                )
                alldata_groups.append(
                    self.prepare_sections(columns).groupby(
                        by=[
                            getattr(self.prepare_sections(columns), x).day,
                            getattr(self.prepare_sections(columns), x).month,
                        ]
                    )
                )
                alldata_groups.append(
                    self.prepare_sections(columns).groupby(
                        by=[getattr(self.prepare_sections(columns), x).month]
                    )
                )
                alldata_groups.append(
                    self.prepare_sections(columns).groupby(
                        by=[getattr(self.prepare_sections(columns), x).day]
                    )
                )
                alldata_groups.append(
                    self.prepare_sections(columns).groupby(
                        by=[getattr(self.prepare_sections(columns), x).year]
                    )
                )
                alldata_groups.append(
                    self.prepare_sections(columns).groupby(
                        by=[
                            getattr(self.prepare_sections(columns), x).day,
                            getattr(self.prepare_sections(columns), x).year,
                        ]
                    )
                )
        return alldata_groups

    def build_ploats(self, algorithm, columns):
        for x in self.get_columns_groups(columns):
            yield self.classifier.build_ploats(algorithm, x)
