from typing import Union, List, Optional
from dataclasses import dataclass, field


@dataclass
class Point:
    x: Union[int, float] = -1
    y: Union[int, float] = -1
    z: Union[int, float] = -1
    conf: Optional[float] = None
    id_: Optional[int] = None


@dataclass
class BBox:
    tl: Point = field(default_factory=Point)  # top-left
    br: Point = field(default_factory=Point)  # bottom-right
    id_: Optional[int] = None  # class id
    conf_: Union[int, float, None] = None  # confidence
    cxcy: Point = field(default_factory=Point)  # center
    kpts: Optional[List[Point]] = None  # kpts bind to bbox

    # objects contour in current images
    segments: Optional[List[List[float]]] = None
    # segments: Optional[List[Point]] = None



    @property
    def xmin(self) -> int:
        return int(self.tl.x)

    @property
    def xmax(self) -> int:
        return int(self.br.x)

    @property
    def ymin(self) -> int:
        return int(self.tl.y)

    @property
    def ymax(self) -> int:
        return int(self.br.y)

    @property
    def id(self):
        return self.id_

    @id.setter
    def id(self, x):
        self.id_ = x

    @property
    def conf(self):
        return self.conf

    @conf.setter
    def conf(self, x):
        self.conf_ = x

    @property
    def height(self) -> int:
        return self.ymax - self.ymin

    @property
    def width(self) -> int:
        return self.xmax - self.xmin

    @property
    def area(self) -> int:
        return (self.ymax - self.ymin) * (self.xmax - self.xmin)

    def intersect(self, other) -> int:
        x_ = min(self.xmax, other.xmax) - max(self.xmin, other.xmin)
        y_ = min(self.ymax, other.ymax) - max(self.ymin, other.ymin)
        if any((x_ < 0, y_ < 0)):
            return 0
        else:
            return x_ * y_

    def iou(self, other) -> float:
        intersect = self.intersect(other)
        if intersect == 0:
            return intersect
        else:
            return intersect / (self.area + other.area - intersect)

    def str_cxcywhn(self, img_w, img_h, eps=1e-8):
        # return str of cxcywh normalized

        # boundary check and rectify
        self.tl.x = min(max(eps, self.tl.x), img_w - eps)
        self.br.x = min(max(eps, self.br.x), img_w - eps)
        self.tl.y = min(max(eps, self.tl.y), img_h - eps)
        self.br.y = min(max(eps, self.br.y), img_h - eps)

        # convert
        cx = float((self.tl.x + self.br.x) / (2.0 * img_w))
        cy = float((self.tl.y + self.br.y) / (2.0 * img_h))
        w = float(abs(self.br.x - self.tl.x)) / img_w
        h = float(abs(self.br.y - self.tl.y)) / img_h

        # double check of boundary
        if not all([0 <= x <= 1 for x in [cx, cy, w, h]]):
            raise ValueError(
                f"Wrong coordination -> cx: {cx}, cy: {cy}, w: {w}, h: {h}."
            )

        items = map(str, [cx, cy, w, h])
        return " ".join(items)
