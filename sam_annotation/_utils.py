import os
from pathlib import Path

import PIL.Image
import PIL.ImageChops
import numpy as np
import cv2


def make_parent_dir(filepath: str):
    """親ディレクトリ作成"""
    filepath_ = Path(filepath)
    filepath_.parent.mkdir(parents=True, exist_ok=True)

def load_image_info(
    path: str
):
    """画像情報の読み込み"""
    info = {}
    with PIL.Image.open(path) as img:
        info["width"] = img.width
        info["height"] = img.height
        info["size"] = img.size
    return info

def load_image(
    path: str,
    # img_format: str, # "RGB", "BGR", "GRAY"
) -> np.ndarray:
    """画像ファイルの読み込み

    Args:
        path (str): 画像ファイルパス

    Returns:
        np.ndarray: _description_
    """

    with PIL.Image.open(path) as pil_img:
        pil_img = pil_img.convert("RGB")
        img = np.array(pil_img)

    return img


def save_image(
    path: str,
    img: np.ndarray,
    # img_format: str,
):
    """画像ファイルの保存

    Args:
        path (str): 保存先の画像ファイルパス
        img (np.ndarray): 画像
    """
    make_parent_dir(path)
    pil_img = PIL.Image.fromarray(img)
    pil_img.save(path)


def find_image_files(
    img_dir: str,
    recursive: bool = True,
) -> list:
    """指定のディレクトリ内にある画像ファイルの探索

    Args:
        img_dir (str): 探索対象のディレクトリ
        recursive (bool): 再帰探索フラグ

    Returns:
        list: 画像ファイルパスのリスト
    """
    _target_img_exts = ('.bmp', '.png', '.jpg', '.jpeg', '.tif', '.tiff')

    img_dir_ = Path(img_dir).absolute()
    image_paths = []

    for dirpath, dirnames, filenames in os.walk(img_dir_):
        dirpath_ = Path(dirpath).absolute()
        if not recursive and dirpath_ != img_dir_:
            continue
        for file in filenames:
            if file.lower().endswith(_target_img_exts):
                img_path = Path(dirpath) / file
                image_paths.append(str(img_path))

    return image_paths


def apply_colored_mask(
    img: np.ndarray,
    mask: np.ndarray,
    color: np.ndarray,
    alpha: float = 0.5
) -> np.ndarray:
    """
    RGB画像に青色のマスクを適用します。

    Parameters:
        image (np.ndarray): 元のRGB画像
        mask (np.ndarray): セグメンテーションマスク（bool型）
        alpha (float): マスクの透明度（0.0～1.0）

    Returns:
        np.ndarray: 青色マスクが適用された画像
    """
    assert mask.shape == img.shape[:2]
    mask_ = mask.astype(bool)

    # 元画像のコピー
    result_img = img.copy()

    # 指定されたカラーのオーバーレイを作成
    color_overlay = np.zeros_like(img)
    color_overlay[..., 0] = color[0]
    color_overlay[..., 1] = color[1]
    color_overlay[..., 2] = color[2]

    # ブレンド
    # マスクが全部無効だとエラーになるのでanyチェックを入れている
    if mask_.any():
        result_img[mask_] = cv2.addWeighted(
            src1=img[mask_],
            alpha=1.0 - alpha,
            src2=color_overlay[mask_],
            beta=alpha,
            gamma=0.0,
        )

    return result_img
