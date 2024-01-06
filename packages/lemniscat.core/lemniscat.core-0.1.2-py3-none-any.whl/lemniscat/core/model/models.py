from dataclasses import dataclass
from typing import List

@dataclass
class Meta:
    name: str
    description: str
    version: str

    def __str__(self) -> str:
        return f'{self.name}: {self.version}'


@dataclass
class TaskResult:
    name: str
    status: str
    errors: List[str]