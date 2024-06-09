from pathlib import Path
import pandas as pd

if __name__ == '__main__':
    # 測定結果ファイルを列挙
    result_dir = r"X:\taro-arts\sam-gui\.output\20240801_235132"
    measure_files = list(Path(result_dir).glob("*/**/time_measure_rawtime.csv"))

    # ファイルの親ディレクトリ名には測定条件の情報が含まれているのでそのリストを取得
    conditions = [f.parent.name for f in measure_files]

    # 全ての測定結果ファイルを読み込み
    df_list = [pd.read_csv(file) for file in measure_files]

    # 抽出対象の列ヘッダ    
    target_columns = ["set_image", "predict", "total"]
    
    df_map = {}
    for target_column in target_columns:
        df_column_list = [df[target_column] for df in df_list]
        df = pd.concat(df_column_list, axis=1)
        df.columns = conditions
        df_map[target_column] = df

    output_file = Path(result_dir) / "summary.xlsx"
    with pd.ExcelWriter(output_file, mode="w") as writer:
        for sheet_name, df in df_map.items():
            df: pd.DataFrame = df
            df.to_excel(writer, sheet_name=sheet_name)
