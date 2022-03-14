import abc
from typing import Sequence

from uk.street.crimes.domain.dataclass import StreetCrime


class StreetCrimeRepository(abc.ABC):
    def save(self, street_crimes: Sequence[StreetCrime]):
        pass
