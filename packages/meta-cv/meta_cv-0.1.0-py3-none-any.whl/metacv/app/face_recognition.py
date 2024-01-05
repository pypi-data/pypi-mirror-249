import time
from ..utils import preprocess


class FaceRecognition:
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

    def predict(self, image, use_preprocess=True, pad=None, normal=None, mean=None, std=None, swap=None):
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

        s = time.time()
        embedding = self.det_output.flatten()
        print("postprocess: ", time.time() - s)

        return embedding
