import flet as ft

def main(page: ft.Page):
    page.add(ft.Text(f"Initial route: {page.route}"))

ft.app(target=main)
# ft.app(target=main, view=ft.WEB_BROWSER)