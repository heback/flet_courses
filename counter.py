import flet as ft
import time

def main(page: ft.Page):
    # 페이지 기본 설정
    page.title = "Flet 카운터 예제"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # 숫자 표시를 위한 텍스트 필드 위젯
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    # 이벤트 핸들러 함수 정의
    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    # 페이지에 위젯(컨트롤) 추가
    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

# Flet 앱 실행
ft.app(target=main)