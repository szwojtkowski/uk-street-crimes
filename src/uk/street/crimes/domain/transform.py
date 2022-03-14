from typing import Dict, List, Sequence

from uk.street.crimes.domain.dataclass import StreetCrime, StreetCrimeOutcome


def group_street_crime_outcomes(
    street_crime_outcomes: Sequence[StreetCrimeOutcome],
) -> Dict[str, StreetCrimeOutcome]:
    grouped_outcomes = {}
    for street_crime_outcome in street_crime_outcomes:
        grouped_outcomes[street_crime_outcome.crime_id] = street_crime_outcome

    return grouped_outcomes


class StreetCrimeOutcomeUpdater:
    def __init__(self, street_crime_outcomes: Sequence[StreetCrimeOutcome]) -> None:
        self._street_crime_outcomes = group_street_crime_outcomes(street_crime_outcomes)

    def update(self, street_crimes: Sequence[StreetCrime]) -> List[StreetCrime]:
        result = []
        for street_crime in street_crimes:
            crime_id = street_crime.crime_id
            if crime_id is not None and crime_id in self._street_crime_outcomes:
                street_crime_outcome = self._street_crime_outcomes[crime_id]
                street_crime.last_outcome = street_crime_outcome.outcome
            result.append(street_crime)

        return result
