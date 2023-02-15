# pip install flet
# or
# pip install flet --upgrade

import flet as ft


def main(page: ft.Page):
    # add/update controls on Page
    pass


ft.app(target=main)

# By default, Flet app starts in a native OS window, which is very handy for developing.
# However, you can open it in a new browser window by modifying a call to flet.app as following:
# ft.app(target=main, view=ft.WEB_BROWSER)
