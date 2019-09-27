from deoplete.util import Candidate, Candidates, Nvim, UserContext
from deoplete.source.base import Base
from pathlib import Path
from subprocess import CalledProcessError, check_output
from typing import Dict


class Source(Base):
    def __init__(self, vim: Nvim):
        super().__init__(vim)

        self.name = "ghq"
        self.mark = "[ghq]"
        self.rank = 10000
        self.min_pattern_length = 3
        self.__result: Candidates = []

    def on_init(self, context: UserContext) -> None:
        self.__result = []

    def gather_candidates(self, context: UserContext) -> Candidates:
        try:
            output: bytes = check_output("ghq list", shell=True)
        except CalledProcessError as e:
            self.error("error on executing ghq: " + str(e))
            return []
        return self._candidates(output.decode("utf-8"))

    def _candidates(self, output: str) -> Candidates:
        candidates: Dict[str, Candidate] = {}
        for line in output.split():
            path = Path(line)
            if len(path.parts) == 0:
                continue
            words = [str(Path(*path.parts[x:])) for x in range(0, len(path.parts))]
            for word in words:
                if word not in candidates:
                    candidates[word] = {"word": word, "menu": line, "dup": 0}
        return list(candidates.values())
