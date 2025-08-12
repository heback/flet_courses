import flet as ft

def main(page: ft.Page):
    page.title = "Flet Icon 예제"
    page.scroll = "adaptive"
    page.padding = 20

    # 1. 기본 아이콘
    basic_icon = ft.Icon(name=ft.Icons.FAVORITE)

    # 2. 크기, 색상 변경
    styled_icon = ft.Icon(
        name=ft.Icons.FAVORITE,
        size=40,
        color=ft.Colors.RED
    )

    # 3. tooltip 적용
    tooltip_icon = ft.Icon(
        name=ft.Icons.INFO,
        size=30,
        color=ft.Colors.BLUE,
        tooltip="이 아이콘은 정보(Info)를 나타냅니다."
    )

    # 4. 버튼과 함께 사용
    button_with_icon = ft.ElevatedButton(
        text="좋아요",
        icon=ft.Icons.THUMB_UP,
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE
    )

    # 5. 아이콘 나열 (Row)
    icon_row = ft.Row(
        controls=[
            ft.Icon(ft.Icons.HOME, size=30, color=ft.Colors.PURPLE, tooltip="홈"),
            ft.Icon(ft.Icons.SEARCH, size=30, color=ft.Colors.BLUE, tooltip="검색"),
            ft.Icon(ft.Icons.SETTINGS, size=30, color=ft.Colors.GREY, tooltip="설정")
        ],
        spacing=20
    )

    # 6. 아이콘 나열 (Column)
    icon_column = ft.Column(
        controls=[
            ft.Icon(ft.Icons.CALL, size=25, color=ft.Colors.GREEN, tooltip="전화"),
            ft.Icon(ft.Icons.EMAIL, size=25, color=ft.Colors.RED, tooltip="이메일"),
            ft.Icon(ft.Icons.LOCATION_ON, size=25, color=ft.Colors.BLUE, tooltip="위치")
        ],
        spacing=10
    )

    page.add(
        ft.Text("Flet Icon 컨트롤 예제", size=28, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text("1. 기본 아이콘"),
        basic_icon,
        ft.Text("2. 크기와 색상 변경"),
        styled_icon,
        ft.Text("3. Tooltip 적용"),
        tooltip_icon,
        ft.Text("4. 버튼과 함께 사용"),
        button_with_icon,
        ft.Text("5. Row로 아이콘 나열"),
        icon_row,
        ft.Text("6. Column으로 아이콘 나열"),
        icon_column
    )

ft.app(target=main)
