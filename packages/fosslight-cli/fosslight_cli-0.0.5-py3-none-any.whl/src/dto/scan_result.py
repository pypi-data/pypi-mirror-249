from dataclasses import dataclass
from typing import Optional


@dataclass
class ScanResult:
    binary_file_path: Optional[str] = None
    report_file_path: Optional[str] = None
