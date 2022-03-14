import abc
from typing import Any, List

from uk.street.crimes.domain.dataclass import StreetCrime, StreetCrimeOutcome


class Provider(abc.ABC):
    @abc.abstractmethod
    def fetch(self) -> List[Any]:
        pass


class StreetCrimeProvider(Provider):
    @abc.abstractmethod
    def fetch(self) -> List[StreetCrime]:
        pass


class StreetCrimeOutcomeProvider(Provider):
    @abc.abstractmethod
    def fetch(self) -> List[StreetCrimeOutcome]:
        pass
