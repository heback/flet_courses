import flet as ft

def main(page: ft.Page):
    page.title = "Flet Text 예제"
    page.scroll = "adaptive"
    page.padding = 20

    # 1. 기본 텍스트
    basic_text = ft.Text("안녕하세요! 이것은 기본 Text 컨트롤입니다.")

    # 2. 스타일 적용 (글자 크기, 색상, 굵기, 기울임꼴, 글꼴)
    styled_text = ft.Text(
        "스타일 적용 예제",
        size=24,
        color=ft.Colors.BLUE,
        weight=ft.FontWeight.BOLD,
        italic=True,
        font_family="Arial"
    )

    # 3. theme_style 적용
    theme_text = ft.Text(
        "Material Design Theme Style 적용",
        theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
        color=ft.Colors.DEEP_ORANGE
    )

    # 4. Rich Text (TextSpan 여러 개로 다른 스타일 혼합)
    rich_text = ft.Text(
        spans=[
            ft.TextSpan("Flet ", ft.TextStyle(size=20, weight=ft.FontWeight.BOLD)),
            ft.TextSpan("은 ", ft.TextStyle(size=20)),
            ft.TextSpan("Python ", ft.TextStyle(color=ft.Colors.GREEN, size=20)),
            ft.TextSpan("기반의 UI 프레임워크", ft.TextStyle(color=ft.Colors.PURPLE, size=20, italic=True))
        ]
    )

    # 5. selectable = True (복사 가능한 텍스트)
    selectable_text = ft.Text(
        "이 텍스트는 드래그해서 복사할 수 있습니다.",
        selectable=True,
        size=16,
        color=ft.Colors.GREY_700
    )

    page.add(
        ft.Text("Flet Text 컨트롤 데모", size=28, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        basic_text,
        styled_text,
        theme_text,
        rich_text,
        selectable_text
    )

ft.app(target=main)
