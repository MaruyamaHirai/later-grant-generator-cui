import csv
import tkinter as tk
from tkinter import messagebox

# CSVファイルに書き込む関数
def write_to_csv(data):
    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

# フォームの値を取得し、CSVに書き込む関数
def submit_form():
    data = []
    for entry in entries:
        data.append([e.get() for e in entry])
    write_to_csv(data)
    messagebox.showinfo("Success", "Data saved to 'output.csv'")

# 新たに行を追加する関数
def add_row():
    row = tk.Frame(root)
    row.pack(side=tk.TOP, padx=5, pady=5)
    tk.Label(row, text="1", width=10).pack(side=tk.LEFT)
    entries.append([tk.Entry(row) for _ in range(5)])
    for e in entries[-1]:
        e.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)

# GUIの作成
root = tk.Tk()


# フォームのエントリー（入力フィールド）を格納するリスト
entries = []

# フォーム生成
row = tk.Frame(root)
row.pack(side=tk.TOP, padx=5, pady=5)
tk.Label(row, text=field, width=10).pack(side=tk.LEFT)
entries.append([tk.Entry(row) for _ in range(5)])  # 5つの入力フィールドを作成
for e in entries[-1]:
    e.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)


# ボタンフレーム
button_fr = tk.Frame(root,relief='solid',bd=1)
button_fr.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

tk.Button(button_fr, text='Submit', command=submit_form).pack(side=tk.RIGHT, anchor=tk.SE, padx=5, pady=5)
tk.Button(button_fr, text='Add Row', command=add_row).pack(side=tk.RIGHT, anchor=tk.SE, padx=5, pady=5)

tk.Entry(button_fr)

root.mainloop()
