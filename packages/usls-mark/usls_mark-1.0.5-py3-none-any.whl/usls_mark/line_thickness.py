import numpy as np
from typing import Optional
from dataclasses import dataclass


@dataclass
class LineThickness:
    now: Optional[int] = None
    recommend: Optional[int] = None
    last: Optional[int] = None
    toggle: bool = False

    def auto_fit(self, image: Optional[np.ndarray] = None):
        # generate recommended value
        if self.now is None:
            self.now = 1 if image is None else self.width_recommended(image)
            self.last = self.recommend = self.now

        # toggle
        if self.now != 1:
            self.last = self.now
        self.now = 1 if self.toggle else self.last

    def increase(self, delta=1):
        if self.now < self.recommend + 10:
            self.now += delta
            self.last = self.now

    def decrease(self, delta=1):
        if self.now > 1:
            self.now -= delta
            self.last = self.now

    def width_recommended(self, image: np.ndarray):
        return max(round(sum(image.shape) / 2 * 0.003), 2)
