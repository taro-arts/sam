import argparse
import tkinter as tk
from tkinter import filedialog, messagebox

from sam_annotation import MainApp

from dataclasses import dataclass

@dataclass
class CommandLineArguments:
    model_type: str = ""
    input_img_dir: str = ""
    output_root_dir: str = ""

def get_args() -> CommandLineArguments:
    """コマンドライン引数の取得"""
    
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model_type",
        default="vit_b",
        type=str,
        choices=["vit_h", "vit_l", "vit_b"],
        # help="(default: 'vit_h')"
    )
    
    # TODO パラメータにモデルのチェックポイント追加するか検討
    # parser.add_argument(
    #     "--model_checkpoint",
    #     default="weights/sam_vit_h_4b8939.pth",
    #     type=str,
    #     # help=""
    # )
    
    parser.add_argument(
        "--input_img_dir",
        default="./images",
        type=str,
        # help=""
    )

    parser.add_argument(
        "--output_root_dir",
        default=".result",
        type=str,
        # help=""
    )
    
    # TODO パラメータにログレベル追加
    # parser.add_argument(
    #     "--log_level",
    #     default=2,
    #     type=int,
    #     choices=[0, 1, 2, 3, 4, 5],
    # )
    # import logging
    # logging.CRITICAL # FATAL
    # logging.ERROR
    # logging.WARNING
    # logging.INFO
    # logging.DEBUG
    # logging.NOTSET
    
    import logging
    logging.CRITICAL
    
    args = parser.parse_args()
    return CommandLineArguments(**args.__dict__)


if __name__ == '__main__':
    # コマンドライン引数の取得
    # TODO: 余力あればコマンドラインからでなくGUIコントロールからでも指定できるようにする
    args = get_args()
    print(f"{args=}")
    
    # メイン処理実行
    win = MainApp(args)
    win.run()
