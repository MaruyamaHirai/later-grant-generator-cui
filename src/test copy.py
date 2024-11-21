import flet as ft
import time
import pandas as pd

def main(page: ft.Page):

    search_field = ft.Ref[ft.TextField]()
    output_text = ft.Ref[ft.Text]()
    submit_btn = ft.Ref[ft.ElevatedButton]()
    store_dropdown = ft.Ref[ft.Dropdown]()

    # 店舗コードマスタ読み込み（store_code_list.csv）
    sid_master = pd.read_csv("./lib/store_code_list.csv")

    def button_clicked(e):
        output_text.current.value = f"Dropdown value is:  {store_dropdown.current.value}"
        page.update()
    
    def textbox_changed(e):
        # 削除
        for option in store_dropdown.current.options:
            store_dropdown.current.options.remove(option)
        # 更新
        search_words = search_field.current.value
        applicable_df = sid_master[sid_master['store_name'].str.contains(search_words)]
        for row in applicable_df.itertuples():
            store_dropdown.current.options.append(ft.dropdown.Option(row.store_name))
        page.update()

    page.add(
        ft.TextField(ref=search_field, label="店舗名", width=300, on_change=textbox_changed,),
        ft.Dropdown(ref=store_dropdown, width=100, 
            options=[
                ft.dropdown.Option("Red"),
                ft.dropdown.Option("Green"),
                ft.dropdown.Option("Blue"),
            ]),
        ft.ElevatedButton(ref=submit_btn, text="Submit", on_click=button_clicked),
        ft.Text(ref=output_text)
        )
    
ft.app(target=main)
