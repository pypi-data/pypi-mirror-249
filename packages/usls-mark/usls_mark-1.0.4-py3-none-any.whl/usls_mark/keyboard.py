import cv2
from pathlib import Path
from typing import Optional
import rich

from .model import Model
from .basics import Task, Mode
from .palette import Palette
from . import __usage__


class KeyBoard:
    def __init__(self, marker):
        self.marker = marker
        # flags
        self.quit: bool = False
        self.is_hiding_text: bool = False
        self.single_clsidx4showing: Optional[int] = None
        self.is_blinking: bool = False
        self.blinking_switcher: bool = False

        # auto label
        self.auto_label = False

    def listen(self, delay=1):

        _key = cv2.waitKey(delay)
        # usage
        if _key in (ord("h"), ord("H")):
            rich.print(__usage__)

        # auto label with model
        if _key in (ord("f"), ord("F")):
            if isinstance(self.marker.model, Model):
                self.auto_label = not self.auto_label
            else:
                self.marker.try_overlay_print(
                    "> Try `--model <YOLOv8-ONNX-model>` to use auto label.", ms=2000
                )

        # task switching
        elif _key in (33, 64, 35):
            if self.marker.mode is Mode.MARK:
                # shift + 1 => mark rect
                if _key == 33:
                    self.marker.task = Task.RECT
                    cv2.setTrackbarPos(
                        self.marker.trackbar_task,
                        self.marker.window_name,
                        self.marker.task.value,
                    )
                    self.marker.try_overlay_print("> Marking rectangle...")
                # shift + 2 => mark point
                elif _key == 64:
                    if self.marker.m_cls.count_kpts <= 0:
                        self.marker.task = Task.RECT
                        self.marker.try_overlay_print(
                            "> Warning: No `-kc` named, can not switch to `Task.POINT`"
                        )
                    else:
                        self.marker.task = Task.POINT
                        cv2.setTrackbarPos(
                            self.marker.trackbar_task,
                            self.marker.window_name,
                            self.marker.task.value,
                        )
                        self.marker.try_overlay_print("> Marking point...")

                # shift + 3 => mark polygon
                else:
                    self.marker.task = Task.POLYGON
                    cv2.setTrackbarPos(
                        self.marker.trackbar_task,
                        self.marker.window_name,
                        self.marker.task.value,
                    )
                    self.marker.try_overlay_print("> Marking polygon...")

            else:
                self.marker.try_overlay_print(
                    "> Warning: task switching should under MARK mode."
                )

        # DOODLE <-> READ
        elif _key in (ord("e"), ord("E")):
            if self.marker.mode is Mode.READ:
                self.marker.mode = Mode.DOODLE
                self.marker.try_overlay_print("> Mode -> DOODLE", ms=900)
            elif self.marker.mode is Mode.DOODLE:
                self.marker.mode = Mode.READ
                self.marker.convas = None
                self.marker.try_overlay_print("> Mode -> READ", ms=900)

            # update trackbar
            cv2.setTrackbarPos(
                self.marker.trackbar_mode,
                self.marker.window_name,
                self.marker.mode.value,
            )

        # MARK <-> READ
        elif _key in (ord("r"), ord("R")):
            if self.marker.mode is Mode.READ:
                self.marker.mode = Mode.MARK
                self.marker.try_overlay_print("> Mode -> MARK", ms=900)
            elif self.marker.mode is Mode.MARK:
                self.marker.mode = Mode.READ
                self.marker.m_image.id_bbox_selected = None
                self.marker.try_overlay_print("> Mode -> READ", ms=900)

            # update trackbar
            cv2.setTrackbarPos(
                self.marker.trackbar_mode,
                self.marker.window_name,
                self.marker.mode.value,
            )

        # switch images and bboxes
        elif _key in (ord("a"), ord("A"), ord("d"), ord("D")):
            if self.marker.mode is Mode.DOODLE:
                self.marker.try_overlay_print(
                    "> Doodle mode can not switch images! Try in Read mode by press `e`."
                )
            else:
                # images
                if not self.marker.m_image.has_bbox_selected():
                    if _key in (ord("a"), ord("A")):
                        self.marker.m_image.last()
                        # self.marker.try_overlay_print(f"> Last image", ms=600)
                    else:
                        self.marker.m_image.next()
                        # self.marker.try_overlay_print(f"> Next image", ms=600)

                    # update trackbar
                    cv2.setTrackbarPos(
                        self.marker.trackbar_image,
                        self.marker.window_name,
                        self.marker.m_image.idx,
                    )
                    # disable line width adjust to each image has recommended line width
                    self.marker.line_thickness.now = None
                else:  # bboxes
                    if _key in (ord("a"), ord("A")):
                        self.marker.m_image.last_bbox_selected()
                        # self.marker.try_overlay_print(f"> Last object", ms=600)
                    else:
                        self.marker.m_image.next_bbox_selected()
                        # self.marker.try_overlay_print(f"> Next object", ms=600)
                    self.marker.m_cls.idx = self.marker.m_image.bboxes[
                        self.marker.m_image.id_bbox_selected
                    ].id_
                    cv2.setTrackbarPos(
                        self.marker.trackbar_class,
                        self.marker.window_name,
                        self.marker.m_cls.idx,
                    )

                # free bboxes predition cache
                if (
                    self.marker.model is not None
                    and self.marker.m_image.bboxes_predicted is not None
                ):
                    self.marker.m_image.bboxes_predicted = None

        # switch classes
        elif _key in (ord("s"), ord("S"), ord("w"), ord("W")):
            if _key in (ord("s"), ord("S")):
                if self.marker.task in (Task.RECT, Task.POLYGON):
                    self.marker.m_cls.next()
                elif self.marker.task is Task.POINT:
                    self.marker.m_cls.kpt_next()
            else:
                if self.marker.task in (Task.RECT, Task.POLYGON):
                    self.marker.m_cls.last()
                elif self.marker.task is Task.POINT:
                    self.marker.m_cls.kpt_last()

            # update class trackbar
            if self.marker.task is Task.RECT:
                cv2.setTrackbarPos(
                    self.marker.trackbar_class,
                    self.marker.window_name,
                    self.marker.m_cls.idx,
                )
            elif self.marker.task is Task.POINT:
                cv2.setTrackbarPos(
                    self.marker.trackbar_kpt_class,
                    self.marker.window_name,
                    self.marker.m_cls.idxk,
                )

            # when select, use W/S to change bbox's class
            if self.marker.m_image.has_bbox_selected():
                self.marker.actions_to_selected_bbox(change_id=True)

        # hiding label text
        elif _key in (ord("n"), ord("N")):
            self.is_hiding_text = not self.is_hiding_text
            self.marker.try_overlay_print(
                f"> {'Hiding' if self.is_hiding_text else 'Showing'} label text."
            )

        # adjust line thickness
        elif _key in (ord("="), ord("+"), ord("-"), ord("_")):
            if _key in (ord("+"), ord("=")):
                self.marker.line_thickness.increase()
                self.marker.try_overlay_print(
                    f"> Line Thickness +1, now = {self.marker.line_thickness.now}"
                )
            else:
                self.marker.line_thickness.decrease()
                self.marker.try_overlay_print(
                    f"> Line Thickness -1, now = {self.marker.line_thickness.now}"
                )

        # min line width toggle
        elif _key in (ord("t"), ord("T")):
            # switch line width betwen 1 and last
            self.marker.line_thickness.toggle = not self.marker.line_thickness.toggle
            self.marker.try_overlay_print(
                f"> Line width is {self.marker.line_thickness.now}, `t` to toggle."
            )

        # display image info
        elif _key in (ord("i"), ord("I")):
            # self.is_showing_path = not self.is_showing_path
            self.marker.try_overlay_print(
                f"> Path: {self.marker.m_image.path}", ms=1000
            )

        # blinking
        elif _key in (ord("b"), ord("B")):
            self.is_blinking = not self.is_blinking
            self.marker.try_overlay_print(
                "> Blinking" if self.is_blinking else "> Not Blinking"
            )

        # remove label file
        elif _key in (ord("c"), ord("C")):
            if not self.marker.m_image.has_bbox_selected():
                if Path(self.marker.m_image.path_label).exists():
                    Path(self.marker.m_image.path_label).unlink()
                    self.marker.try_overlay_print(
                        f"> {len(self.marker.m_image.bboxes)} bboxes deleted, unrecoverable!"
                    )
                else:
                    self.marker.try_overlay_print("> No objects found!")

        # shuffle color palette
        elif _key in (ord("l"), ord("L")):
            self.marker.palette = Palette(shuffle=True)
            self.marker.try_overlay_print("> Color palette shuffled!")

        # show single class [0-8]
        elif _key in range(48, 57):  # 0-8 => 48-56
            value = int(chr(_key))
            if value <= self.marker.m_cls.count - 1:
                self.single_clsidx4showing = value
                self.marker.try_overlay_print(
                    f"> Only show class_id: {self.single_clsidx4showing} => {self.marker.m_cls.names[self.single_clsidx4showing]}"
                )
            else:
                self.single_clsidx4showing = None
                self.marker.try_overlay_print(
                    f"> class_id: {value} not found! Max class is {self.marker.m_cls.count - 1}. Showing all.",
                    ms=1000,
                )

        # show all clsses [9]
        elif _key == 57:
            self.single_clsidx4showing = None
            self.marker.try_overlay_print("> Showing all.", ms=1000)

        # ESC to quit
        elif _key == 27:
            self.quit = True
