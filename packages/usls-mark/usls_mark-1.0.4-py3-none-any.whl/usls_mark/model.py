import numpy as np
import onnxruntime
import cv2

from .basics import Task

class Model:
    def __init__(self, f, use_gpu=False):
        # TODO
        self.use_gpu = use_gpu
        self.t_conf = 0.3
        self.t_iou = 0.45
        self.session = onnxruntime.InferenceSession(
            f,
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
            if self.use_gpu
            else ["CPUExecutionProvider"],
        )  # session
        self.cacher = dict()
        self.iShapes = [x.shape for x in self.session.get_inputs()]  # input shapes
        self.oShapes = [x.shape for x in self.session.get_outputs()]  # input shapes
        self.nc = self.oShapes[0][1] - 4
        meta = self.session.get_modelmeta().custom_metadata_map  # metadata
        self.class_names = (
            eval(meta["names"]) if "names" in meta else None
        )  # class names
        
        # task support
        _task = meta["task"] if "task" in meta else None
        self.task = Task.RECT if _task == "detect" else Task.POLYGON if _task == "segment" else NotImplemented
        self.ndtype = (
            np.half
            if self.session.get_inputs()[0].type == "tensor(float16)"
            else np.single
        )  # dtype
        self.conf_update = False  # check if conf updated
        self.class_specific = self.nc  # class_id = nc => all
        self.class_update = False  # check if class_specific updated

    def warmup(self, *, size, n):
        [self(np.empty(size, dtype=np.single)) for _ in range(n)]

    def _preprocess(self, x) -> dict:
        self.cacher["im0"] = x
        shape = x.shape[:2]  # current shape
        new_shape = self.iShapes[0][-2:]
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        self.cacher["ratio"] = r, r
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        self.cacher["dw"], self.cacher["dh"] = (
            (new_shape[1] - new_unpad[0]) / 2,
            (new_shape[0] - new_unpad[1]) / 2,
        )  # wh padding
        if shape[::-1] != new_unpad:  # resize
            x = cv2.resize(x, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = (
            int(round(self.cacher["dh"] - 0.1)),
            int(round(self.cacher["dh"] + 0.1)),
        )
        left, right = (
            int(round(self.cacher["dw"] - 0.1)),
            int(round(self.cacher["dw"] + 0.1)),
        )
        x = cv2.copyMakeBorder(
            x, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114)
        )  # add border
        x = (
            np.ascontiguousarray(np.einsum("asd->das", x)[::-1], dtype=self.ndtype)
            / 255.0
        )  # tranform
        x = x[None] if len(x.shape) == 3 else x
        self.cacher["im"] = x

    def _postprocess(self, x, **kwargs):
        # decode

        self.t_conf = float(kwargs.get("conf") or self.t_conf)  # update conf
        x = x[np.amax(x[..., 4:], axis=-1) > self.t_conf]  # filter by conf
        x[..., :2] = x[..., :2] - x[..., 2:4] / 2
        x = np.c_[
            x[..., :4], np.amax(x[..., 4:], axis=-1), np.argmax(x[..., 4:], axis=-1)
        ]  # box, score, cls
        x = x[cv2.dnn.NMSBoxes(x[:, :4], x[:, -2], self.t_conf, self.t_iou)]  # nms

        # filtering by class
        if self.class_specific != self.nc:
            x = x[x[..., -1] == self.class_specific]

        # de-scale
        x[..., [0, 1]] -= [self.cacher["dw"], self.cacher["dh"]]
        x[..., :4] /= min(self.cacher["ratio"])
        x[..., [0, 2]] = x[:, [0, 2]].clip(0, self.cacher["im0"].shape[1])  # clip
        x[..., [1, 3]] = x[:, [1, 3]].clip(0, self.cacher["im0"].shape[0])

        return x

    def is_updated(self) -> bool:
        return self.conf_update or self.class_update

    def is_class_updated(self) -> bool:
        return self.class_specific

    def is_conf_updated(self) -> bool:
        return self.conf_update

    def reset_class_status(self) -> bool:
        self.class_update = False

    def reset_conf_status(self) -> bool:
        self.conf_update = False

    def reset_status(self) -> bool:
        self.conf_update = False
        self.class_update = False

    def specific_class_name(self) -> str:
        return (
            self.class_names[self.class_specific]
            if self.class_specific != self.nc
            else "All included"
        )

    def set_class(self, x: int) -> int:
        if self.class_specific == x:
            self.class_update = False
        else:
            self.class_specific = x
            self.class_update = True

    def set_conf(self, conf: float):
        if self.t_conf == conf:
            self.conf_update = False
        else:
            self.t_conf = conf
            self.conf_update = True

    def __call__(self, x, **kwargs):
        # the whole pipeline
        self._preprocess(x)
        y = np.einsum(
            "asd->ads",
            self.session.run(
                None, {self.session.get_inputs()[0].name: self.cacher["im"]}
            )[0],
        )[0]
        ys = self._postprocess(y, **kwargs)
        return ys


if __name__ == "__main__":
    model = Model("/mnt/z/Desktop/yolov8m.onnx")
    _ = model(cv2.imread("/mnt/z/Desktop/falling/0000000000.jpg"))
