import threading

from segment_anything import SamPredictor, sam_model_registry
from segment_anything.modeling import Sam
import numpy as np
import torch

# TODO: スレッド利用有無の切り替えができるようにする

class SamPredictorWrapper:
    """SamPredictorクラスのラッパー"""

    def __init__(
        self,
        model_type: str,
        checkpoint: str,
        device: str,
    ):
        """コンストラクタ

        Args:
            model_type (str): モデルタイプ（"vit_h", "vit_l", or "vit_b"）
            checkpoint (str): モデルの重みパラメータファイルへのパス
        """
        self._lock = threading.RLock()

        self._thread_set_image = None

        # Samインスタンス
        self._sam: Sam = None

        # SamPredictorインスタンス
        self._predictor: SamPredictor = None

        # Sam埋め込みを算出する画像
        self._img = None

        # Samに与えるプロンプト
        self._prompt = {
            "point_coords": None,
            "point_labels": None,
            "box": None,
        }

        self._model_type = model_type
        self._checkpoint = checkpoint
        self._device = device if torch.cuda.is_available() else 'cpu'

        self._initialize(
            model_type,
            checkpoint,
        )

    def __del__(
        self
    ):
        """デストラクタ"""
        with self._lock:
            # TODO: GPUメモリキャッシュの明示的な解放処理を入れる
            pass

    @property
    def prompt(self):
        with self._lock:
            return self._prompt

    def _initialize(
        self,
        model_type: str,
        checkpoint: str
    ):
        """初期化"""
        with self._lock:
            assert model_type in ("vit_h", "vit_l", "vit_b")
            build_sam = sam_model_registry[model_type]
            self._sam = build_sam(checkpoint)
            self._sam.to(self._device)
            self._predictor = SamPredictor(sam_model=self._sam)

    def set_image(
        self,
        img: np.ndarray,
        img_format: str,
    ):
        """画像エンコード

        Args:
            img (np.ndarray): 画像
            img_format (str): 画像フォーマット（'RGB' or 'BGR'）
        """
        # with self._lock:
        #     self._predictor.set_image(img, image_format=img_format)
        #     # TODO: マルチスレッド化
        with self._lock:
            self._thread_set_image = threading.Thread(
                target=self._set_image_thread,
                args=(img.copy(), img_format)
            )
            self._thread_set_image.start()

    def _set_image_thread(self, img, img_format):
        """画像埋め込みのスレッド関数"""
        with self._lock:
            self._predictor.set_image(img, image_format=img_format)
            # TODO: マルチスレッド化

    def set_prompt_point(
        self,
        x: int,
        y: int,
        label: int = 1
    ):
        """プロンプトに与えるポイントの指定

        Args:
            x (int): X座標
            y (int): Y座標
            label (int): ポイントの前景・背景ラベル（1: 前景、0: 背景）
        """
        with self._lock:
            self._prompt["point_coords"] = np.array([[x, y]])
            self._prompt["point_labels"] = np.array([label])
            
    def set_prompt_points(
        self,
        point_coords: np.ndarray,
        point_labels: np.ndarray = None,
    ):
        """プロンプトに与えるポイントリストの指定

        Args:
            point_coords (np.ndarray): ポイントの座標リスト
            point_labels (np.ndarray): ポイントの前景・背景ラベルリスト（1: 前景、0: 背景）
                Noneの場合、ポイントはすべて前景扱いとする
        """
        with self._lock:
            # 前景・背景ラベルの指定がないときは前景扱いとする
            if point_labels is None:
                point_labels = np.ones((len(point_coords),), np.int32)

            self._prompt["point_coords"] = point_coords
            self._prompt["point_labels"] = point_labels

    def set_prompt_box(
        self,
        box: np.ndarray  # [x0, y0, x1, y1]形式 ([x0, y0, w, h] ではない)
    ):
        """プロンプトに与えるボックスの指定

        Args:
            box (np.ndarray): ボックス（XYXY形式で指定。XYWH形式ではない）
        """
        with self._lock:
            self._prompt["box"] = box

    def set_prompt(
        self,
        point_coords: np.ndarray = None,
        point_labels: np.ndarray = None,
        box: np.ndarray = None,
    ):
        """プロンプト指定

        Args:
            point_coords (np.ndarray): ポイントの座標リスト
            point_labels (np.ndarray): ポイントの前景・背景ラベルリスト（1: 前景、0: 背景）
            box (np.ndarray): ボックス（XYXY形式で指定。XYWH形式ではない）
        """
        with self._lock:
            if point_coords is not None:
                self.set_prompt_points(point_coords, point_labels)
            if point_labels is not None:
                self.set_prompt_box(box)

    def predict(
        self,
        multimask_output: bool = False,
    ) -> np.ndarray:
        """推論実行

        Args:
            multimask_output (bool): 複数マスク出力フラグ
                Trueの場合、3種類のマスクが出力される

        Returns:
            np.ndarray: 単一または複数のマスク
        """
        with self._lock:
            if self._thread_set_image is None:
                return None
            
            masks, scores, logits = self._predictor.predict(
                **self._prompt,
                # point_coords=None,
                # point_labels=None,
                # box=None,
                mask_input=None,
                multimask_output=multimask_output,
                return_logits=False,
            )

            return masks
