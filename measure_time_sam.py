"""SAMの処理時間計測用コード"""

import argparse
import json
import random
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
import PIL.Image
import torch
import tqdm
from segment_anything import SamPredictor, sam_model_registry

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
    """コマンドライン引数"""

    # SAMのバックボーンモデル ["vit_h", "vit_l", "vit_b"]
    model_type: str = ""

    # 入力画像パス
    # input_image: str = ""

    # 入力画像サイズ
    image_width: int = 0
    image_height: int = 0

    # 測定の繰り返し回数
    iterations: int = 0

    # 推論に使用するデバイス ["cuda", "cpu"]
    device: str = ""

    # SAM推論時の複数マスク出力フラグ
    multimask_output: bool = True

    # SAM推論時のロジット出力フラグ
    return_logits: bool = False

    # 乱数シード
    rand_seed: int = 12345

    # 出力先ディレクトリ
    output_dir: str = ""

    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf8") as fp:
            json.dump(
                self.__dict__,
                fp,
                indent=4,
            )

    # @classmethod
    # def load(cls, path):
    #     with open(path) as fp:
    #         items = json.load(fp)
    #         return CommandLineArguments(**items)


def _get_args() -> CommandLineArguments:
    """コマンドライン引数の取得"""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model_type",
        default="vit_b",
        type=str,
        choices=["vit_h", "vit_l", "vit_b"],
        # help="(default: 'vit_h')"
    )
    # parser.add_argument(
    #     "--input_image",
    #     default=None,
    #     type=str,
    #     # help=""
    # )
    parser.add_argument(
        "--image_width",
        # default=-1,
        default=1024,
        type=int,
        help="",
    )
    parser.add_argument(
        "--image_height",
        # default=-1,
        default=1024,
        type=int,
        # help=""
    )
    parser.add_argument(
        "--iterations",
        default=20,
        type=int,
        # help=""
    )
    parser.add_argument(
        "--device",
        default="cuda",
        type=str,
        choices=["cuda", "cpu"],
        # help=""
    )
    parser.add_argument(
        "--multimask_output",
        action="store_true",
        # help=""
    )
    parser.add_argument(
        "--return_logits",
        action="store_true",
        # help=""
    )
    parser.add_argument(
        "--rand_seed",
        default=12345,
        type=int,
        # help=""
    )
    parser.add_argument(
        "--output_dir",
        default=".result",
        type=str,
        # help=""
    )

    args = parser.parse_args()
    return CommandLineArguments(**args.__dict__)


def _initialize_seed(seed):
    """乱数シード初期化"""
    random.seed(seed)
    np.random.seed(seed)
    torch.random.manual_seed(seed)


def _load_image_as_rgb_format(path: str) -> np.ndarray:
    """画像ファイルの読み込み"""
    with PIL.Image.open(path) as pil_img:
        pil_img = pil_img.convert("RGB")
        img = np.array(pil_img)
    return img


def _resize_image(img: np.ndarray, width: int, height: int) -> np.ndarray:
    """画像のリサイズ"""
    img_ = PIL.Image.fromarray(img)
    img_ = img_.resize((width, height), PIL.Image.Resampling.BILINEAR)
    return np.array(img_)


def _generate_test_image_and_prompt(
    img_w: int,
    img_h: int,
    num_point: int,
    use_box: bool,
    seed: int,
) -> Tuple[np.ndarray, dict]:
    """テスト用画像とプロンプト生成"""

    _initialize_seed(seed)

    if num_point > 0:
        point_coords = np.hstack((
            np.random.randint(low=0, high=img_w, size=(num_point, 1)),
            np.random.randint(low=0, high=img_h, size=(num_point, 1)),
        ))
        point_labels = np.random.randint(low=0, high=2, size=(num_point))
    else:
        point_coords = None
        point_labels = None

    if use_box:
        box = [0, 0, img_w, img_h]
    else:
        box = None

    mask_input = None

    # 画像生成
    img = np.random.randint(
        low=0, high=256, size=(img_h, img_w, 3),
        dtype=np.uint8)

    # 物体描画
    # img = np.zeros((img_h, img_w, 3), np.uint8)
    # for coord, label in zip(point_coords, point_labels):
    #     if label == 0:
    #         continue
    #     x, y = coord
    #     img[y, x] = 255

    # プロンプト
    prompt = {
        "point_coords": point_coords,
        "point_labels": point_labels,
        "box": box,
        "mask_input": mask_input,
    }

    return img, prompt


def main():
    # 年月日時分秒の文字列　"YYYYMMDD_hhmmss"
    # dt_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    # コマンドライン引数の取得
    args = _get_args()
    print(f"{args=}")

    # 乱数シード初期化
    _initialize_seed(args.rand_seed)

    # 測定対象の入力画像の準備
    if False and args.input_image is not None and args.input_image != "":
        # 入力画像ファイルパス
        img_path = Path(args.input_image).absolute()
        if not img_path.exists():
            raise ValueError(f"Not found {img_path}.")
        if not img_path.is_file():
            raise ValueError(f"{img_path} is not a file.")

        # 入力画像を読み込み
        img = _load_image_as_rgb_format(args.input_image)

        # 画像サイズが指定されていればリサイズ
        img_h, img_w = img.shape[:2]
        img_w = args.image_width if args.image_width > 0 else img_w
        img_h = args.image_height if args.image_height > 0 else img_h
        img = _resize_image(img, img_w, img_h)

    else:
        # 入力画像とプロンプトを生成
        img_h = args.image_height
        img_w = args.image_width
        img, prompt = _generate_test_image_and_prompt(
            img_w=args.image_width,
            img_h=args.image_height,
            num_point=0,
            use_box=False,
            seed=args.rand_seed,
        )

    # SAMモデルのインスタンス生成と初期化
    build_sam = sam_model_registry[args.model_type]
    sam_model = build_sam(checkpoint=_SAM_CHECKPOINT_MAP[args.model_type])
    sam_model.to(args.device)
    sam_predictor = SamPredictor(sam_model)

    # ウォームアップ
    if True:
        sam_predictor.set_image(img)
        sam_predictor.predict()

    # 推論パラメータ

    point_coords = prompt.get("point_coords", None)
    point_labels = prompt.get("point_labels", None)
    box = prompt.get("box", None)
    mask_input = prompt.get("mask_input", None)
    multimask_output = args.multimask_output
    return_logits = args.return_logits

    # debug
    print(f"{point_coords=}")
    print(f"{point_labels=}")
    print(f"{box=}")
    if mask_input is not None:
        print(f"{mask_input.shape=}")
    print(f"{multimask_output=}")
    print(f"{return_logits=}")

    time_list = []
    for _ in tqdm.tqdm(range(args.iterations)):
        ts = []

        torch.cuda.synchronize()
        ts.append(["", time.perf_counter()])

        # 画像エンコード
        sam_predictor.set_image(img, image_format="RGB")

        torch.cuda.synchronize()
        ts.append(["set_image", time.perf_counter()])

        # 推論
        masks, iou_preds, low_res_masks = sam_predictor.predict(
            point_coords=point_coords,
            point_labels=point_labels,
            box=box,
            mask_input=mask_input,
            multimask_output=multimask_output,
            return_logits=return_logits,
        )

        torch.cuda.synchronize()
        ts.append(["predict", time.perf_counter()])

        # debug
        if False:
            print(f"{masks.shape=},"
                  f"{masks.dtype=},"
                  f"{iou_preds=},"
                  f"{low_res_masks.shape=},"
                  f"{low_res_masks.dtype=}")

        # 処理時間
        time_map = {}
        for idx, (caption, _) in enumerate(ts[1:]):
            msec = (ts[idx + 1][1] - ts[idx][1]) * 1e3
            time_map[caption] = msec
        msec = (ts[-1][1] - ts[0][1]) * 1e3
        time_map["total"] = msec
        time_list.append(time_map)

    # 出力先ディレクトリパス
    img_h, img_w = img.shape[:2]
    info_str = "_".join([
        # f"{dt_str}",
        f"{args.model_type}",
        f"{img_w}x{img_h}",
        f"{args.device}",
    ])
    output_dir = (Path(args.output_dir) / info_str)

    # パラメータの保存
    args.save(output_dir / "args.json")

    # 処理時間の保存
    df_rawtime = pd.DataFrame(time_list)
    df_summary = df_rawtime.describe()
    df_rawtime.to_csv(Path(output_dir) / "time_measure_rawtime.csv")
    df_summary.to_csv(Path(output_dir) / "time_measure_summary.csv")
    # df_rawtime.to_json(Path(output_dir) / "time_measure_rawtime.json")
    # df_summary.to_json(Path(output_dir) / "time_measure_summary.json")

    print(df_summary)


if __name__ == "__main__":
    main()
