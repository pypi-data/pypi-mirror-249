"""Implementation of data_struct for Sketch2DStatic and Sketch2DApp.

License:
    BSD
"""

import csv
import json
import typing

import sketching.data_struct


class LocalDataLayer(sketching.data_struct.DataLayer):
    """Implementation of DataLayer for desktop environment."""

    def get_csv(self, path: str) -> sketching.data_struct.Records:
        with open(path) as f:
            rows = list(csv.DictReader(f))

        return rows

    def write_csv(self, records: sketching.data_struct.Records,
        columns: sketching.data_struct.Columns, path: str):
        def build_record(target: typing.Dict) -> typing.Dict:
            return dict(map(lambda key: (key, target[key]), columns))

        records_serialized = map(build_record, records)

        with open(path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=columns)  # type: ignore
            writer.writeheader()
            writer.writerows(records_serialized)

    def get_json(self, path: str):
        with open(path) as f:
            target = json.load(f)

        return target

    def write_json(self, target, path: str):
        with open(path, 'w') as f:
            json.dump(target, f)
