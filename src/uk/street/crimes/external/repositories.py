import logging
from typing import Sequence

from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk

from uk.street.crimes.domain.dataclass import StreetCrime
from uk.street.crimes.domain.repositories import StreetCrimeRepository


class StreetCrimeElasticsearchRepository(StreetCrimeRepository):
    def __init__(self, host: str):
        self._es = Elasticsearch(host)

    def save(self, street_crimes: Sequence[StreetCrime]):
        actions = []
        for crime in street_crimes:
            action = {
                "_index": "crime-index",
                "crimeID": crime.crime_id,
                "districtName": crime.district_name,
                "latitude": crime.latitude,
                "longitude": crime.longitude,
                "crimeType": crime.crime_type,
                "lastOutcome": crime.last_outcome,
            }
            actions.append(action)
        try:
            for success, info in parallel_bulk(self._es, actions):
                if not success:
                    logging.warning("A document failed: ", info)
        except Exception as e:
            logging.debug("Database request exception.", e)
