import flet as ft


def main(page: ft.Page):
    for i in range(5000):
        page.add(ft.Text(f"Line {i}"))
    page.scroll = ft.ScrollMode.ALWAYS
    page.update()


ft.app(target=main, view=ft.WEB_BROWSER)