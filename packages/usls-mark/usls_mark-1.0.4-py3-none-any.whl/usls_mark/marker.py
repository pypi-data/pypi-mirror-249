import os
import cv2
import numpy as np
from pathlib import Path
import shutil
import random
import uuid
from datetime import datetime
from typing import Optional

from .model import Model
from .basics import Task, Mode
from .result import Option
from .bbox import BBox, Point
from .image_manager import ImageManager
from .class_manager import ClassesManager
from .palette import Palette
from .keyboard import KeyBoard
from .mouse import Mouse
from .line_thickness import LineThickness


class MarkerApp:
    def __init__(
        self,
        dir_image,
        classes,
        classes_kpts=None,
        model=None,
        use_gpu=False,
        min_side=5,
        summary=False,
        verbose=False,
    ):
        # mode & task
        self.min_side = min_side
        self.mode = Mode.READ
        self.task = Task.RECT

        # doodle canavs
        self.convas: Optional[np.ndarray] = None

        # image manager
        self.dir_image = dir_image
        self.m_image = ImageManager()
        self.m_image.load(self.dir_image)
        self.m_image.idx = 0

        # class manager
        self.m_cls = ClassesManager()
        self.m_cls.parse(classes or [self.dir_image])
        self.m_cls.parse_kpts(classes_kpts)


        # datasets summary
        if summary:
            self.summary(verbose)

        # kits
        self.line_thickness = LineThickness()
        self.palette = Palette()
        self.keyboard = KeyBoard(self)
        self.mouse = Mouse(self)

        # build UI
        self.with_qt = self.window_init()
        self.window_name = "usls image marker"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, 800, 800)

        # mode trackbar
        self.trackbar_mode = self.build_trackbar(
            window=self.window_name,
            name=f"Modes: {[x.name for x in Mode]}",
            count=len(Mode),
        ).unwrap()

        # task trackbar
        self.trackbar_task = self.build_trackbar(
            window=self.window_name,
            name=f"Tasks: {[x.name for x in Task]}",
            count=len(Task),
        ).unwrap()

        # class trackbar
        self.trackbar_class = self.build_trackbar(
            window=self.window_name,
            name=f"Classes: {self.m_cls.names}",
            count=self.m_cls.count,
        ).unwrap()

        # kpts class trackbar
        self.trackbar_kpt_class = self.build_trackbar(
            window=self.window_name,
            name=f"Classes Keypoints: {self.m_cls.names_kpts}",
            count=self.m_cls.count_kpts,
        ).unwrap()

        # images trackbar
        self.trackbar_image = self.build_trackbar(
            window=self.window_name,
            name="Images",
            count=self.m_image.count,
            fn=lambda x: self.m_image.set_idx(x),
        ).unwrap()

        # set mouse callback
        cv2.setMouseCallback(self.window_name, self.mouse.listen)

        # build nn model
        if model is None:
            self.model = None
        elif isinstance(model, str):
            # build model
            self.model = Model(
                f=model,
                use_gpu=use_gpu,
            )

            if self.model.task is NotImplemented:
                raise NotImplementedError('Model type not supported! Try using yolov8 serial models.')
            elif self.model.task is Task.RECT:
                # build conf trackbar
                _conf_max = 100
                self.trackbar_conf = self.build_trackbar(
                    window=self.window_name,
                    name="Confidence: 0.",
                    initial=int(self.model.t_conf * _conf_max),
                    count=_conf_max,
                    fn=lambda x: self.model.set_conf(x / _conf_max),
                ).unwrap()

                # build nc trackbar
                self.trackbar_conf = self.build_trackbar(
                    window=self.window_name,
                    name="Pre-trained class focused on(The max means all included)",
                    initial=self.model.nc + 1,
                    count=self.model.nc + 1,
                    fn=lambda x: self.model.set_class(x),
                ).unwrap()

            elif self.model.task is Task.POLYGON:
                raise NotImplementedError('Segments model is not supported for now. Please wait.')
            else:
                raise NotImplementedError('Model is not supported. Try yolov8 detect model.')



    def mainloop(self):
        while True:
            # update
            img_c = self.m_image.image.copy()
            color = self.palette(int(self.m_cls.idx))
            self.line_thickness.auto_fit(img_c)
            img_c = self.blink_or_not(img_c)

            # TODO
            pairs = self.m_image.bboxes_highly_overlappped()
            if pairs is not None:
                self.try_overlay_print(
                    "> Bboxes highly overlappped"
                )
            # if not self.keyboard.is_blinking:
            #     pairs = self.m_image.bboxes_highly_overlappped()
            #     if pairs is not None:
            #         self.keyboard.is_blinking = True
            #         self.try_overlay_print(
            #             "> Bboxes highly overlappped"
            #         )
            #     else:
            #         self.keyboard.is_blinking = False

            # statusbar info
            if self.with_qt:
                _s = (
                    f"{self.mouse.cursor}"
                    + "\t" * 5
                    + f"Num_objects: {str(len(self.m_image.bboxes))}"
                    + "\t" * 8
                    + f"Resolution: ({self.m_image.height}, {self.m_image.width})"
                    + "\t" * 8
                    + f"Path: {self.m_image.path}"
                    + "\t" * 8
                    + f"Bboxes_highly_overlappped: {pairs}"
                )

                # load model class name when using model
                if self.model is not None:
                    _ss = f"Class focused on: => {self.model.specific_class_name()}"
                    # if self.model.is_class_updated():
                    #     self.try_overlay_print(_ss)
                    _s += "\t" * 5 + _ss
                cv2.displayStatusBar(self.window_name, _s)

            # marking
            if self.mode is Mode.MARK:
                # cursor text
                img_c = self.hide_text_or_not(img_c, color)

                # enable object select
                img_c = self.highlight_selected_or_not(img_c)

                # mark manully
                if not self.keyboard.auto_label:
                    if self.task is Task.RECT:
                        self.mouse.cursor.draw_crossline(
                            img_c,
                            self.line_thickness.now,
                            color,
                        )

                        # drawing
                        if self.m_image.rect_temp.tl.x != -1:
                            # the 1st point
                            cv2.rectangle(
                                img_c,
                                (
                                    self.m_image.rect_temp.tl.x,
                                    self.m_image.rect_temp.tl.y,
                                ),
                                (self.mouse.cursor.x, self.mouse.cursor.y),
                                color,
                                self.line_thickness.now,
                            )

                            # the 2nd point
                            if self.m_image.rect_temp.br.x != -1:
                                line = (
                                    f"{self.m_cls.idx} "
                                    + self.m_image.rect_temp.str_cxcywhn(
                                        self.m_image.width, self.m_image.height
                                    )
                                )
                                # save label and reset
                                self.save_label_det(line)
                                self.m_image.rect_temp = BBox()

                    else:
                        # Note that:
                        # Point drawing in mouse.py
                        # Polygon no support manully mark for now
                        cv2.circle(
                            img_c,
                            (self.mouse.cursor.x, self.mouse.cursor.y),
                            int(self.line_thickness.now * 2),
                            color,
                            -1,
                            cv2.LINE_AA,
                        )
                else:  # auto label with yolo
                    # indicater
                    cv2.circle(
                        img_c,
                        (self.mouse.cursor.x, self.mouse.cursor.y),
                        int(self.line_thickness.now * 2),
                        color,
                        -1,
                        cv2.LINE_AA,
                    )

                    if self.task is Task.RECT:
                        # drawing
                        if self.m_image.rect_temp.br.x != -1:
                            # TODO: if already has one bbox here, remove last one

                            # save label and reset
                            line = (
                                f"{self.m_cls.idx} "
                                + self.m_image.rect_temp.str_cxcywhn(
                                    self.m_image.width, self.m_image.height
                                )
                            )
                            self.save_label_det(line)
                            self.m_image.rect_temp = BBox()
                    
                    elif self.task is Task.POLYGON:
                        # TODO: drawing
                        pass

            elif self.mode is Mode.DOODLE:
                if self.convas is None:
                    self.convas = self.m_image.image.copy()
                self.color_doodle = color
                img_c = self.convas
            else:  # read
                pass

            cv2.imshow(self.window_name, img_c)
            self.keyboard.listen()

            # ESC to quit
            if self.keyboard.quit:
                break

            # mouse click to quit
            if cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1:
                break

        cv2.destroyAllWindows()

        # deal with wrong images which can not be read by opencv
        if len(self.m_image.deprecated_img_set) > 0:
            print(
                f"> Warning: {len(self.m_image.deprecated_img_set)} images can not be decode."
            )

            # create dir
            self.dir_deprecated = "images-deprecated"
            self.dir_deprecated = self.smart_path(
                Path(self.dir_deprecated), exist_ok=False, sep="-"
            )  # increment run
            self.dir_deprecated.mkdir(
                parents=True, exist_ok=True
            )  # make dir for every page

            # move
            for img in self.m_image.deprecated_img_set:
                shutil.move(img, str(self.dir_deprecated))
            print(f"> Deprecated images saved at: {self.dir_deprecated}")

    def draw_objects_label_text(
        self,
        *,
        img,
        label,
        line_thickness,
        x,
        y,
        color,
        font=cv2.FONT_HERSHEY_SIMPLEX,
        lineType=cv2.LINE_AA,
    ):
        # get text width, height
        text_w, text_h = cv2.getTextSize(
            label,
            0,
            fontScale=line_thickness / 3,
            thickness=max(line_thickness - 1, 1),
        )[0]

        # check if label is outside of image
        outside = y - text_h - 3 >= 0
        delta = 3
        cv2.putText(
            img,
            label,
            (x, y - delta if outside else y + text_h + delta),
            font,
            line_thickness / 3,
            color=color,
            thickness=int(line_thickness * 0.7),
            lineType=cv2.LINE_AA,
        )
        return img


    def check_mark_task(self, line: list) -> Task:
        # check one line type
        # RECT: cls, cx, cy, w, h  (1 + 4)
        # POINT: cls, cx, cy, w, h, k1x, k1y, k1conf, ..., knx, kny, knconf  (1 + 4 + 3*n)
        # POINT: cls, k1x, k1y, ..., knx, kny (1 + 2*n)
        # =>>>> 5 + 3*x = 1 + 2*y
        # =>>>> collision happens a lot! 65
        n = len(line)
        if 0 < n < 5:
            return NotImplemented
        elif n == 5:
            return Task.RECT
        elif self.m_cls.count_kpts > 0 and n == (self.m_cls.count_kpts * 3 + 5):
            return Task.RECT
        elif (n - 1) % 2 == 0: # and self.task is not Task.POLYGON:
            return Task.POLYGON


    def draw_from_file(
        self,
        *,
        img,
        line_thickness,
        # ids_included: List,
    ):
        height, width = img.shape[:2]
        self.m_image.bboxes.clear()

        # Drawing bounding boxes from the files
        if Path(self.m_image.path_label).exists():
            with open(self.m_image.path_label, "r") as f:
                for idx, line in enumerate(f):
                    line_c = line.strip().split()
                    if len(line_c) == 0:
                        continue

                    # treat each line as an object, get it's task type
                    task_ = self.check_mark_task(line_c)

                    if task_ is NotImplemented:
                        self.try_overlay_print(f'Error: Label format is wrong, length < 5.')
                        print(f'> Unsupported label format path: {path}')
                        continue

                    # Task.RECT, Task.POINT
                    if task_ in (Task.RECT, Task.POINT):
                        cls_id, cx, cy, box_w, box_h, *kpts_list = line_c
                        box_w, box_h, cx, cy = map(float, (box_w, box_h, cx, cy))
                        cls_id = int(cls_id)
                        cls_name = self.m_cls.names[cls_id]

                        # coords
                        w = width * box_w
                        h = height * box_h
                        xmin = int(width * cx - w / 2.0)
                        xmax = int(width * cx + w / 2.0)
                        ymin = int(height * cy - h / 2.0)
                        ymax = int(height * cy + h / 2.0)

                        color = self.palette(cls_id)

                        # kpts
                        kpts_ = [Point] * self.m_cls.count_kpts
                        if len(kpts_list) > 0:
                            step = len(kpts_list) // self.m_cls.count_kpts
                            assert (
                                step == 3
                            ), "> Error: keypoint format must be like: x, y, visible(0|1)"
                            for id_, i in enumerate(range(0, len(kpts_list), step)):
                                x_, y_ = kpts_list[i], kpts_list[i + 1]

                                # continue when has no kpt
                                if x_ == "-1" and y_ == "-1":
                                    continue

                                x_, y_, visiable = (
                                    float(x_),
                                    float(y_),
                                    float(kpts_list[i + 2]),
                                )
                                x_ *= width
                                y_ *= height

                                # save
                                kpts_[id_] = Point(
                                    x=x_,
                                    y=y_,
                                    id_=id_,
                                    conf=visiable,
                                )

                                # draw
                                cv2.circle(
                                    img,
                                    (int(x_), int(y_)),
                                    line_thickness * 2,
                                    color,
                                    -1,
                                    cv2.LINE_AA,
                                )

                                # Display Label if has label txt
                                if not self.keyboard.is_hiding_text:
                                    img = self.draw_objects_label_text(
                                        img=img,
                                        label=self.m_cls.names_kpts[id_],
                                        line_thickness=line_thickness,
                                        x=int(x_),
                                        y=int(y_),
                                        color=color,
                                    )

                        # save to memory
                        self.m_image.bboxes.append(
                            BBox(
                                tl=Point(xmin, ymin),
                                br=Point(xmax, ymax),
                                id_=cls_id,
                                kpts=kpts_ if len(kpts_) > 0 else None,
                            )
                        )

                        # show single class
                        if self.keyboard.single_clsidx4showing is not None:
                            if cls_id != self.keyboard.single_clsidx4showing:
                                continue

                        # draw bbox
                        cv2.rectangle(
                            img,
                            (xmin, ymin),
                            (xmax, ymax),
                            color,
                            line_thickness,
                            cv2.LINE_AA,
                        )

                        # Display Label if has label txt
                        if not self.keyboard.is_hiding_text:
                            img = self.draw_objects_label_text(
                                img=img,
                                label=cls_name,
                                line_thickness=line_thickness,
                                x=xmin,
                                y=ymin,
                                color=color,
                            )

                    elif task_ is Task.POLYGON:
                        cls_id, *kpts_list = line_c
                        cls_id = int(cls_id)
                        cls_name = self.m_cls.names[cls_id]

                        xys_, xys = [], []
                        for id_, i in enumerate(range(0, len(kpts_list), 2)):
                                x_ = float(kpts_list[i]) * width
                                y_ = float(kpts_list[i + 1]) * height

                                # xy de-scaled
                                xys_.append([x_, y_])
                                xys.append(
                                    Point(
                                        x=x_,
                                        y=y_,
                                        id_=cls_id,
                                        conf=1.0,
                                    )
                                )

                        # segments -> bbox
                        xys_ = np.asarray(xys_, dtype=np.single)
                        xmin = np.amin(xys_[:, 0], axis=-1)
                        ymin = np.amin(xys_[:, 1], axis=-1)
                        xmax = np.amax(xys_[:, 0], axis=-1)
                        ymax = np.amax(xys_[:, 1], axis=-1)

                        # save to memory
                        self.m_image.bboxes.append(
                            BBox(
                                tl=Point(xmin, ymin),
                                br=Point(xmax, ymax),
                                id_=cls_id,
                                segments=xys_
                            )
                        )

                        # draw
                        color = self.palette(cls_id)
                        cv2.polylines(img, np.int32([xys_]), True, color, line_thickness)
                        # cv2.fillPoly(im_canvas, np.int32([segment]), self.color_palette(int(cls_), bgr=True))
                        
                        # optional
                        # cv2.rectangle(img, (int(xmin), int(ymin)), (int(xmax), int(ymax)),
                        #               color, line_thickness, cv2.LINE_AA)
              
                        # Display Label if has label txt
                        if not self.keyboard.is_hiding_text:
                            img = self.draw_objects_label_text(
                                img=img,
                                label=self.m_cls.names[cls_id],
                                line_thickness=line_thickness,
                                x=int(xmin),
                                y=int(ymin),
                                color=color,
                            )

        return img



    def bind_point_to_bbox(self):
        smallest_area = -1
        for idx, bbox in enumerate(self.m_image.bboxes):
            # check if cursor is in bbox
            if (
                bbox.tl.x <= self.mouse.cursor.x <= bbox.br.x
                and bbox.tl.y <= self.mouse.cursor.y <= bbox.br.y
            ):
                # find smaller bbox
                if bbox.area < smallest_area or smallest_area == -1:
                    smallest_area = bbox.area
                    self.m_image.id_bbox_bind_point_selected = idx

    # TODO:
    def find_and_delete_point(self):
        # find out the point which cursor on and delete it

        idx_ = -1  # the bbox cursor is in
        smallest_area = -1
        for idx, bbox in enumerate(self.m_image.bboxes):
            # check if cursor is in bbox
            if (
                bbox.tl.x <= self.mouse.cursor.x <= bbox.br.x
                and bbox.tl.y <= self.mouse.cursor.y <= bbox.br.y
            ):
                # find smaller bbox
                if bbox.area < smallest_area or smallest_area == -1:
                    smallest_area = bbox.area
                    idx_ = idx

        for i, kpt in enumerate(self.m_image.bboxes[idx_].kpts):
            if kpt == Point():
                continue

            _delta = 10
            if (
                kpt.x - _delta <= self.mouse.cursor.x <= kpt.x + _delta
                and kpt.y - _delta <= self.mouse.cursor.y <= kpt.y + _delta
            ):
                # find the kpt
                self.m_image.bboxes[idx_].kpts[i] = Point()  # delete from mem
                kpts_ = self.m_image.bboxes[
                    self.m_image.id_bbox_bind_point_selected
                ].kpts
                s_ = []
                for kpt in kpts_:
                    if kpt.x == -1:
                        s_.extend([-1, -1, 0])
                    else:
                        s_.extend(
                            [
                                kpt.x / self.m_image.width,
                                kpt.y / self.m_image.height,
                                kpt.conf,
                            ]
                        )
                line_kpt = " ".join(map(str, s_))

                # load original label file
                with open(self.m_image.path_label, "r") as f_original:
                    lines_original = f_original.readlines()

                # # re-write label file
                with open(self.m_image.path_label, "w") as f:
                    for idx, line in enumerate(lines_original):
                        if idx != idx_:  # nothing changed
                            f.write(line)
                        else:
                            line_new = (
                                " ".join(line.strip().split(" ")[:5])
                                + " "
                                + line_kpt
                                + "\n"
                            )
                            f.write(line_new)


    def set_selected_object(self, set_cls_trackbar=True):
        # support bbox and polygon
        smallest_area = -1
        for idx, bbox in enumerate(self.m_image.bboxes):
            # check if cursor is in bbox
            if (
                bbox.tl.x <= self.mouse.cursor.x <= bbox.br.x
                and bbox.tl.y <= self.mouse.cursor.y <= bbox.br.y
            ): 
                # polygon is always smaller than bbox
                if bbox.segments is not None:
                    if cv2.pointPolygonTest(
                        bbox.segments, (self.mouse.cursor.x, self.mouse.cursor.y), False
                    ) >= 0:
                        area = cv2.contourArea(bbox.segments)
                    else:
                        continue
                else:
                    area = bbox.area

                # find smaller one
                if area < smallest_area or smallest_area == -1:
                    smallest_area = area
                    self.m_image.id_bbox_selected = idx
                    self.m_cls.idx = bbox.id_

                    # set class trackbar position
                    if set_cls_trackbar:
                        cv2.setTrackbarPos(
                            self.trackbar_class, self.window_name, bbox.id_
                        )


    def actions_to_selected_bbox(self, *, delete=False, change_id=False):
        # load initial label file
        with open(self.m_image.path_label, "r") as f_original:
            lines_original = f_original.readlines()

        # re-write label file
        with open(self.m_image.path_label, "w") as f:
            for idx, line in enumerate(lines_original):
                if idx != self.m_image.id_bbox_selected:  # nothing changed
                    f.write(line)
                elif change_id is True:  # re-write
                    line_new = str(self.m_cls.idx) + ' ' + ' '.join(line.strip().split(' ')[1:]) + '\n'
                    f.write(line_new)
                elif delete is True:  # skip
                    continue
                else:
                    pass

    def window_init(self) -> bool:
        try:
            cv2.namedWindow("Test")
            cv2.displayOverlay("Test", "Test", 1)
            cv2.displayStatusBar("Test", "Test", 1)
            with_qt = True
        except cv2.error as _:
            with_qt = False
        cv2.destroyAllWindows()
        return with_qt

    @staticmethod
    def build_trackbar(
        window: str, name: str, count: int, initial=0, fn=lambda _x: _x
    ) -> Option:
        """Build trackbar"""
        if count > 1:
            cv2.createTrackbar(
                name,
                window,
                initial,
                count - 1,
                fn,
            )
        else:
            print(f"> The {name} trackbar failed to create because of the length.")

        return Option(name)

    def hide_text_or_not(self, img, color):
        if not self.keyboard.is_hiding_text:
            img = self.draw_objects_label_text(
                img=img,
                label=self.m_cls.names[self.m_cls.idx]
                if self.task in (Task.RECT, Task.POLYGON)
                else self.m_cls.names_kpts[self.m_cls.idxk],
                line_thickness=self.line_thickness.now,
                x=self.mouse.cursor.x,
                y=self.mouse.cursor.y,
                color=color,
            )
        return img

    def blink_or_not(self, img):
        # Blink bboxes
        if self.keyboard.is_blinking:
            img = self.draw_from_file(
                img=img,
                line_thickness=0
                if self.keyboard.blinking_switcher
                else self.line_thickness.now,
                # ids_included=ids_included,
            )
            self.keyboard.blinking_switcher = not self.keyboard.blinking_switcher
        else:
            img = self.draw_from_file(
                img=img,
                line_thickness=self.line_thickness.now,
                # ids_included=ids_included,
            )
        return img

    def highlight_selected_or_not(self, img):
        if self.m_image.has_bbox_selected():
            _bbox = self.m_image.bboxes[self.m_image.id_bbox_selected]

            mask_highlight = np.zeros((img.shape), dtype=np.uint8)
            _lw = self.line_thickness.now // 2  # border

            if _bbox.segments is not None:
                cv2.fillPoly(mask_highlight, np.int32([_bbox.segments]), (255, 255, 255, 0))

            else:
                cv2.rectangle(
                    mask_highlight,
                    (_bbox.tl.x - _lw, _bbox.tl.y - _lw),
                    (_bbox.br.x + _lw, _bbox.br.y + _lw),
                    (255, 255, 255, 0),
                    -1,
                    cv2.LINE_AA,
                )
            img = cv2.addWeighted(img, 1, mask_highlight, 0.5, 0)
        return img

    # def highlight_selected_or_not(self, img, segments=False):
    #     if self.m_image.has_bbox_selected():
    #         _bbox = self.m_image.bboxes[self.m_image.id_bbox_selected]

    #         mask_highlight = np.zeros((img.shape), dtype=np.uint8)
    #         _lw = self.line_thickness.now // 2  # border

    #         if segments:
    #             cv2.fillPoly(mask_highlight, np.int32([_bbox.segments]), (255, 255, 255, 0))

    #         else:
    #             cv2.rectangle(
    #                 mask_highlight,
    #                 (_bbox.tl.x - _lw, _bbox.tl.y - _lw),
    #                 (_bbox.br.x + _lw, _bbox.br.y + _lw),
    #                 (255, 255, 255, 0),
    #                 -1,
    #                 cv2.LINE_AA,
    #             )
    #         img = cv2.addWeighted(img, 1, mask_highlight, 0.5, 0)
    #     return img

    def save_label_det(self, line):
        with open(self.m_image.path_label, "a") as f:
            if os.path.getsize(self.m_image.path_label) == 0:
                f.write(line)
            else:
                f_r = open(self.m_image.path_label, "r").read()
                if f_r[-1] == "\n":
                    msg = line
                else:
                    msg = "\n" + line
                f.write(msg)

    def display_path_when_no_qt(self, img):
        # deprecated
        if self.keyboard.is_showing_path:
            msg = f"{self.m_image.path}"

            # get text width, height
            text_w, text_h = cv2.getTextSize(
                msg,
                0,
                fontScale=self.line_thickness.now / 4,
                thickness=max(self.line_thickness.now - 1, 1),
            )[0]

            text_x, text_y = (
                self.m_image.image.shape[1] // 20,
                self.m_image.image.shape[0] // 10,
            )
            _dealt = 10
            cv2.rectangle(
                img,
                (max(0, text_x - _dealt), max(0, text_y - text_h - _dealt)),
                (
                    min(text_x + text_w + _dealt, img.shape[1]),
                    min(text_y + _dealt, img.shape[0]),
                ),
                (0, 0, 0),
                -1,
                cv2.LINE_AA,
            )
            cv2.putText(
                img,
                msg,
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                self.line_thickness.now / 4,
                (255, 255, 255),
                thickness=int(self.line_thickness.now * 0.7),
                lineType=cv2.LINE_AA,
            )
        return img

    @staticmethod
    def smart_path(path="", *, exist_ok=False, sep="-", mkdir=False, method=0):
        # Increment file or directory path

        # random string in currnet path
        if path == "":
            if method == 0:
                _ASCII_LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                path = Path.cwd() / ("".join(random.choices(_ASCII_LETTERS, k=8)))
            elif method == 1:
                path = Path.cwd() / str(uuid.uuid4())
            elif method == 2:
                path = Path.cwd() / datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        path = Path(path)  # os-agnostic

        # make increment
        if path.exists() and not exist_ok:
            path, suffix = (
                (path.with_suffix(""), path.suffix) if path.is_file() else (path, "")
            )

            # increment path
            for n in range(2, 9999):
                p = f"{path}{sep}{n}{suffix}"
                if not os.path.exists(p):  # non-exist will break
                    break
            path = Path(p)

        # make dir directly
        if mkdir:
            path.mkdir(parents=True, exist_ok=True)  # make directory

        return path

    def try_overlay(self, msg, ms=1000) -> Option:
        """print to overlay when enable"""
        ret = True
        if self.with_qt:
            cv2.displayOverlay(
                self.window_name,
                msg,
                ms,
            )
        else:
            ret = False
        return Option(ret)

    def try_overlay_print(self, msg, ms=1000):
        """print to overlay or to terminal"""
        self.try_overlay(msg, ms).unwrap_or(lambda x: print)

    def build_model(self):
        if self.model is None:
            self.try_overlay_print(
                "> Try `--model <YOLOv8-ONNX-model>` to use auto label."
            )
        elif isinstance(self.model, str):
            self.model = Model(
                f=self.model,
                conf=self.conf,
                use_gpu=self.use_gpu,
            )

    def summary(self, verbose=False):
        # labels
        p_labels, p_labels_empty = [], []
        cls_inst = {}

        for p in Path(self.dir_image).rglob("*.txt"):
            is_empty = True
            bboxes: List[BBox] = []
            with open(p, "r") as f:
                for line in f:
                    line = line.strip().split(" ")
                    if len(line) == 1 and line[0] == "":
                        continue
                    is_empty = False
                    _class = line[0]
                    _class = self.m_cls.names[int(_class)]
                    if self.task is Task.RECT:
                        _ = cls_inst.setdefault(_class, 0)
                        cls_inst[_class] += 1
                    else:
                        raise NotImplementedError("TODO")
            if is_empty:
                p_labels_empty.append(p)
            else:
                p_labels.append(p)

        # images which has no label file
        num_images_has_no_lable = []
        for image in self.m_image.paths:
            if not Path(image).with_suffix(".txt").exists():
                num_images_has_no_lable.append(Path(image))

        # summary
        print(
            f"\nsummary:\n"
            + f"> Found {len(self.m_image.paths)} images"
            + f"({len(num_images_has_no_lable)} has no label)\n"
            + f"> Found {len(p_labels)} labels"
            + f"({len(p_labels_empty)} empty)\n"
            + f"> Found {sum(v for v in cls_inst.values())} instances({cls_inst})"
        )

        if verbose:
            if len(num_images_has_no_lable) > 0:
                saveout = 'list_images_no_label.txt'
                print(f"\n> List of images which has no label file saved at: {saveout}")
                with open(saveout, 'w+') as f:
                    f.write("> Images which has no label file:\n")
                    for x in num_images_has_no_lable:
                        f.write(str(x) + '\n')

            if len(p_labels_empty) > 0:
                saveout = 'list_empty_label.txt'
                print("\n> List of labels which is empty saved at: {saveout}")
                with open(saveout, 'w+') as f:
                    f.write("> Labels which is empty:\n")
                    for x in p_labels_empty:
                        f.write(str(x) + '\n')
