import cv2
import time
import numpy as np
from ..utils import preprocess_1, postprocess_1, softmax


class Classification:
    def __init__(self,
                 model_path: str,
                 input_width: int,
                 input_height: int,
                 confidence_thresh: float,
                 class_names: list):
        self.model_path = model_path
        self.input_width = input_width
        self.input_height = input_height
        self.confidence_thresh = confidence_thresh
        self.class_names = class_names
        self.mean = [0.485, 0.456, 0.406]
        self.std = [0.229, 0.224, 0.225]
        self.model = None
        self.det_output = None

    def initialize_model(self):
        # todo 该函数由子类实现
        pass

    def infer(self, image):
        # todo 该函数由子类实现
        # self.outputs:
        # det_output: [batch_size, class_num]
        pass

    def predict(self, image, use_preprocess=True):
        dets, det_scores, det_labels = [], [], []
        s = time.time()
        if isinstance(image, list):
            if use_preprocess:
                img = [preprocess_1(im, (self.input_height, self.input_width), self.mean, self.std) for im in image]
            else:
                img = image
        else:
            if use_preprocess:
                img = preprocess_1(image, (self.input_height, self.input_width), self.mean, self.std)
            else:
                img = image
        print("preprocess: ", time.time() - s)

        s = time.time()
        self.infer(img)
        print("infer: ", time.time() - s)

        assert self.det_output.shape[-1] == len(self.class_names), "infer det output shape is not match"

        s = time.time()
        output_score = np.array([softmax(p) for p in self.det_output])
        output_class = np.argmax(output_score, axis=1)

        for label, score in zip(output_class, output_score):
            dets.append(self.class_names[int(label)])
            det_scores.append(float(score[int(label)]))
            det_labels.append(int(label))
        print("postprocess: ", time.time() - s)

        return dets, det_scores, det_labels

    def feature(self, image, use_preprocess=True):
        s = time.time()
        if isinstance(image, list):
            if use_preprocess:
                img = [preprocess_1(im, (self.input_height, self.input_width), self.mean, self.std) for im in image]
            else:
                img = image
        else:
            if use_preprocess:
                img = preprocess_1(image, (self.input_height, self.input_width), self.mean, self.std)
            else:
                img = image
        print("preprocess: ", time.time() - s)

        s = time.time()
        self.infer(img)
        print("infer: ", time.time() - s)

        s = time.time()
        features = postprocess_1(self.det_output, axis=1)
        print("postprocess: ", time.time() - s)

        return features

    def show(self, image, dets, det_scores, det_labels):
        if dets is None or len(dets) == 0:
            return image
        for det, score, label in zip(dets, det_scores, det_labels):
            print(self.class_names[label], score)
            cv2.putText(image, '%s(%.2f)' % (self.class_names[label], score),
                        (0, 20),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1,
                        (0, 255, 0),
                        thickness=1)
