from functools import lru_cache
from io import StringIO
from typing import List

import numpy as np
import pandas as pd
import requests
import s2sphere as s2


@lru_cache(maxsize=1)
def download_cell_partitionings(
    cell_levels=[5000, 2000, 1000], shortnames=["coarse", "middle", "fine"]
):
    if len(cell_levels) != len(shortnames):
        raise ValueError("cell_levels and shortnames must have the same length")

    url_templates = [
        "https://raw.githubusercontent.com/TIBHannover/GeoEstimation/original_tf/geo-cells/cells_50_{}.csv",
        # Add more URL templates here if needed
    ]

    files = []

    for cell_level in cell_levels:
        for url_template in url_templates:
            url = url_template.format(cell_level)
            try:
                response = requests.get(url)
                response.raise_for_status()
                files.append(response.content)
                break  # Download was successful, so we can stop trying
            except requests.exceptions.RequestException as e:  # noqa F841
                continue  # Try the next URL template
        else:
            # None of the URL templates worked
            raise Exception(
                f"Failed to download cell partitioning for level {cell_level}"
            )

    files_decoded = [file.decode("utf-8") for file in files]

    partitionings = {
        "files": files_decoded,
        "shortnames": shortnames,
    }

    return partitionings


class Partitioning:
    def __init__(
        self,
        csv_file: str,
        shortname=None,
        skiprows=None,
        index_col="class_label",
        col_class_label="hex_id",
        col_latitute="latitude_mean",
        col_longitude="longitude_mean",
    ):
        """
        Required information in CSV:
            - class_indexes from 0 to n
            - respective class labels i.e. hexid
            - latitude and longitude
        """
        self._df = pd.read_csv(
            StringIO(csv_file), index_col=index_col, skiprows=skiprows
        )
        self._df = self._df.sort_index()

        self._nclasses = len(self._df.index)
        self._col_class_label = col_class_label
        self._col_latitude = col_latitute
        self._col_longitude = col_longitude

        # map class label (hexid) to index
        self._label2index = dict(
            zip(self._df[self._col_class_label].tolist(), list(self._df.index))
        )

        self.name = shortname
        if shortname:
            self.shortname = shortname
        else:
            self.shortname = self.name

    def __len__(self):
        return self._nclasses

    def __repr__(self):
        return f"{self.name} short: {self.shortname} n: {self._nclasses}"

    def get_class_label(self, idx):
        return self._df.iloc[idx][self._col_class_label]

    def get_lat_lng(self, idx):
        x = self._df.iloc[idx]
        return float(x[self._col_latitude]), float(x[self._col_longitude])

    def contains(self, class_label):
        if class_label in self._label2index:
            return True
        return False

    def label2index(self, class_label):
        try:
            return self._label2index[class_label]
        except KeyError:
            raise KeyError(f"unkown label {class_label} in {self}")


class Hierarchy:
    def __init__(self, partitionings: List[Partitioning]):
        """
        Provide a matrix of class indices where each class of the finest partitioning will be assigned
        to the next coarser scales.

        Resulting index matrix M has shape: max(classes) * |partitionings| and is ordered from coarse to fine
        """
        self.partitionings = partitionings

        self.M = self.__build_hierarchy()

    def __build_hierarchy(self):
        def _hextobin(hexval):
            thelen = len(hexval) * 4
            binval = bin(int(hexval, 16))[2:]
            while (len(binval)) < thelen:
                binval = "0" + binval

            binval = binval.rstrip("0")
            return binval

        def _create_cell(lat, lng, level):
            p1 = s2.LatLng.from_degrees(lat, lng)
            cell = s2.Cell.from_lat_lng(p1)
            cell_parent = cell.id().parent(level)
            hexid = cell_parent.to_token()
            return hexid

        cell_hierarchy = []

        finest_partitioning = self.partitionings[-1]
        if len(self.partitionings) > 1:
            # loop through finest partitioning
            for c in range(len(finest_partitioning)):
                cell_bin = _hextobin(self.partitionings[-1].get_class_label(c))
                level = int(len(cell_bin[3:-1]) / 2)
                parents = []

                # get parent cells
                for lvl in reversed(range(2, level + 1)):
                    lat, lng = finest_partitioning.get_lat_lng(c)
                    hexid_parent = _create_cell(lat, lng, lvl)
                    # to coarsest partitioning
                    for p in reversed(range(len(self.partitionings))):
                        if self.partitionings[p].contains(hexid_parent):
                            parents.append(
                                self.partitionings[p].label2index(hexid_parent)
                            )

                    if len(parents) == len(self.partitionings):
                        break

                cell_hierarchy.append(parents[::-1])
        M = np.array(cell_hierarchy, dtype=np.int32)
        assert max([len(p) for p in self.partitionings]) == M.shape[0]
        assert len(self.partitionings) == M.shape[1]
        return M
