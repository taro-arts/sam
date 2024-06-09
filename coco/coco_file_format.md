# COCO ファイルフォーマット

https://cocodataset.org/#format-data

COCOはタスクに応じたアノテーションタイプが存在する
- オブジェクト検出
- キーポイント検出
- スタッフセグメンテーション
- パノプティックセグメンテーション
- デンスポーズ
- 画像キャプション

## 基本構造

| セクション  | 説明                                         | データ型 |
| ----------- | -------------------------------------------- | -------- |
| info        | データセット全体に関する基本的なメタデータ   | dict     |
| licenses    | 各画像に適用されるライセンス情報             | list     |
| images      | 各画像に関するメタデータ                     | list     |
| annotations | 各画像に対するアノテーション情報             | list     |
| categories  | データセットに含まれる各カテゴリに関する情報 | list     |


```json
{
    "info": {...},
    "licenses": [...],
    "images": [...],
    "annotations": [...],
    "categories": [...]
}
```
※各要素の詳細は以降に記載

## タスク共通

### info

※AI学習においては基本的に必要ないデータ

| 要素名       | 説明                                                          | データ型 |
| ------------ | ------------------------------------------------------------- | -------- |
| year         | データセットが作成された年                                    | int      |
| version      | データセットのバージョン                                      | str      |
| description  | データセットの説明                                            | str      |
| contributor  | データセットの作成に貢献した人や団体の名前                    | str      |
| url          | データセットに関する詳細情報が記載されているウェブサイトのURL | str      |
| date_created | データセットが作成された日付 ("YYYY/MM/DD")                   | datetime |

```json
{
    "info": {
        "year": 2021,
        "version": "1.0",
        "description": "XXX Dataset",
        "contributor": "Example Contributor",
        "url": "http://example.com",
        "date_created": "2021/06/15"
    }
}
```
### images

| 要素名        | 説明                           | データ型 |
| ------------- | ------------------------------ | -------- |
| id            | 画像の一意の識別子             | int      |
| width         | 画像の幅（ピクセル単位）       | int      |
| height        | 画像の高さ（ピクセル単位）     | int      |
| file_name     | 画像ファイルの名前             | str      |
| license       | 画像に適用されるライセンスのID | int      |
| flickr_url    | FlickrデータセットのURL        | str      |
| coco_url      | COCOデータセットのURL          | str      |
| date_captured | 画像が撮影された日付           | datetime |

```json
{
    "images": [
        {
            "id": 1,
            "width": 640,
            "height": 480,
            "file_name": "example_image.jpg",
            "license": 1,
            "flickr_url": "http://farm1.staticflickr.com/1/00000000001_abcdef.jpg",
            "coco_url": "http://images.cocodataset.org/val2017/000000000001.jpg",
            "date_captured": "2021/06/01",
        }
    ]
}
```
### licenses
※AI学習においては基本的に必要ないデータ

| 要素名 | 説明                                                        | データ型 |
| ------ | ----------------------------------------------------------- | -------- |
| id     | ライセンスの一意の識別子                                    | int      |
| name   | ライセンスの名前                                            | str      |
| url    | ライセンスに関する詳細情報が記載されているウェブサイトのURL | str      |

```json
{
    "licenses": [
        {
            "id": 1,
            "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
            "name": "Attribution-NonCommercial-ShareAlike License"
        },
        {
            "id": 2,
            "url": "http://creativecommons.org/licenses/by-nc/2.0/",
            "name": "Attribution-NonCommercial License"
        },
    ]
}
```


## 物体検出のアノテーション

### annotations

| 要素名       | 説明                                                      | データ型         |
| ------------ | --------------------------------------------------------- | ---------------- |
| id           | アノテーションの一意の識別子                              | int              |
| image_id     | 対応する画像のID                                          | int              |
| category_id  | アノテーションが属するカテゴリのID                        | int              |
| segmentation | セグメンテーション情報 (RLEまたはポリゴン座標のリスト)    | RLE or [polygon] |
| area         | アノテーションの領域面積                                  | float            |
| bbox         | バウンディングボックス ([x, y, width, height])            | list             |
| iscrowd      | アノテーションが群集であるかどうかを示すフラグ (0または1) | int (0 or 1)     |

- 単一オブジェクト（iscrowd=0）：
  - ポリゴンを使用
  - 複数ポリゴンになる場合もある
- 複数オブジェクト（iscrowd=1）：
  - RLEを使用
  - 人々の群衆などのオブジェクトグループのラベル付けに使用
- バウンディングボックス：
  - 画像の左上から測定
  - 0-indexed

- [ ] RLEのデータ型？
- [ ] ポリゴン座標のリスト？
- [ ] バウンディングボックスの要素のデータ型？

```json
{
    "annotations": [
        {
            "id": 1,
            "image_id": 1,
            "category_id": 1,
            "segmentation": [[100.0, 100.0, 200.0, 100.0, 200.0, 200.0, 100.0, 200.0]],
            "area": 10000.0,
            "bbox": [100.0, 100.0, 100.0, 100.0],
            "iscrowd": 0
        }
    ]
}
```



### categories

| 要素名        | 説明                   | データ型 |
| ------------- | ---------------------- | -------- |
| id            | カテゴリの一意の識別子 | int      |
| name          | カテゴリの名前         | str      |
| supercategory | カテゴリの上位カテゴリ | str      |

```json
{
    "categories": [
        {
            "id": 1,
            "name": "person",
            "supercategory": "human",
        }
    ]
}
```
## キーポイント検出のアノテーション

物体検出のアノテーション情報（IDやバウンディングボックスなど）に追加で＋２個のフィールドがある

- 各カテゴリのカテゴリ構造体には、2つの追加フィールドが含まれる
  - 「keypoints」
    - キーポイント名の長さkの配列
  - 「skeleton」
    - キーポイントエッジペアのリストを介して接続性を定義
    - 視覚化に使用される
- 現在、キーポイントは人物カテゴリに対してのみラベル付けされている
  - ほとんどの中規模/大規模の非群衆人物インスタンスの場合

### annotations

| 要素名        | 説明                                                   | データ型 |
| ------------- | ------------------------------------------------------ | -------- |
| num_keypoints | キーポイント数 k                                       | int      |
| keypoints     | キーポイントの配列（長さ3k個の配列） [x1, y1, v1, ...] | list     |
| [cloned]      | ※物体検出と同じアノテーション情報                     | -        |


- keypoints
  - 各キーポイントには以下が含まれる
    - 位置x、y（0から始まる）
    - 可視性フラグv
      - v=0: ラベルなし（この場合 x=y=0）
      - v=1: ラベル付きだが可視ではない
      - v=2: ラベル付きで可視
  - キーポイントは、オブジェクトセグメント内にある場合、可視とみなされる
- num_keypoints
  - 特定のオブジェクトのラベル付きキーポイントの数（v>0）
  - 群衆や小さなオブジェクトなど、多くのオブジェクトでは num_keypoints=0 になる

### categories

| 要素名    | 説明                                                    | データ型 |
| --------- | ------------------------------------------------------- | -------- |
| keypoints | キーポイントの名前のリスト                              | 配列     |
| skeleton  | スケルトンを形成する2つのキーポイントのIDのペアのリスト | 配列     |
| [cloned]  | ※物体検出アノテーション                      | -        |

```json
{
    "annotations": [
        {
            "num_keypoints": ...,
            "keypoints": ...,
            "[cloned]": ...,
        }
    ],
    "categories": [
        {
            "keypoints": [
                "nose",
                "left_eye",
                "right_eye",
                "left_ear",
                "right_ear",
                "left_shoulder",
                "right_shoulder",
                "left_elbow",
                "right_elbow",
                "left_wrist",
                "right_wrist",
                "left_hip",
                "right_hip",
                "left_knee",
                "right_knee",
                "left_ankle",
                "right_ankle"
            ],
            "skeleton": [
                [16,14],
                [14,12],
                [17,15],
                [15,13],
                [12,13],
                [6,12],
                [7,13],
                [6,7],
                [6,8],
                [7,9],
                [8,10],
                [9,11],
                [2,3],
                [1,2],
                [1,3],
                [2,4],
                [3,5],
                [4,6],
                [5,7]
            ],

            "[cloned]": ...,
        }
    ]
}
```

### スタッフセグメンテーションのアノテーション

※未確認

- 物体検出のフォーマットと同一
- iscrowdは不要で、デフォルトで0に設定
- 単一のRLEアノテーションでエンコード
- フォーマット間の変換スクリプトあり
- category_id は現在のスタッフカテゴリのID

### パノプティックセグメンテーションのアノテーション

※未確認

```
annotation{
    "image_id": int, 
    "file_name": str, 
    "segments_info": [segment_info],
}

segment_info{
    "id": int,
    "category_id": int,
    "area": int, 
    "bbox": [x,y,width,height],
    "iscrowd": 0 or 1,
}

categories[{
    "id": int, 
    "name": str, 
    "supercategory": str, 
    "isthing": 0 or 1,
    "color": [R,G,B],
}]
```

### 画像キャプションのアノテーション

※未確認

```
annotation{
    "id": int,
    "image_id": int,
    "caption": str,
}
```

### デンスポーズのアノテーション

※未確認

```
annotation{
    "id": int, 
    "image_id": int, 
    "category_id": int, 
    "is_crowd": 0 or 1, 
    "area": int, 
    "bbox": [x,y,width,height], 
    "dp_I": [float], 
    "dp_U": [float], 
    "dp_V": [float], 
    "dp_x": [float], 
    "dp_y": [float], 
    "dp_masks": [RLE],
}
```

## 補足

### COCO API

COCO API でアノテーションデータのアクセスや操作
https://github.com/cocodataset/cocoapi



## 参考

https://cocodataset.org/