
import threading
from tkinter import filedialog

import numpy as np

import sam_annotation._utils as _utils
from ._logger import Logger

class ImageFileContainer:
    """画像コンテナクラス"""

    def __init__(
        self,
        img_root_dir: str = None,
        recursive: bool = True,
    ):
        """_summary_

        Args:
            img_dir (str): 画像ディレクトリ
            recursive (bool): 再帰探索フラグ
        """
        self._lock = threading.RLock()
        self._has_data = False
        self._img_root_dir = ""
        self._img_paths = []
        self._img_idx = -1

        self._initialize(img_root_dir, recursive)

    @property
    def img_root_dir(self) -> str:
        with self._lock:
            return self._img_root_dir

    @property
    def img_paths(self) -> set:
        with self._lock:
            return set(self._img_paths)

    def __len__(self):
        with self._lock:
            return len(self.img_paths)

    def _initialize(
        self,
        img_dir: str,
        recursive: bool
    ):
        with self._lock:
            if img_dir is None:
                img_dir = filedialog.askdirectory()
            if img_dir is None or img_dir == "":
                return

            img_paths = _utils.find_image_files(img_dir, recursive)

            self._img_paths = img_paths
            self._img_root_dir = img_dir
            self._img_idx = 0

    def size(self) -> int:
        with self._lock:
            return len(self._img_paths)

    def empty(self) -> bool:
        with self._lock:
            return self.size() == 0

    def get(self, index=None) -> str:
        with self._lock:
            if self.empty():
                return None

            if index is None:
                index = self._img_idx

            if index < 0 or index >= len(self._img_paths):
                return None

            img_path = self._img_paths[index]
            return img_path
            # img = _utils.load_image(img_path)
            # return img

    # TODO: 周回形式にするか、端まで来たら止めるか、止める場合は最後の要素とNoneどちらを返すか検討する
    
    def get_next(self) -> str:
        with self._lock:
            self._img_idx = min(self._img_idx + 1, self.size() - 1)
            Logger.debug(f"{self._img_idx=}")
            return self.get()

    def get_prev(self) -> str:
        with self._lock:
            self._img_idx = max(self._img_idx - 1, 0)
            Logger.debug(f"{self._img_idx=}")
            return self.get()
