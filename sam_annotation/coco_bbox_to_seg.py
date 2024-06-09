import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import cv2
import pycocotools.coco

import _utils
from sam_predictor_wrapper import SamPredictorWrapper

# SAMのチェックポイントを配置しているディレクトリへのパス
_SAM_CHECKPOINT_DIR = "./weights"

# SAMの各モデルタイプに対応するチェックポイント
_SAM_CHECKPOINT_MAP = {
    "vit_h": f"{_SAM_CHECKPOINT_DIR}/sam_vit_h_4b8939.pth",
    "vit_l": f"{_SAM_CHECKPOINT_DIR}/sam_vit_l_0b3195.pth",
    "vit_b": f"{_SAM_CHECKPOINT_DIR}/sam_vit_b_01ec64.pth",
}


@dataclass
class CommandLineArguments:
    """コマンドライン引数パラメータ"""

    # アノテーションファイルパス
    anno_file: str = ""

    # 画像ディレクトリパス
    img_dir: str = ""

    # SAMのバックボーンモデルの種類
    sam_model_type: str = "vit_h"  # vit_h, vit_l, vit_b のいずれか

    # SAMモデルのチェックポイントパス
    sam_checkpoint: str = ""


def get_args() -> CommandLineArguments:
    """コマンドライン引数の取得"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--anno_file",
        default=r"X:\coco-annotator\datasets\ObjectBox\.exports\coco-1721658307.3440244.json",
        type=str,
    )
    parser.add_argument(
        "--img_dir",
        default=r"X:\coco-annotator\datasets\ObjectBox",
        type=str,
    )
    parser.add_argument(
        "--sam_model_type",
        default="vit_h",
        type=str,
        choices=["vit_h", "vit_l", "vit_b"]
    )
    parser.add_argument(
        "--sam_checkpoint",
        default=r"",
        type=str,
    )
    args = parser.parse_args()
    return CommandLineArguments(**args.__dict__)


def convert_mask_to_polygon(mask):

    # マスク領域の輪郭を取得
    contours, _ = cv2.findContours(
        mask.astype(np.uint8),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # ポリゴン座標に変換
    polygon = []
    for contour in contours:
        contour = contour.flatten().tolist()  # Flattenしてリストに変換
        if len(contour) > 4:  # 有効なポリゴンのみを追加
            polygon.append(contour)

    return polygon


def main():
    """メイン処理"""
    # コマンドライン引数を取得
    args = get_args()
    # モデルのチェックポイントが空の時は自動設定
    if args.sam_checkpoint is None or args.sam_checkpoint == "":
        args.sam_checkpoint = _SAM_CHECKPOINT_MAP[args.sam_model_type]

    # 画像ディレクトリ内の画像ファイルを取得
    img_paths = _utils.find_image_files(args.img_dir, recursive=False)
    img_name_to_path = {Path(p).name: p for p in img_paths}

    if len(img_paths) != len(set(img_name_to_path)):
        # 画像ファイル名（親ディレクトリパス部を除く）の重複エラー
        raise RuntimeError("len(img_paths) != len(set(img_filenames))")

    if not Path(args.anno_file).exists():
        # アノテーションファイルが存在しない
        raise RuntimeError(f"Not found annotation file. {args.anno_file=}")

    # アノテーションファイルの読み込み
    coco = pycocotools.coco.COCO(args.anno_file)

    # SAMモデルのインスタンス生成
    predictor = SamPredictorWrapper(
        model_type=args.sam_model_type,
        checkpoint=args.sam_checkpoint,
        device='cuda:0'
    )

    for img_id, img_info in coco.imgs.items():
        img_name = img_info["file_name"]
        # img_path = Path(args.img_dir) / img_filename
        img_path = img_name_to_path[img_name]
        print(f"{img_path=}")

        # 画像ファイル読み込み
        org_img = _utils.load_image(img_path)

        # 画像埋め込み
        predictor.set_image(org_img, img_format='RGB')

        # BBoxごとに処理
        annos = coco.imgToAnns[img_id]
        anno_id_to_seg = {}
        for anno in annos:
            anno_id = anno["id"]
            bbox = anno["bbox"]

            # アノテーションのBBoxをSAMのプロンプトに指定
            predictor.set_prompt(box=bbox)

            # マスク推論
            masks = predictor.predict(multimask_output=False)
            print(f"{bbox=}, {masks.shape}")

            # マスクをポリゴンデータに変換
            mask = masks[0]
            polygon = convert_mask_to_polygon(mask)
            anno_id_to_seg[anno_id] = polygon

            coco.anns[anno_id]["segmentation"] = polygon
            coco.anns[anno_id]["iscrowd"] = 0

    with open("output.json", "w") as fp:
        json.dump(coco.dataset, fp)


if __name__ == '__main__':
    main()
