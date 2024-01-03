from pathlib import Path
import numpy as np
import re
import cv2
from typing import Union, List, Optional, Tuple
from dataclasses import dataclass, field

from .bbox import BBox, Point


@dataclass
class ImageManager:
    """Save all objects for each image"""

    _format = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
    _idx: int = 0
    paths: Optional[List[str]] = None  # image path list
    image: Optional[np.ndarray] = None  # image current
    bboxes: List[BBox] = field(default_factory=list)

    # bbox id which has been selected
    id_bbox_selected: Optional[int] = None
    id_bbox_bind_point_selected: Optional[int] = None

    # save deprecated
    deprecated_img_set: set = field(default_factory=set)

    # temp shape for drawing
    rect_temp: BBox = field(default_factory=BBox)
    point_temp: Point = field(default_factory=Point)

    # bboxes predictions
    # TODO :check if has boxes overlapped(one object has multi objects)
    bboxes_predicted: Optional[List] = None


    def bboxes_highly_overlappped(self) -> Optional[List]:
        pairs = []
        for i in range(len(self.bboxes) // 2 + 1):
            for j in range(i + 1, len(self.bboxes)):
                if self.bboxes[i].iou(self.bboxes[j]) > 0.85:
                    pairs.append((i, j))
        if len(pairs) == 0:
            pairs = None
        return pairs

    @property
    def path(self) -> str:
        # current image path
        if self.paths is None:
            raise ValueError("> Error: Paths is empty!")
        return self.paths[self._idx]

    @property
    def path_label(self):
        # corresponding label path
        return Path(self.path).with_suffix(".txt")

    def has_bbox_selected(self) -> bool:
        # check if any bbox has been selected
        return self.id_bbox_selected is not None

    def has_bbox_bind_to_point(self) -> bool:
        # check if any bbox has been bind to point
        return self.id_bbox_bind_point_selected is not None

    @property
    def count_bboxes(self):
        return len(self.bboxes)

    def last_bbox_selected(self):
        self.id_bbox_selected = (
            self.count_bboxes - 1
            if self.id_bbox_selected == 0
            else self.id_bbox_selected - 1
        )

    def next_bbox_selected(self):
        self.id_bbox_selected = (
            0
            if self.id_bbox_selected == self.count_bboxes - 1
            else self.id_bbox_selected + 1
        )

    def last(self):
        self.idx = 0 if self.idx - 1 < 0 else self.idx - 1

    def next(self):
        self.idx = self.count - 1 if self.idx + 1 > self.count - 1 else self.idx + 1

    def set_idx(self, x):
        self.idx = x

    @property
    def idx(self):
        return self._idx

    @idx.setter
    def idx(self, x):
        self._idx = x

        # try load image
        # self.image = cv2.imread(self.paths[self.idx])
        self.image = cv2.imdecode(np.fromfile(self.paths[self.idx], dtype=np.uint8), -1)
        if self.image is None:
            # create empty one
            self.image = np.ones((800, 600, 3))
            cv2.putText(
                self.image,
                "Deprecated image!",
                (10, self.image.shape[0] // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 0),
                thickness=2,
                lineType=cv2.LINE_AA,
            )

            # save wrong images path, delete all these image at the end of the program
            self.deprecated_img_set.add(self.paths[self.idx])

    def load(self, d):
        # load images from directory

        self.paths = [
            str(x) for x in Path(d).iterdir() if x.suffix.lower() in self._format
        ]
        self.paths.sort(key=self.natural_sort)

        if len(self.paths) < 1:
            raise ValueError(
                f"> No images found. Go checking the directory: {Path(d).resolve()}"
            )

    @staticmethod
    def natural_sort(x, _pattern=re.compile("([0-9]+)"), mixed=True):
        return [
            int(_x) if _x.isdigit() else _x
            for _x in _pattern.split(str(x) if mixed else x)
        ]

    @property
    def height(self) -> Union[int, float, None]:
        return None if self.image is None else self.image.shape[0]

    @property
    def width(self) -> Union[int, float, None]:
        return None if self.image is None else self.image.shape[1]

    @property
    def count(self):
        return len(self.paths)
