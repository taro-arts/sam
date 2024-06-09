import threading

class IDManager:
    """ID管理クラス"""
    def __init__(self):
        self._thread = threading.RLock()
        self._ids = []
        self._id = 1
        
    @property
    def ids(self):
        return self._ids
    
    def generate_id(self) -> int:
        """ID生成"""
        with self._thread:
            # 未存在のIDを探索
            while self._id in self._ids:
                self._id += 1
            self.push_id(self._id)
            return self._id

    def add_id(self, id_: int):
        """指定IDを末尾に追加"""
        with self._thread:
            if id_ in self._ids:
                raise ValueError
            self._ids.append(id_)

    def remove_id(self, id_: int):
        """末尾のIDを削除"""
        with self._thread:
            self._ids.remove(id_)
       
    def push_id(self, id_: int):
        """指定IDを末尾に追加"""
        with self._thread:
            if id_ in self._ids:
                raise ValueError
            self._ids.append(id_)

    def pop_id(self):
        """末尾のIDを削除"""
        with self._thread:
            del self._ids[-1]


    # TODO 適切なデータ構造を検討（スタック、FIFO、ツリーなどが考えられる）