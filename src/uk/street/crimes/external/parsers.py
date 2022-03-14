import logging
from typing import Mapping, Optional

from uk.street.crimes.domain.dataclass import StreetCrime, StreetCrimeOutcome


class StreetCrimeParser:
    def parse(self, raw_street_crime: Mapping) -> Optional[StreetCrime]:
        try:
            crime_id = raw_street_crime.get("Crime ID")
            if not crime_id:
                return None

            latitude = raw_street_crime.get("Latitude")
            if latitude:
                latitude = float(latitude)

            longitude = raw_street_crime.get("Longitude")
            if longitude:
                longitude = float(longitude)

            return StreetCrime(
                crime_id=crime_id,
                district_name=None,
                latitude=latitude,
                longitude=longitude,
                crime_type=raw_street_crime.get("Crime type"),
                last_outcome=raw_street_crime.get("Last outcome category"),
            )
        except Exception as e:
            logging.debug(f"Couldn't parse object: {str(raw_street_crime)}", e)
            return None


class StreetCrimeOutcomeParser:
    def parse(self, raw_street_crime: Mapping) -> Optional[StreetCrimeOutcome]:
        try:
            return StreetCrimeOutcome(
                crime_id=raw_street_crime.get("Crime ID"),
                outcome=raw_street_crime.get("Outcome type"),
            )
        except Exception as e:
            logging.debug(f"Couldn't parse object: {str(raw_street_crime)}", e)
            return None
