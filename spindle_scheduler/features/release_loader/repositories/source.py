from dataclasses import dataclass

from ..domains import RawRelease
from ..infra.local import read_releases


@dataclass
class SourceRepository:
    def read_releases(self) -> list[RawRelease]:
        return read_releases()


source_repository = SourceRepository()
