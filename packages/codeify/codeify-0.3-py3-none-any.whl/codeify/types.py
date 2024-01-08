from dataclasses import dataclass
from typing import Iterable, Any, Dict, Optional

@dataclass
class CodeGeneration:
    input_dir: str
    output_dir: str
    spec_file: str

@dataclass
class FileGeneration:
    input_file: str
    output_file: str
    data: Dict[str, Any]

class DirectoryContext:
    def __init__(self, ignore_files: Optional[Iterable[str]] = None, file_generators: Optional[Iterable[FileGeneration]] = None):
        self._ignore = set(ignore_files) if ignore_files else set()
        self._generators = list(file_generators) if file_generators else list()

    def ignore_file(self, filename: str) -> bool:
        return filename in self._ignore

    @property
    def file_generators(self) -> Iterable[FileGeneration]:
        yield from self._generators
