import threading
from pathlib import Path

import numpy as np
import cv2

from . import _utils
# from .image_container import ImageFileContainer
from .annotation_repository import AnnotationRepository
from .key_const import *
from ._logger import Logger
from .sam_predictor_wrapper import SamPredictorWrapper

# SAMのチェックポイントを配置しているディレクトリへのパス
_SAM_CHECKPOINT_DIR = "./weights"

# SAMの各モデルタイプに対応するチェックポイント
_SAM_CHECKPOINT_MAP = {
    "vit_h": f"{_SAM_CHECKPOINT_DIR}/sam_vit_h_4b8939.pth",
    "vit_l": f"{_SAM_CHECKPOINT_DIR}/sam_vit_l_0b3195.pth",
    "vit_b": f"{_SAM_CHECKPOINT_DIR}/sam_vit_b_01ec64.pth",
}

# SAMのモデルタイプ
_SAM_MODEL_TYPES = list(_SAM_CHECKPOINT_MAP.keys())

# ウィンドウプロパティのマップ
# cv2.WindowPropertyFlags
_WND_PROP_MAP = {
    "WND_PROP_FULLSCREEN": cv2.WND_PROP_FULLSCREEN,
    "WND_PROP_AUTOSIZE": cv2.WND_PROP_AUTOSIZE,
    "WND_PROP_ASPECT_RATIO": cv2.WND_PROP_ASPECT_RATIO,
    "WND_PROP_OPENGL": cv2.WND_PROP_OPENGL,
    "WND_PROP_VISIBLE": cv2.WND_PROP_VISIBLE,
    "WND_PROP_TOPMOST": cv2.WND_PROP_TOPMOST,
    "WND_PROP_VSYNC": cv2.WND_PROP_VSYNC,
}

# TODO 排他制御がきちんと考慮できてないかもしれないので後で確認する
# TODO 描画系の処理は別のソースファイルに移せないか検討する
# TODO 各ウィンドウの処理が1つのクラス内に集まりすぎているのでウィンドウごとにクラス分けるようにする
# TODO マウスクラスの実装をするか検討する
# TODO キーボードクラスの実装をするか検討する
# TODO 結果出力クラスを実装するか検討する（アノテーションクラスをそれにするか？）



class MainApp:
    """メインアプリケーションクラス"""

    @property
    def name(self): return self._winname_overlay

    @property
    def alive(self):
        """生存フラグのゲッター"""
        with self._lock:
            return self._alive

    @alive.setter
    def alive(self, val: bool):
        """生存フラグのセッター"""
        with self._lock:
            self._alive = val

    def __init__(self, args):
        """コンストラクタ"""

        # 排他制御オブジェクト
        self._lock = threading.RLock()

        # ウィンドウ名
        winname: str = "SAM Annotation"
        self._winname_overlay = winname + ": overlay"
        self._winname_mask = winname + ": mask"

        # ウィンドウ生存フラグ
        self._alive = None

        # キー待機時間（０以下は永久に待機）
        self._delay = 10

        # ウィンドウ画像
        self._input_img_rgb = np.ones((240, 320, 3), np.uint8) * 128

        # セグメンテーション結果のマスク画像
        self._segment_mask = np.zeros((240, 320), bool)

        # 画像ファイルコンテナ
        self._anno_repository = None

        # 入力画像パス
        self._input_img_path = None

        # SAM推論インスタンス
        self._sam_predictor = None

        # SAMnのモデルタイプ
        assert args.model_type in _SAM_MODEL_TYPES
        self._model_type = args.model_type

        # 入力画像フォルダパス
        self._input_img_dir = args.input_img_dir

        # 処理結果の出力先フォルダパス
        self._output_root_dir = args.output_root_dir

        # 初期化処理
        self._initialize()

    def __del__(self):
        """デストラクタ"""
        with self._lock:
            try:
                self._deinitialize()
            except:
                pass

    def _initialize(self):
        """初期化"""

        with self._lock:

            # SAM推論インスタンスの生成
            # model_type = SAM_MODEL_TYPES[0]
            model_type = "vit_b"
            model_checkpoint = _SAM_CHECKPOINT_MAP[model_type]
            self._sam_predictor = SamPredictorWrapper(
                model_type=model_type,
                checkpoint=model_checkpoint,
                device='cuda'
            )

            # ウィンドウ生成
            # cv2.WindowFlags
            # - WINDOW_NORMAL: int
            # - WINDOW_AUTOSIZE: int (default)
            # - WINDOW_OPENGL: int
            # - WINDOW_FULLSCREEN: int
            # - WINDOW_FREERATIO: int
            # - WINDOW_KEEPRATIO: int
            # - WINDOW_GUI_EXPANDED: int
            # - WINDOW_GUI_NORMAL: int
            flags = cv2.WINDOW_GUI_NORMAL
            cv2.namedWindow(self._winname_overlay, flags=flags)
            cv2.namedWindow(self._winname_mask, flags=flags)

            # アスペクト比が1になるようにする
            self._set_window_property(
                prop_id=_WND_PROP_MAP["WND_PROP_ASPECT_RATIO"],
                prop_value=1.0
            )

            # 画像ディレクトリの選択
            self._select_img_dir()

            # マウスコールバックの登録
            self._set_mouse_callback(self._mouse_callbck)

    def _deinitialize(self):
        """終了処理"""
        with self._lock:
            # ウィンドウの破棄
            # desroyAllWindowsで破棄済みの可能性を考慮してtryで囲む
            try:
                cv2.destroyWindow(self._winname_overlay)
            except:
                pass

    def run(self):
        """メイン処理実行"""
        self.alive = True
        while self.alive:
            # ウィンドウ更新
            self._update_window()

            # キーイベント処理
            self._process_key()

            # ウィンドウを閉じるとWND_PROP_VISIBLEがFalseになるので
            # その時はループを抜ける
            if not bool(self._get_window_propaties()["WND_PROP_VISIBLE"]):
                break
            
    def _stop_run_loop(self):
        """メインループ停止"""
        with self._lock:
            self.alive = False

    def _process_key(self):
        """キーイベント処理"""
        with self._lock:
            # key = cv2.pollKey()
            key = cv2.waitKeyEx(self._delay)
            key_ = KEYMAP.get(key, "UNKNOWN")
            Logger.debug(f"{key_=} ({key}) [{hex(key)}]")

            if key < 0:  # キー押下なし
                return

            if key == KEY_ESCAPE:  # ESC
                # 終了
                self._stop_run_loop()
            elif key == KEY_ENTER:
                pass
            elif key == KEY_DELETE:
                # 現在のSAM結果をクリア
                self._clear_sam_result()
            elif key == KEY_RIGHT_ARROW:
                # 次の画像をロード
                self._save()
                self._load_next_image()
            elif key == KEY_LEFT_ARROW:
                # 前の画像をロード
                self._save()
                self._load_prev_image()
            elif key == KEY_S:
                # 保存
                self._save()
            elif key == KEY_E:
                # エクスポート
                self._save()
            else:
                pass

    def _save(self):
        # TODO 実装
        pass

    def _mouse_callbck(
        self,
        event: int,
        x: int,
        y: int,
        flags: int,
        userdata
    ):
        """マウスのコールバック"""
        with self._lock:
            _MOUSE_EVENT_MAP = {
                cv2.EVENT_MOUSEMOVE: "EVENT_MOUSEMOVE",
                cv2.EVENT_LBUTTONDOWN: "EVENT_LBUTTONDOWN",
                cv2.EVENT_RBUTTONDOWN: "EVENT_RBUTTONDOWN",
                cv2.EVENT_MBUTTONDOWN: "EVENT_MBUTTONDOWN",
                cv2.EVENT_LBUTTONUP: "EVENT_LBUTTONUP",
                cv2.EVENT_RBUTTONUP: "EVENT_RBUTTONUP",
                cv2.EVENT_MBUTTONUP: "EVENT_MBUTTONUP",
                cv2.EVENT_LBUTTONDBLCLK: "EVENT_LBUTTONDBLCLK",
                cv2.EVENT_RBUTTONDBLCLK: "EVENT_RBUTTONDBLCLK",
                cv2.EVENT_MBUTTONDBLCLK: "EVENT_MBUTTONDBLCLK",
                cv2.EVENT_MOUSEWHEEL: "EVENT_MOUSEWHEEL",
                cv2.EVENT_MOUSEHWHEEL: "EVENT_MOUSEHWHEEL",
            }

            if event == cv2.EVENT_MOUSEMOVE:
                pass
            elif event == cv2.EVENT_LBUTTONDOWN:
                pass
            elif event == cv2.EVENT_RBUTTONDOWN:
                pass
            elif event == cv2.EVENT_MBUTTONDOWN:
                pass
            elif event == cv2.EVENT_LBUTTONUP:
                self._sam_predictor.set_prompt_point(x, y)
                self._run_sam_prediction()
            elif event == cv2.EVENT_RBUTTONUP:
                pass
            elif event == cv2.EVENT_MBUTTONUP:
                pass
            elif event == cv2.EVENT_LBUTTONDBLCLK:
                pass
            elif event == cv2.EVENT_RBUTTONDBLCLK:
                pass
            elif event == cv2.EVENT_MBUTTONDBLCLK:
                pass
            elif event == cv2.EVENT_MOUSEWHEEL:
                pass
            elif event == cv2.EVENT_MOUSEHWHEEL:
                pass
            else:
                # raise NotImplementedError()
                pass

            flag_name = "EVENT_FLAG"
            if flags & cv2.EVENT_FLAG_LBUTTON:
                flag_name += "+LBUTTON"
            if flags & cv2.EVENT_FLAG_RBUTTON:
                flag_name += "+RBUTTON"
            if flags & cv2.EVENT_FLAG_MBUTTON:
                flag_name += "+MBUTTON"
            if flags & cv2.EVENT_FLAG_CTRLKEY:
                flag_name += "+CTRLKEY"
            if flags & cv2.EVENT_FLAG_SHIFTKEY:
                flag_name += "+SHIFTKEY"
            if flags & cv2.EVENT_FLAG_ALTKEY:
                flag_name += "+ALTKEY"

            Logger.debug(
                f"{self._winname_overlay=}: {event=} ({_MOUSE_EVENT_MAP[event]}), "
                f"{x=}, {y=}, {flags=} ({flag_name}), {userdata=}")

    def _select_img_dir(self, img_dir=None):
        """画像ディレクトリの選択"""
        with self._lock:
            # 画像ディレクトリパスがNoneのときは内部でフォルダダイアログが出る
            annotation_repository = AnnotationRepository()
            annotation_repository.initialize(
                img_root_dir=self._input_img_dir,
                recursive=False,
                coco_file=None,
            )
            if len(annotation_repository.image_paths) <= 0:
                raise RuntimeError("No image file found.")
            self._anno_repository = annotation_repository

            # 最初の画像をロード
            self._load_next_image()

    def _load_next_image(self):
        """次の画像をロード"""
        with self._lock:
            img_path = self._anno_repository.get_next_image_path()
            self._update_window_image(img_path)

    def _load_prev_image(self):
        """前の画像をロード"""
        with self._lock:
            img_path = self._anno_repository.get_prev_image_path()
            self._update_window_image(img_path)

    def _run_sam_prediction(self):
        """SAM推論の実行"""
        with self._lock:
            # SAMのプロンプト指定
            # points = np.array([[x, y]])
            # self._sam_predictor.set_prompt_points(
            #     point_coords=points,
            #     point_labels=None,
            # )

            # SAMセグメンテーション実行
            masks = self._sam_predictor.predict(
                multimask_output=False,
            )

            Logger.debug(f"{masks.shape=}, {masks.dtype=}")
            self._segment_mask = masks[0]
            self._update_window()

    def _clear_sam_result(self):
        """SAM推論結果のクリア"""
        with self._lock:
            # セグメンテーション結果のクリア
            if self._segment_mask is not None:
                self._segment_mask[:] = False
                self._update_window()

    def _update_window_image(self, img_path):
        """ウィンドウ画像更新"""

        with self._lock:
            if self._input_img_path != img_path:
                self._input_img_path = img_path

                # 入力画像パスが変わったときは読み込み
                rgb_img = _utils.load_image(self._input_img_path)
                self._input_img_rgb = rgb_img
                self._segment_mask = np.zeros(rgb_img.shape[:2], bool)

                # 読み込んだ画像をSAMにエンコード
                self._sam_predictor.set_image(rgb_img, img_format="RGB")

                # SAM結果をクリア
                self._clear_sam_result()

            self._update_window()

    def _update_window(self):
        """ウィンドウ更新"""
        with self._lock:
            # セグメンテーション結果のマスクを重畳
            overlay_img_rgb = _utils.apply_colored_mask(
                self._input_img_rgb,
                self._segment_mask,
                color=(0, 0, 255),
                alpha=0.5,
            )
            overlay_img_bgr = cv2.cvtColor(overlay_img_rgb, cv2.COLOR_RGB2BGR)

            cv2.imshow(
                self._winname_overlay,
                overlay_img_bgr
            )

            cv2.imshow(
                self._winname_mask,
                self._segment_mask.astype(np.uint8) * 255
            )

            # TODO: ファイル保存が毎回走るので保存タイミングを見直す
            # result_data = {
            #     "overlay": (overlay_img_rgb, ".jpg"),
            #     "segment": (self._segment_mask.astype(np.uint8) * 255, ".png")
            # }
            # self._output_result_images(result_data)

    def _output_result_images(self, result_img_map: dict):
        """結果をファイル出力"""
        with self._lock:
            if self._output_root_dir is None:
                return

            # TODO: この出力処理はもう少し整理しておきたい
            input_img_path = Path(self._input_img_path).absolute()
            input_root_dir = Path(
                self._anno_repository.img_root_dir).absolute()
            output_root_dir = Path(self._output_root_dir).absolute()

            output_path_base = str(input_img_path).replace(
                str(input_root_dir.parent),
                str(output_root_dir) + "/"
            )

            for key, (img, ext) in result_img_map.items():
                output_img_path = Path(output_path_base).with_stem(
                    input_img_path.stem + f"_{key}"
                )
                output_img_path = output_img_path.with_suffix(ext)

                Logger.debug(f"{output_img_path=}")
                _utils.save_image(output_img_path, img)

    def _set_window_title(self, title: str):
        """ウィンドウタイトル更新"""
        with self._lock:
            cv2.setWindowTitle(self._winname_overlay, title=title)

    def _move_window(self, x: int, y: int):
        """ウィンドウ移動"""
        with self._lock:
            cv2.moveWindow(self._winname_overlay, x, y)

    def _resize_window(self, width: int, height: int):
        """ウィンドウのリサイズ"""
        with self._lock:
            cv2.resizeWindow(self._winname_overlay, width, height)

    def _get_window_image_rect(self):
        """ウィンドウ画像の矩形情報の取得"""
        with self._lock:
            rect = cv2.getWindowImageRect(self._winname_overlay)
            return rect

    def _get_window_propaties(self):
        """ウィンドウプロパティ一覧の取得"""
        with self._lock:
            props = {}
            for key, prop_id in _WND_PROP_MAP.items():
                try:
                    props[key] = self._get_window_propaty(prop_id)
                except:
                    props[key] = None
            return props

    def _set_window_property(self, prop_id: int, prop_value: float):
        """ウィンドウプロパティの設定"""
        with self._lock:
            cv2.setWindowProperty(self._winname_overlay, prop_id, prop_value)
            cv2.setWindowProperty(self._winname_mask, prop_id, prop_value)

    def _get_window_propaty(self, prop_id: int):
        """ウィンドウプロパティの取得"""
        with self._lock:
            return cv2.getWindowProperty(self._winname_overlay, prop_id)

    def _create_trackbar(
        self,
        trackbarname: str,
        val: int,
        minval: int,
        maxval: int,
        callback
    ):
        """トラックバー生成"""
        with self._lock:
            # callback(pos: int)
            cv2.createTrackbar(
                trackbarname, self._winname_overlay, val, maxval, callback)
            cv2.setTrackbarMin(
                trackbarname, self._winname_overlay, minval=minval)
            cv2.setTrackbarMax(
                trackbarname, self._winname_overlay, maxval=maxval)
            cv2.setTrackbarPos(trackbarname, self._winname_overlay, pos=val)
            pos = cv2.getTrackbarPos(trackbarname, self._winname_overlay)
            assert pos == val

    def _set_mouse_callback(self, callback):
        """マウスコールバックの設定"""
        with self._lock:
            # callback(event: int, x: int, y: int, flags: int)
            cv2.setMouseCallback(self._winname_overlay, callback)

    if False:
        def _trackbar_callback_dummy(self, pos):
            """トラックバーのデバッグ用コールバック"""
            with self._lock:
                Logger.debug(f"{self._name=}, {pos=}")
