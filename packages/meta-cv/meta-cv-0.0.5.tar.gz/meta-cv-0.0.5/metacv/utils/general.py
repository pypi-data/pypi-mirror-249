import cv2
import numpy as np


def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)


def xywh2xyxy(x):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2
    y[..., 1] = x[..., 1] - x[..., 3] / 2
    y[..., 2] = x[..., 0] + x[..., 2] / 2
    y[..., 3] = x[..., 1] + x[..., 3] / 2
    return y


def _force_forder(x):
    """
    Converts arrays x to fortran order. Returns
    a tuple in the form (x, is_transposed).
    """
    if x.flags.c_contiguous:
        return x.T, True
    else:
        return x, False


def fast_dot(A, B):
    """
    Uses blas libraries directly to perform dot product
    """
    from scipy import linalg

    a, trans_a = _force_forder(A)
    b, trans_b = _force_forder(B)
    gemm_dot = linalg.get_blas_funcs("gemm", arrays=(a, b))

    # gemm is implemented to compute: C = alpha * AB  + beta * C
    return gemm_dot(alpha=1.0, a=a, b=b, trans_a=trans_a, trans_b=trans_b)


def preprocess_1(img, input_size):
    # 传入图像默认为RGB
    if img.shape[:2] == input_size:
        padded_img = img.astype(np.float32)
    else:
        padded_img = cv2.resize(img, (input_size[1], input_size[0]), interpolation=cv2.INTER_LINEAR).astype(np.float32)

    return padded_img


def postprocess_1(nparray, order=2, axis=-1):
    """Normalize a N-D numpy array along the specified axis."""
    norm = np.linalg.norm(nparray, ord=order, axis=axis, keepdims=True)
    return nparray / (norm + np.finfo(np.float32).eps)


def preprocess(img, input_size):
    # 传入图像默认为RGB
    r = min(input_size[0] / img.shape[0], input_size[1] / img.shape[1])

    if img.shape[:2] == input_size:
        padded_img = img.astype(np.float32)
    else:
        if len(img.shape) == 3:
            padded_img = np.ones((input_size[0], input_size[1], 3), dtype=np.float32) * 114
        else:
            padded_img = np.ones(input_size, dtype=np.float32) * 114
        resized_img = cv2.resize(img,
                                 (int(round(img.shape[1] * r)), int(round(img.shape[0] * r))),
                                 interpolation=cv2.INTER_LINEAR).astype(np.float32)
        padded_img[: int(round(img.shape[0] * r)), : int(round(img.shape[1] * r))] = resized_img

    return padded_img, r


def nms(boxes, scores, nms_thr):
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)

        inds = np.where(ovr <= nms_thr)[0]
        order = order[inds + 1]

    return keep


def multiclass_nms(boxes, scores, nms_thr, score_thr, predictions=None):
    num_classes = scores.shape[1]
    mi = 4 + num_classes  # mask start index

    cls_scores = np.max(scores, axis=1)
    cls_indexes = np.argmax(scores, axis=1)
    valid_score_mask = cls_scores > score_thr
    if valid_score_mask.sum() == 0:
        return None
    else:
        valid_indexes = cls_indexes[valid_score_mask]
        valid_scores = cls_scores[valid_score_mask]
        valid_boxes = boxes[valid_score_mask]
        valid_predictions = predictions[valid_score_mask]
        keep = nms(valid_boxes, valid_scores, nms_thr)
        if len(keep) > 0:
            if predictions is None:
                dets = np.concatenate([valid_boxes[keep], valid_scores[keep, None], valid_indexes[keep]], 1)
            else:
                dets = np.concatenate(
                    [valid_boxes[keep], valid_scores[keep, None], valid_indexes[keep, None],
                     valid_predictions[keep, mi:]], 1)

    if len(dets) == 0:
        return None

    return dets


def postprocess(predictions, ratio, score_thr, nms_thr, num_classes):
    boxes = predictions[:, :4]
    scores = predictions[:, 4:4 + num_classes]
    boxes_xyxy = np.ones_like(boxes)
    boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2.
    boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2.
    boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2.
    boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2.
    boxes_xyxy /= ratio

    dets = multiclass_nms(boxes_xyxy, scores, nms_thr=nms_thr, score_thr=score_thr, predictions=predictions)

    return dets


def mask2contour(mask):
    h, w = mask.shape[:2]
    _, pred = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(pred, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) < 1:
        return [[[0, 0]], [[0, w - 1]], [[h - 1, w - 1]], [[h - 1, 0]]]

    area = [cv2.contourArea(c) for c in contours]
    max_idx = np.argmax(area)

    return contours[max_idx]


def distance2bbox(points, distance, max_shape=None):
    """Decode distance prediction to bounding box.

    Args:
        points (Tensor): Shape (n, 2), [x, y].
        distance (Tensor): Distance from the given point to 4
            boundaries (left, top, right, bottom).
        max_shape (tuple): Shape of the image.

    Returns:
        Tensor: Decoded bboxes.
    """
    x1 = points[:, 0] - distance[:, 0]
    y1 = points[:, 1] - distance[:, 1]
    x2 = points[:, 0] + distance[:, 2]
    y2 = points[:, 1] + distance[:, 3]
    if max_shape is not None:
        x1 = x1.clamp(min=0, max=max_shape[1])
        y1 = y1.clamp(min=0, max=max_shape[0])
        x2 = x2.clamp(min=0, max=max_shape[1])
        y2 = y2.clamp(min=0, max=max_shape[0])
    return np.stack([x1, y1, x2, y2], axis=-1)


def postprocess_2(predictions, input_size, ratio, score_thr, nms_thr, feat_stride_fpn=[8, 16, 32]):
    bboxes_list, scores_list = [], []
    center_cache = {}
    for idx, stride in enumerate(feat_stride_fpn):
        scores = predictions[idx * 3]
        bbox_preds = predictions[idx * 3 + 1]
        bbox_preds = bbox_preds * stride
        height = input_size[0] // stride
        width = input_size[1] // stride
        key = (height, width, stride)
        if key in center_cache:
            anchor_centers = center_cache[key]
        else:
            anchor_centers = np.stack(np.mgrid[:height, :width][::-1], axis=-1).astype(np.float32)
            anchor_centers = (anchor_centers * stride).reshape((-1, 2))
            anchor_centers = np.stack([anchor_centers] * 2, axis=1).reshape((-1, 2))
            if len(center_cache) < 100:
                center_cache[key] = anchor_centers

        pos_inds = np.where(scores >= score_thr)[0]
        bboxes = distance2bbox(anchor_centers, bbox_preds)
        pos_scores = scores[pos_inds]
        pos_bboxes = bboxes[pos_inds]
        scores_list.append(pos_scores)
        bboxes_list.append(pos_bboxes)

    scores = np.vstack(scores_list)
    scores_ravel = scores.ravel()
    order = scores_ravel.argsort()[::-1]
    bboxes = np.vstack(bboxes_list) / ratio

    pre_det = np.hstack((bboxes, scores)).astype(np.float32, copy=False)
    pre_det = pre_det[order, :]
    keep = nms(bboxes, scores, nms_thr)
    det = pre_det[keep, :]

    return det
