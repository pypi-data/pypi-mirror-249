from pathlib import Path
from typing import List
from dataclasses import dataclass, field


@dataclass
class ClassesManager:
    names: List = field(default_factory=list)
    names_kpts: List = field(default_factory=list)
    _idx: int = 0
    _idxk: int = 0

    def parse(self, x: List[str]):
        # load class from `txt` or `list` or `auto parse from txt files has been labelled`
        if len(x) == 1:
            if x[0].endswith(".txt"):  # .txt name file
                with open(x[0], "r") as f:
                    for line in f:
                        self.names.append(line.strip())
            elif x[0].endswith(".yaml") or x[0].endswith(".yml"):
                raise NotImplementedError(
                    "YAML file is not supported for now! Try TXT file"
                )
            elif Path(x[0]).is_dir():
                # auto parsing classes from labels directory
                _max = 0
                for p in Path(x[0]).rglob("*.txt"):
                    with open(p, "r") as f:
                        for line in f:
                            _max = max(int(line.strip().split(" ")[0]), _max)
                self.names = [str(x) for x in range(_max + 1)]

            else:
                self.names = x
        else:
            self.names = x

        # empty checking
        if len(self.names) == 0:
            raise ValueError(f"> Error: classes is empty => {x}.")

        # duplicates checking
        if len(self.names) != len(set(self.names)):
            raise ValueError(
                f"> Error: [--classes] | [-c] has duplicates: {self.names}"
            )

    def parse_kpts(self, x: List[str]):
        # TODO
        self.names_kpts = x

    def next(self):
        self.idx = self.count - 1 if self.idx - 1 < 0 else self.idx - 1

    def last(self):
        self.idx = 0 if self.idx + 1 > self.count - 1 else self.idx + 1

    def kpt_next(self):
        self.idxk = self.count_kpts - 1 if self.idxk - 1 < 0 else self.idxk - 1

    def kpt_last(self):
        self.idxk = 0 if self.idxk + 1 > self.count_kpts - 1 else self.idxk + 1

    @property
    def count(self):
        return len(self.names)

    @property
    def count_kpts(self):
        return len(self.names_kpts) if self.names_kpts is not None else 0

    @property
    def idx(self):
        return self._idx

    @idx.setter
    def idx(self, x):
        self._idx = x

    @property
    def idxk(self):
        return self._idxk

    @idxk.setter
    def idxk(self, x):
        self._idxk = x
