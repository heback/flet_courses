import flet as ft


def main(page: ft.Page):
    first_name = ft.TextField()
    last_name = ft.TextField()
    col = ft.Column(controls=[
        first_name,
        last_name
    ])
    col.disabled = True
    page.add(col)


ft.app(target=main)