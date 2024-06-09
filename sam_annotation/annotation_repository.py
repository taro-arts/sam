import threading
import json
from pathlib import Path

import numpy as np
import pycocotools
import pycocotools.coco
from pycocotools import mask as mask_tools
import cv2

import sam_annotation._utils as _utils
from sam_annotation._id_manager import IDManager
# from ._logger import Logger

from dataclasses import dataclass


@dataclass
class _CategoryInfo:
    """カテゴリ情報クラス"""
    id: int = -1
    name: str = ""
    subcategory: str = ""

    def as_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class _ImageInfo:
    """画像情報クラス"""

    id: int = -1
    filename: str = ""
    width: int = -1
    height: int = -1
    # _license = None
    # _flickr_url: str = ""
    # _coco_url: str = ""
    # _date_captured: str = "YYYY/MM/DD"

    def as_dict(self) -> dict:
        return self.__dict__.copy()


@dataclass
class _AnnotationInfo:
    """アノテーション情報クラス"""
    id = -1
    image_id = -1
    catetory_id = -1
    segmentation = None
    area = 0.0
    bbox = [0.0] * 4
    iscrowd = 0

    def as_dict(self) -> dict:
        return self.__dict__.copy()


class AnnotationRepository:
    """アノテーション管理クラス"""

    def __init__(
        self,
    ):
        """コンストラクタ"""
        self._lock = threading.RLock()

        # 画像ディレクトリのルートパス
        self._img_root_dir = ""

        # アノテーション、画像、カテゴリの各ID管理インスタンス
        self._img_id_manager = IDManager()
        self._cat_id_manager = IDManager()
        self._anno_id_manager = IDManager()
        
        # 画像IDと画像情報の対応マップ
        self._img_id_to_info = {}   # COCO形式

        # カテゴリIDとカテゴリ情報の対応マップ
        self._cat_id_to_info = {}   # COCO形式

        # アノテーションIDとアノテーション情報の対応マップ
        self._anno_id_to_info = {}  # COCO形式

        # 画像パスと画像IDの対応マップ
        self._img_id_to_path = {}
        self._img_path_to_id = {}

        # 画像IDとアノテーションリストのマップ
        self._img_id_to_anno_list = {}

        # 現在の画像インデックス
        self._img_idx = 0

    @property
    def image_paths(self) -> list:
        return list(self._img_path_to_id.keys())

    def initialize(
        self,
        img_root_dir: str,
        recursive=True,
        coco_file=None
    ):
        """初期化処理"""
        with self._lock:
            self._img_root_dir = img_root_dir
            self._load(img_root_dir, recursive, coco_file)

    def _load(
        self,
        img_root_dir: str,
        recursive=True,
        coco_file=None
    ):
        if coco_file is None:
            # 画像ファイルを探索してパスリスト作成
            img_paths = _utils.find_image_files(
                img_dir=img_root_dir, recursive=recursive)

            # 画像ファイルパスのリストに重複はない前提
            assert len(img_paths) == len(set(img_paths))

            for img_path in img_paths:
                # 画像ID生成
                img_id = self._img_id_manager.generate_id()

                # 画像情報の取得
                img_info = _utils.load_image_info(img_path)
                info = _ImageInfo()
                info.id = img_id
                info.filename = Path(img_path).name
                info.width = img_info["width"]
                info.height = img_info["height"]

                # 画像IDと画像情報の対応付け
                self._img_path_to_id[img_path] = img_id
                self._img_id_to_path[img_id] = img_path
                self._img_id_to_info[img_path] = info

        else:
            coco = pycocotools.coco.COCO(coco_file)

            # アノテーション情報
            for anno_id, ann in coco.anns.items():
                assert anno_id == ann['id']
                self._anno_id_manager.append_id(anno_id)

                anno_info = _AnnotationInfo()
                anno_info.id = ann["id"]
                anno_info.image_id = ann["image_id"]
                anno_info.catetory_id = ann["category_id"]
                anno_info.segmentation = ann["segmentation"]
                anno_info.iscrowd = ann["iscrowd"]
                anno_info.bbox = ann["bbox"]
                anno_info.area = ann["area"]
                self._anno_id_to_info[anno_id] = anno_info

            # 画像情報
            for img_id, img in coco.imgs.items():
                assert img_id == img['id']
                self._img_id_manager.append_id(img_id)

                img_info = _ImageInfo()
                img_info.id = img["id"]
                img_info.filename = img["filename"]
                img_info.width = img["width"]
                img_info.height = img["height"]
                self._anno_id_to_info[img_id] = img_info

            # カテゴリ情報
            for cat_id, cat in coco.cats.items():
                assert cat_id == cat['id']
                self._cat_id_manager.append_id(cat_id)

                cat_info = _CategoryInfo()
                cat_info.id = cat["id"]
                cat_info.name = cat["name"]
                cat_info.subcategory = cat["supercategory"]
                self._cat_id_to_info[anno_id] = cat_info

            # TODO: COCOファイルで初期化できるようにする
            raise NotImplementedError

    def save(self, filepath):
        """アノテーション情報の保存"""
        with self._lock:
            coco_data = self._coco_data()
            with open(filepath, 'w') as f:
                json.dump(coco_data, f)

    def _coco_data(self):
        """COCO形式データに変換"""
        with self._lock:
            images = []
            for _, info in self._img_id_to_info.items():
                images.append(info.to_dict())

            categories = []
            for _, info in self._cat_id_to_info.items():
                categories.append(info.to_dict())

            annotations = []
            for _, info in self._anno_id_to_info.items():
                annotations.append(info.to_dict())

            categories = self._create_category_info_list()

            # COCO形式のアノテーションファイルを作成
            coco_data = {
                'images': images,
                'annotations': annotations,
                'categories': categories,
            }
            return coco_data

    def get_next_image_path(self) -> str:
        """次の画像パス取得"""
        with self._lock:
            self._img_idx = min(
                self._img_idx + 1,
                len(self._img_id_manager.ids) - 1
            )
            img_id =  self._img_id_manager.ids[self._img_idx]
            return self._img_id_to_path[img_id]

    def get_prev_image_path(self) -> str:
        """前の画像パス取得"""
        with self._lock:
            self._img_idx = max(self._img_idx - 1, 0)
            img_id =  self._img_id_manager.ids[self._img_idx]
            return self._img_id_to_path[img_id]

    def add_annotation(
        self,
        img_path: str,
        category_id: int,
        mask: np.ndarray,
    ):
        """アノテーション情報の追加"""
        with self._lock:
            # アノテーションID生成
            anno_id = self._anno_id_manager.generate_id()
            
            # 画像パスに対応する画像ID
            img_id = self._img_path_to_id[img_path]

            # マスクをCOCOのRLE形式に変換
            rle = mask_tools.encode(np.asfortranarray(mask.astype(np.uint8)))

            # 面積を計算
            area = mask_tools.area(rle).tolist()

            # bboxを計算
            bbox = mask_tools.toBbox(rle).tolist()

            # アノテーション情報を作成
            anno_info = _AnnotationInfo()
            anno_id.id = anno_id
            anno_info.segmentation = rle
            anno_info.area = area
            anno_info.iscrowd = 0
            anno_info.image_id = img_id
            anno_info.bbox = bbox
            anno_info.catetory_id = category_id

            use_rle = False
            if use_rle:
                raise NotImplementedError
            
                # セグメンテーションマスクをRLE形式でエンコード
                rle = mask_tools.encode(np.asfortranarray(mask))

                # RLEデータをシリアライズ可能な形式に変換
                rle['counts'] = rle['counts'].decode('utf-8')

                # RLEデータをセグメンテーション情報として設定
                anno_info["segmentation"] = rle

            else:
                # マスク領域の輪郭を取得
                contours, _ = cv2.findContours(
                    mask.astype(np.uint8),
                    cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE
                )

                # ポリゴン座標に変換
                segmentation = []
                for contour in contours:
                    contour = contour.flatten().tolist()  # Flattenしてリストに変換
                    if len(contour) > 4:  # 有効なポリゴンのみを追加
                        segmentation.append(contour)

                # ポリゴンデータをセグメンテーション情報として設定
                anno_info['segmentation'] = segmentation
                anno_info['isbox'] = False

            self._anno_id_to_info[anno_id] = anno_info

    def remove_annotation(
        self,
        annotation_id: int
    ):
        """アノテーション情報の削除"""
        with self._lock:
            self._anno_id_manager.remove_id(annotation_id)
            del self._anno_id_to_info[annotation_id]
