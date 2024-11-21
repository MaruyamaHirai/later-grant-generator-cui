import pandas as pd
import re
from pprint import pprint
from os import makedirs,rename
from datetime import datetime,timedelta

# ポイントコードマスタ読み込み（point_code_list.csv）
pid_master = pd.read_csv("./lib/point_code_list.csv")
# 店舗コードマスタ読み込み（store_code_list.csv）
sid_master = pd.read_csv("./lib/store_code_list.csv")

# データを格納するための空のリストを作成
data = []

# ファイル名用日付
datetime_now = datetime.now()

while True:
    
    input_pcid = ""
    input_store = ""

    # ループ：ポイントカードID
    while True:
        # ポイントカードID入力
        input_pcid = input("ポイントカードIDを入力して下さい(0始まり10桁数字) : ")
        
        # ■入力チェック
        if re.match("^[A-Z0-9]{10}$", input_pcid):
            # クリア→店舗コード入力へ
            break
        else:
            # フォーマットエラー→再入力
            print("エラー: 0始まりの半角数字10桁で入力して下さい")

    # ループ：店舗コード
    while True:
        # 店舗コード入力
        input_store = input("店舗コードを入力して下さい(2桁英大文字/数字) : ")

        # ■入力チェック
        if re.match("^[0-9][A-Z0-9]$", input_store):
            
            # マスタから店舗読み込み
            row = sid_master.loc[sid_master['store_code'] == input_store]
            # 店舗コード該当なしエラー→再入力
            if row.empty:
                print("エラー: 該当の店舗が存在しません")
                continue
            # 店舗名表示
            print(row.iat[0,0],row.iat[0,1])

            # クリア→ポイントコード入力へ
            break
        else:
            # フォーマットエラー→再入力
            print("エラー: 半角英数字2桁で入力してください")

    # ループ：ポイントコード
    # ＊同じ顧客で複数付与がある場合もここでループ
    print("ポイントコードを入力してください (Aを抜いた4桁数字)。連続入力をやめる場合は end を入力してください")
    i = 1 # 複数付与カウント
    while True:
        # ポイントコード入力
        input_pcode = input(f"[{input_pcid},{i}件目]  : A ")

        # ■入力チェック
        if re.match("^[0-9]{4}$", input_pcode):
            # マスタからポイント読み込み
            input_pcode = "A" + input_pcode
            row = pid_master.loc[pid_master['point_code'] == input_pcode]
            # ポイントコード該当なしエラー→再入力
            if row.empty:
                print("エラー: 該当のポイントコードが存在しません")
                continue
            print(row.iat[0,0],row.iat[0,1],row.iat[0,2],"pt")
            input_point = row['point'].values[0]

            # ポイントを整形（7文字空白詰め）
            input_point = str(input_point).rjust(7)

            # クリア→リストに格納
            data.append([input_pcid,input_pcode,input_store,"",input_point])
            i += 1

        elif input_pcode == "end":
            # データ入力終了
            break
        else:
            # フォーマットエラー→再入力
            print("エラー: Aを除いた半角数字4桁で入力してください")
    
    # 確認処理
    print("==================================================")
    print("■現在のデータ：")
    pprint(data)
    print("==================================================")

    # 終了処理

    # ■日付分岐
    # ・昼前の後日付与実行前（00:00~11:25）→ スクリプト実行"当日"
    # ・　　”　　　　 実行後（11:25~24:00）→ スクリプト実行"翌日"
    date = ""
    # 当日
    if datetime_now.strftime("%H:%M:%S") <= "11:25:00":
        date = datetime_now.strftime('%Y%m%d')
    # 翌日
    else:
        date = datetime_now + timedelta(days=1)
        date = date.strftime('%Y%m%d')
    # 日付のディレクトリを作成
    makedirs(f"./data/{date}",exist_ok=True)
    
    # リストをDataFrameに変換
    df = pd.DataFrame(data)
    # DataFrameをCSVファイルに出力
    df.to_csv(f'./data/{date}/手動付与用_POINT_{datetime_now.strftime("%Y%m%d")}.csv', index=False, header=False)

    print("CSVファイルを更新しました。")

    if input("入力処理を継続しますか？ (y/n) : ") == "n":
        # 処理終了
        break



