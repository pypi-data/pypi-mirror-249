import cv2
import time
import numpy as np
from ..utils import preprocess, postprocess, sigmoid, mask2contour


class Segment:
    def __init__(self,
                 model_path: str,
                 input_width: int,
                 input_height: int,
                 confidence_thresh: float,
                 nms_thresh: float,
                 class_names: list):
        self.model_path = model_path
        self.input_width = input_width
        self.input_height = input_height
        self.nms_thresh = nms_thresh
        self.confidence_thresh = confidence_thresh
        self.class_names = class_names
        self.feature_size = (self.input_height // 4, self.input_width // 4)
        self.model = None
        self.det_output = None
        self.mask_output = None

    def initialize_model(self):
        # todo 该函数由子类实现
        pass

    def infer(self, image):
        # todo 该函数由子类实现
        # self.outputs:
        # det_output: [1, 32 + 4 + 80, 6300]
        # mask_output: [1, 32, 120, 160]
        pass

    def predict(self, image, use_preprocess=True, pad=None, normal=None, mean=None, std=None, swap=None):
        total_dets, total_scores, total_labels = [], [], []
        s = time.time()
        if isinstance(image, list):
            batch_size = len(image)
            if use_preprocess:
                outputs = [preprocess(im, (self.input_height, self.input_width),
                                      pad, normal, mean, std, swap) for im in image]
                img, ratio = [out[0] for out in outputs], outputs[0][1]
            else:
                img, ratio = image, 1.0
        else:
            batch_size = 1
            if use_preprocess:
                img, ratio = preprocess(image, (self.input_height, self.input_width), pad, normal, mean, std, swap)
            else:
                img, ratio = image, 1.0
        print("preprocess: ", time.time() - s)

        s = time.time()
        self.infer(img)
        print("infer: ", time.time() - s)

        assert self.det_output.shape[1] == (32 + 4 + len(self.class_names)), "infer det output shape is not match"

        s = time.time()
        for i in range(batch_size):
            dets, det_scores, det_labels = [], [], []
            boxes = postprocess(self.det_output[i].T, ratio=1., score_thr=self.confidence_thresh,
                                nms_thr=self.nms_thresh, num_classes=len(self.class_names))
            if boxes is None:
                total_dets.append(dets)
                total_scores.append(det_scores)
                total_labels.append(det_labels)
                continue

            masks = sigmoid(boxes[:, 6:] @ self.mask_output[i])
            masks = masks.reshape((-1, self.feature_size[0], self.feature_size[1]))

            ih, iw = self.feature_size[0] / self.input_height, self.feature_size[1] / self.input_width
            for mask, box, score, label in zip(masks, boxes[:, :4], boxes[:, 4], boxes[:, 5]):
                x1, y1, x2, y2 = max(box[0] * iw, 0), max(box[1] * ih, 0), box[2] * iw, box[3] * ih
                crop = mask[int(y1):int(y2) + 1, int(x1):int(x2) + 1] * 255
                contour = mask2contour(crop.astype(np.uint8))
                contour = [(int((c[0][0] + x1) / ih / ratio), int((c[0][1] + y1) / ih / ratio)) for c in contour]
                dets.append(contour)
                det_scores.append(float(score))
                det_labels.append(int(label))

            total_dets.append(dets)
            total_scores.append(det_scores)
            total_labels.append(det_labels)
        print("postprocess: ", time.time() - s)

        return total_dets, total_scores, total_labels

    def show(self, image, dets, det_scores, det_labels):
        if dets is None or len(dets) == 0:
            return image
        for det, score, label in zip(dets, det_scores, det_labels):
            min_rect = cv2.minAreaRect(np.array(det))
            min_rect = cv2.boxPoints(min_rect)
            x, y = [int(r[0]) for r in min_rect], [int(r[1]) for r in min_rect]
            cv2.line(image, pt1=(x[0], y[0]), pt2=(x[1], y[1]), color=(255, 255, 0), thickness=2)
            cv2.line(image, pt1=(x[1], y[1]), pt2=(x[2], y[2]), color=(255, 255, 0), thickness=2)
            cv2.line(image, pt1=(x[2], y[2]), pt2=(x[3], y[3]), color=(255, 255, 0), thickness=2)
            cv2.line(image, pt1=(x[3], y[3]), pt2=(x[0], y[0]), color=(255, 255, 0), thickness=2)
            print(self.class_names[label], score)
            cv2.putText(image, '%s(%.2f)' % (self.class_names[label], score),
                        ((x[0] + x[2]) // 2, (y[0] + y[2]) // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 255, 0),
                        thickness=2)

        return image
