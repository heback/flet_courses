import flet as ft


# --- 재사용 가능한 메뉴 생성 함수 ---
def create_app_menu(page: ft.Page) -> ft.PopupMenuButton:
    """
    모든 뷰에서 공통으로 사용할 AppBar 팝업 메뉴를 생성합니다.
    """
    return ft.PopupMenuButton(
        items=[
            ft.PopupMenuItem(text="홈", on_click=lambda _: page.go("/")),
            ft.PopupMenuItem(text="검색", on_click=lambda _: page.go("/search")),
            ft.PopupMenuItem(text="즐겨찾기",
                             on_click=lambda _: page.go("/favorites")),
            ft.PopupMenuItem(text="설정",
                             on_click=lambda _: page.go("/settings")),
        ]
    )


# --- 뷰(View) 클래스 정의 ---

class HomeView(ft.View):
    """홈 화면을 위한 뷰"""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.route = "/"
        # AppBar의 actions에서 헬퍼 함수를 호출하여 메뉴를 생성합니다.
        self.appbar = ft.AppBar(
            title=ft.Text("홈"),
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[create_app_menu(page)],
        )
        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.icons.HOME_ROUNDED, size=100,
                                color=ft.colors.BLUE_500),
                        ft.Text("홈 화면", size=32, weight=ft.FontWeight.BOLD),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        ]


class SearchView(ft.View):
    """검색 화면을 위한 뷰"""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.route = "/search"
        self.appbar = ft.AppBar(
            title=ft.Text("검색"),
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[create_app_menu(page)],  # 중복 코드 제거
        )
        self.padding = ft.padding.all(20)
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.controls = [
            ft.TextField(hint_text="무엇을 찾고 계신가요?", width=300),
            ft.ElevatedButton("검색하기")
        ]


class FavoritesView(ft.View):
    """즐겨찾기 화면을 위한 뷰"""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.route = "/favorites"
        self.appbar = ft.AppBar(
            title=ft.Text("즐겨찾기"),
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[create_app_menu(page)],  # 중복 코드 제거
        )
        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.icons.FAVORITE_ROUNDED, size=100,
                                color=ft.colors.PINK_500),
                        ft.Text("즐겨찾기", size=32, weight=ft.FontWeight.BOLD),
                        ft.Text("아직 즐겨찾기한 항목이 없습니다."),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                expand=True,
            )
        ]


class SettingsView(ft.View):
    """설정 화면을 위한 뷰"""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.route = "/settings"
        self.appbar = ft.AppBar(
            title=ft.Text("설정"),
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[create_app_menu(page)],  # 중복 코드 제거
        )
        self.padding = ft.padding.all(20)
        self.controls = [
            ft.Column([
                ft.Switch(label="다크 모드"),
                ft.Switch(label="알림 받기"),
            ])
        ]


# --- 메인 애플리케이션 로직 ---

def main(page: ft.Page):
    page.title = "AppBar 메뉴 및 라우팅 예제"

    page.window_min_width = 400
    page.window_min_height = 600

    views_map = {
        "/": HomeView,
        "/search": SearchView,
        "/favorites": FavoritesView,
        "/settings": SettingsView,
    }

    def route_change(route):
        current_route = page.route
        page.views.clear()
        page.views.append(views_map[current_route](page))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


ft.app(target=main)
