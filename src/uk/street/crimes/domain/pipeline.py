import logging

from uk.street.crimes.domain.providers import (
    StreetCrimeOutcomeProvider,
    StreetCrimeProvider,
)
from uk.street.crimes.domain.repositories import StreetCrimeRepository
from uk.street.crimes.domain.transform import StreetCrimeOutcomeUpdater


class StreetCrimeExtractionPipeline:
    def __init__(
        self,
        street_crime_provider: StreetCrimeProvider,
        street_crime_outcome_provider: StreetCrimeOutcomeProvider,
        street_crime_repository: StreetCrimeRepository,
    ) -> None:
        self._street_crime_provider = street_crime_provider
        self._street_crime_outcome_provider = street_crime_outcome_provider
        self._street_crime_repository = street_crime_repository

    def run(self):
        street_crimes = self._street_crime_provider.fetch()
        logging.debug(f"Fetched {len(street_crimes)} street crimes.")

        street_crime_outcomes = self._street_crime_outcome_provider.fetch()
        logging.debug(f"Fetched {len(street_crime_outcomes)} street crimes.")

        street_crime_outcome_updater = StreetCrimeOutcomeUpdater(
            street_crime_outcomes=street_crime_outcomes
        )
        updated_street_crimes = street_crime_outcome_updater.update(street_crimes)
        self._street_crime_repository.save(updated_street_crimes)
