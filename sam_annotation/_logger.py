
# NOTE: 手抜きのロガークラスなので後で余力があれば中身をきちんとしたものにする

# import logging
# import warnings

class Logger:
    """ロガークラス"""
    def __init__(self):
        pass

    @classmethod
    def debug(cls, msg: str):
        print(msg)

    @classmethod
    def info(cls, msg: str):
        print(msg)

    @classmethod
    def warn(cls, msg: str):
        print(msg)
    
    @classmethod
    def error(cls, msg: str):
        print(msg)
    
    @classmethod
    def critical(cls, msg: str):
        print(msg)

