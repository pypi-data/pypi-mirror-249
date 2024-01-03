import cv2
from typing import Union
from dataclasses import dataclass

from .basics import Task, Mode
from .bbox import Point, BBox


@dataclass
class Cursor:
    x: Union[int, float] = -1
    y: Union[int, float] = -1

    def __repr__(self):
        return f"Cursor: (x={self.x}, y={self.y})"

    def draw_crossline(self, image, line_width, color):
        """cursor line for drawing rect"""
        cv2.line(
            image,
            (self.x, 0),
            (self.x, image.shape[0]),
            color,
            line_width,
        )
        cv2.line(
            image,
            (0, self.y),
            (image.shape[1], self.y),
            color,
            line_width,
        )


class Mouse:
    def __init__(self, marker):
        self.marker = marker
        self.cursor = Cursor()
        self.is_ldc_previous: bool = False  # left-button double click

    def listen(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            self.cursor.x = x
            self.cursor.y = y

        if self.marker.mode is Mode.DOODLE:
            if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
                cv2.circle(
                    self.marker.convas,
                    (x, y),
                    self.marker.line_thickness.now,
                    self.marker.color_doodle,
                    -1,
                )

        elif self.marker.mode is Mode.MARK:
            # MARK det mode
            if self.marker.task == Task.RECT:
                # left button double click -> select object
                if event == cv2.EVENT_LBUTTONDBLCLK:
                    self.is_ldc_previous = True
                    if self.marker.keyboard.auto_label:
                        self.marker.m_image.rect_temp = BBox()  # reset
                    else:
                        self.marker.m_image.rect_temp.tl = Point(-1, -1)  # reset

                    # if clicked inside a bounding box we set that bbox
                    # new: add support for polygon
                    self.marker.set_selected_object(set_cls_trackbar=True)


                # right button pressed down
                elif event == cv2.EVENT_RBUTTONDOWN:
                    self.marker.set_selected_object(
                        set_cls_trackbar=False
                    )  # cancel set class
                    if self.marker.m_image.has_bbox_selected():
                        self.marker.actions_to_selected_bbox(delete=True)
                        self.marker.m_image.id_bbox_selected = None

                # left button pressed down
                elif event == cv2.EVENT_LBUTTONDOWN:
                    if self.is_ldc_previous:  # cancel last double click
                        self.is_ldc_previous = False
                    else:  # Normal left click
                        # auto label
                        if self.marker.keyboard.auto_label:
                            # de-select
                            if self.marker.m_image.has_bbox_selected():
                                self.marker.m_image.id_bbox_selected = None
                            else:
                                # cache model prediction for the 1st time
                                # if self.marker.model.is_conf_update() or self.marker.m_image.bboxes_predicted is None:
                                if (
                                    self.marker.model.is_updated()
                                    or self.marker.m_image.bboxes_predicted is None
                                ):
                                    # no matter what, reset model status
                                    self.marker.model.reset_status()

                                    # predict by model
                                    self.marker.m_image.bboxes_predicted = (
                                        self.marker.model(
                                            self.marker.m_image.image
                                        ).tolist()
                                    )
                                    # sorted by area
                                    self.marker.m_image.bboxes_predicted.sort(
                                        key=lambda x: x[2] * x[3]
                                    )

                                # matching, find the bbox with min area
                                for (
                                    *box,
                                    score,
                                    id_,
                                ) in self.marker.m_image.bboxes_predicted:  # tlwh
                                    # box in cursor
                                    if (
                                        box[0] <= self.cursor.x <= box[0] + box[2]
                                        and box[1] <= self.cursor.y <= box[1] + box[3]
                                    ):
                                        self.marker.m_image.rect_temp = BBox(
                                            tl=Point(box[0], box[1]),
                                            br=Point(box[0] + box[2], box[1] + box[3]),
                                            id_=self.marker.m_cls.idx,
                                            kpts=None,
                                        )

                                        # check if already has one bbox here, change its class id
                                        for i_, b_ in enumerate(
                                            self.marker.m_image.bboxes
                                        ):
                                            if (
                                                self.marker.m_image.rect_temp.iou(b_)
                                                >= 0.97
                                            ):
                                                self.marker.m_image.id_bbox_selected = (
                                                    i_
                                                )
                                                if self.marker.m_image.has_bbox_selected():
                                                    self.marker.actions_to_selected_bbox(
                                                        change_id=True
                                                    )
                                                    self.marker.m_image.id_bbox_selected = None
                                                    self.marker.m_image.rect_temp = (
                                                        BBox()
                                                    )
                                        break
                                    else:
                                        self.marker.m_image.rect_temp = BBox()

                        else:  # label manully
                            if self.marker.m_image.rect_temp.tl.x == -1:
                                if self.marker.m_image.has_bbox_selected():
                                    self.marker.m_image.id_bbox_selected = None
                                else:  # first click
                                    self.marker.m_image.rect_temp.tl = Point(x, y)
                            else:  # second click
                                # minimal size for bounding box to avoid errors
                                if (
                                    abs(x - self.marker.m_image.rect_temp.tl.x)
                                    <= self.marker.min_side
                                    or abs(y - self.marker.m_image.rect_temp.tl.y)
                                    <= self.marker.min_side
                                ):
                                    self.marker.try_overlay_print(
                                        f"> bbox min side should be greater than: {self.marker.min_side}"
                                    )
                                else:
                                    self.marker.m_image.rect_temp.br = Point(x, y)

            # kpt task
            elif self.marker.task is Task.POINT:
                if event == cv2.EVENT_MOUSEMOVE:
                    self.cursor.x = x
                    self.cursor.y = y

                    # reset
                    self.marker.m_image.id_bbox_bind_point_selected = None
                    self.marker.bind_point_to_bbox()  # bind pt to bbox

                # right button pressed down
                elif event == cv2.EVENT_RBUTTONDOWN:
                    self.marker.find_and_delete_point()

                # left button pressed down
                elif event == cv2.EVENT_LBUTTONDOWN:
                    if self.is_ldc_previous:  # cancel last double click
                        self.is_ldc_previous = False
                    else:  # Normal left click
                        self.marker.m_image.point_temp = Point(
                            x=x, y=y, conf=1.0, id_=self.marker.m_cls._idxk
                        )
                        if self.marker.m_image.has_bbox_bind_to_point():
                            if (
                                self.marker.m_image.bboxes[
                                    self.marker.m_image.id_bbox_bind_point_selected
                                ].tl.x
                                <= self.cursor.x
                                <= self.marker.m_image.bboxes[
                                    self.marker.m_image.id_bbox_bind_point_selected
                                ].br.x
                                and self.marker.m_image.bboxes[
                                    self.marker.m_image.id_bbox_bind_point_selected
                                ].tl.y
                                <= self.cursor.y
                                <= self.marker.m_image.bboxes[
                                    self.marker.m_image.id_bbox_bind_point_selected
                                ].br.y
                            ):
                                # init when not exists
                                if (
                                    self.marker.m_image.bboxes[
                                        self.marker.m_image.id_bbox_bind_point_selected
                                    ].kpts
                                    is None
                                ):
                                    self.marker.m_image.bboxes[
                                        self.marker.m_image.id_bbox_bind_point_selected
                                    ].kpts = [Point] * self.marker.m_cls.count_kpts

                                # put current kpt into bbox binged
                                self.marker.m_image.bboxes[
                                    self.marker.m_image.id_bbox_bind_point_selected
                                ].kpts[
                                    self.marker.m_cls._idxk
                                ] = self.marker.m_image.point_temp

                                # kpts in bbox
                                kpts_ = self.marker.m_image.bboxes[
                                    self.marker.m_image.id_bbox_bind_point_selected
                                ].kpts
                                s_ = []
                                for kpt in kpts_:
                                    if kpt.x == -1:
                                        s_.extend([-1, -1, 0])
                                    else:
                                        s_.extend(
                                            [
                                                kpt.x / self.marker.m_image.width,
                                                kpt.y / self.marker.m_image.height,
                                                kpt.conf,
                                            ]
                                        )
                                line_kpt = " ".join(map(str, s_))

                                # find the label of bbox line need to modify
                                # load original label file
                                with open(
                                    self.marker.m_image.path_label, "r"
                                ) as f_original:
                                    lines_original = f_original.readlines()

                                # re-write label file
                                with open(self.marker.m_image.path_label, "w") as f:
                                    for idx, line in enumerate(lines_original):
                                        if (
                                            idx
                                            != self.marker.m_image.id_bbox_bind_point_selected
                                        ):  # nothing changed
                                            f.write(line)
                                        else:
                                            # id, x, y, w, h,
                                            line_new = (
                                                " ".join(line.strip().split(" ")[:5])
                                                + " "
                                                + line_kpt
                                                + "\n"
                                            )
                                            f.write(line_new)

                                # reset
                                self.marker.m_image.id_bbox_bind_point_selected = None

            elif self.marker.task is Task.POLYGON:
                if event == cv2.EVENT_LBUTTONDBLCLK:
                    self.is_ldc_previous = True
                    self.marker.set_selected_object(set_cls_trackbar=True)

                elif event == cv2.EVENT_RBUTTONDOWN:

                    # TODO:
                    self.marker.set_selected_object(
                        set_cls_trackbar=False
                    )  # cancel set class 
                    if self.marker.m_image.has_bbox_selected():
                        self.marker.actions_to_selected_bbox(delete=True)
                        self.marker.m_image.id_bbox_selected = None
                elif event == cv2.EVENT_LBUTTONDOWN:
                    if self.is_ldc_previous:  # cancel last double click
                        self.is_ldc_previous = False
                    else:  # Normal left click
                        if self.marker.m_image.has_bbox_selected():
                            self.marker.m_image.id_bbox_selected = None

                        # auto label
                        if self.marker.keyboard.auto_label:
                            pass
                            self.marker.try_overlay_print("Not supported for now!")
                        else:  # label manully
                            self.marker.try_overlay_print("Not supported for now!")


        else:
            pass
