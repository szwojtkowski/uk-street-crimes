import csv
import logging
import os
import re
from typing import List, Optional

import fsspec as fs
from fsspec.core import url_to_fs

from uk.street.crimes.domain.dataclass import StreetCrime, StreetCrimeOutcome
from uk.street.crimes.domain.providers import (
    StreetCrimeOutcomeProvider,
    StreetCrimeProvider,
)
from uk.street.crimes.external.parsers import (
    StreetCrimeOutcomeParser,
    StreetCrimeParser,
)


def get_csv_data_subdir_paths(data_dir: str) -> List[str]:
    filesystem, _ = url_to_fs(data_dir)
    paths = filesystem.ls(data_dir)
    subdir_paths = [path for path in paths if os.path.isdir(path)]
    return subdir_paths


class StreetCrimeCsvProvider(StreetCrimeProvider):
    def __init__(self, data_dir: str, street_crime_parser: StreetCrimeParser) -> None:
        self._data_dir = data_dir
        self._street_crime_parser = street_crime_parser

    @staticmethod
    def _extract_district_name_from_filename(filename: str) -> Optional[str]:
        try:
            extracted_name = re.search("[0-9]+-[0-9]+-(.+?).csv", filename).group(1)
            return extracted_name.replace("-", " ")
        except AttributeError:
            logging.debug(f"Couldn't extract district name from filename: {filename}")
            return None

    def fetch(self) -> List[StreetCrime]:
        files = fs.open_files(f"{self._data_dir}**/*-street.csv", mode="r")

        street_crimes = []
        for file in files:
            with file as fh:
                basename = os.path.basename(file.path)
                district_name = self._extract_district_name_from_filename(basename)
                reader = csv.DictReader(fh)
                for row in reader:
                    street_crime = self._street_crime_parser.parse(row)

                    if street_crime is not None:
                        street_crime.district_name = district_name
                        street_crimes.append(street_crime)

        return street_crimes


class StreetCrimeOutcomeCsvProvider(StreetCrimeOutcomeProvider):
    def __init__(
        self, data_dir: str, street_crime_outcome_parser: StreetCrimeOutcomeParser
    ) -> None:
        self._data_dir = data_dir
        self._street_crime_outcome_parser = street_crime_outcome_parser

    def fetch(self) -> List[StreetCrimeOutcome]:
        files = fs.open_files(f"{self._data_dir}**/*-outcomes.csv", mode="r")

        street_crime_outcomes = []
        for file in files:
            with file as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    street_crime_outcome = self._street_crime_outcome_parser.parse(row)

                    if street_crime_outcome is not None:
                        street_crime_outcomes.append(street_crime_outcome)

        return street_crime_outcomes
