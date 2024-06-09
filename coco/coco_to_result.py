import json
import numpy as np
import pycocotools
from pycocotools.coco import COCO
import pycocotools.coco
from pycocotools.cocoeval import COCOeval
from pycocotools import mask as maskUtils
import pycocotools.mask


def coco_to_detection_result_bbox(coco_file, result_file, score=1.0, indent=4):
    """"""
    with open(coco_file) as fp:
        coco = json.load(fp)
    anns = coco["annotations"]

    results = []
    for ann in anns:
        result = {
            "image_id": ann["image_id"],
            "category_id": ann["category_id"],
            "bbox": ann["bbox"],
            "score": score,
        }
        results.append(result)

    with open(result_file, "w") as fp:
        json.dump(results, fp, indent=indent)


def coco_to_detection_result_segment(coco_file, result_file, score=1.0, indent=4):
    """"""
    with open(coco_file) as fp:
        coco = json.load(fp)
    img_id_to_info = {x["id"]: x for x in coco["images"]}
    anns = coco["annotations"]

    results = []
    for ann in anns:
        seg = ann["segmentation"]
        img_id = ann["image_id"]
        img_info = img_id_to_info[img_id]
        img_h = img_info["height"]
        img_w = img_info["width"]
        if isinstance(seg, list):
            rles = pycocotools.mask.frPyObjects(
                pyobj=seg, h=img_h, w=img_w)
        elif isinstance(seg, dict):
            rles = pycocotools.mask.frPyObjects(
                pyobj=[seg["counts"]], h=img_h, w=img_w)
        else:
            raise ValueError

        for idx, _ in enumerate(rles):
            rles[idx]["counts"] = rles[idx]["counts"].decode() # bytes to str
        rle = pycocotools.mask.merge(rles, intersect=False)
        rle["counts"] = rle["counts"].decode()

        result = {
            "image_id": img_id,
            "category_id": ann["category_id"],
            "segmentation": rle,
            "score": score,
        }
        results.append(result)

    with open(result_file, "w") as fp:
        json.dump(results, fp, indent=indent,)


def _evaluate(annotation_file, result_file, iou_type):
    assert iou_type in ("bbox", "segm", "keypoints")
    coco_gt = COCO(annotation_file)
    coco_dt = coco_gt.loadRes(result_file)
    coco_eval = COCOeval(coco_gt, coco_dt, iouType=iou_type)
    coco_eval.evaluate()
    coco_eval.accumulate()
    coco_eval.summarize()


def _evaluaate_object_detection_bbox():
    annotation_file = r'.\coco\.annotations\instances_val2017.json'
    result_file = r'detection_result_bbox.json'
    coco_to_detection_result_bbox(annotation_file, result_file)
    _evaluate(annotation_file, result_file, iou_type="bbox")


def _evaluaate_object_detection_segm():
    annotation_file = r'.\coco\.annotations\instances_val2017.json'
    result_file = r'detection_result_segm.json'
    coco_to_detection_result_segment(annotation_file, result_file)
    _evaluate(annotation_file, result_file, iou_type="segm")


def _main():
    # _evaluaate_object_detection_bbox()
    _evaluaate_object_detection_segm()

if __name__ == "__main__":
    _main()
