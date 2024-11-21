import flet as ft
import time
import pandas as pd

def main(page: ft.Page):

    search_field = ft.Ref[ft.SearchBar]()
    output_text = ft.Ref[ft.Text]()
    submit_btn = ft.Ref[ft.ElevatedButton]()
    store_dropdown = ft.Ref[ft.Dropdown]()

    # 店舗コードマスタ読み込み（store_code_list.csv）
    sid_master = pd.read_csv("./lib/store_code_list.csv")

    def button_clicked(e):
        output_text.current.value = f"Dropdown value is:  {store_dropdown.current.value}"
        page.update()

    def search_changed(e):
        # 更新
        search_words = search_field.current.value
        applicable_df = sid_master[sid_master['store_name'].str.contains(search_words)]
        search_field.current.controls = [
            ft.ListTile(
                title=ft.Text(row.store_name),
                data=row.store_name,
                on_click=lambda e:print(row.store_name)
                )
            for row in applicable_df.itertuples()
            ]
        # search_field.current.controls = [
        #     ft.ListTile(title=ft.Text(f"Color {i}"), data=i)
        #     for i in range(10)
        # ]
        # print("change")
        page.update()

    page.add(
        ft.SearchBar(ref=search_field,
                     view_elevation=4,
                     bar_hint_text="店舗名",
                     width=200,
                     on_change=search_changed,
                     
                     ),
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
