from typing import Protocol


class JobRunner(Protocol):
    def run(self, job_id: str) -> None: ...
