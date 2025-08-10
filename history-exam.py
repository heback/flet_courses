import flet as ft
from flet import TemplateRoute


def main(page: ft.Page):
    page.title = "뒤로 가기 및 앞으로 가기 예제"
    page.window.width = 400
    page.window.height = 700

    # 현재 경로와 뷰 스택을 표시할 텍스트 컨트롤
    current_route_info = ft.Text()
    views_stack_info = ft.Text()

    def update_route_info():
        """화면에 현재 경로와 뷰 스택 정보를 업데이트하는 함수"""
        current_route_info.value = f"현재 경로 (page.route): {page.route}"

        stack_routes = [v.route for v in page.views]
        views_stack_info.value = f"현재 뷰 스택 (page.views): {stack_routes}"
        page.update()

    def route_change(e: ft.RouteChangeEvent):
        """
        URL이 변경될 때마다 호출되어, 현재 URL을 기반으로
        뷰 스택을 처음부터 올바르게 다시 구성합니다.
        """
        print(f"Route changed to: {e.route}")

        # 새로운 뷰를 그리기 전에 항상 기존 뷰 스택을 비웁니다.
        page.views.clear()

        # 기본 뷰 (홈)는 항상 스택의 가장 아래에 추가합니다.
        page.views.append(
            ft.View(
                route="/",
                appbar=ft.AppBar(title=ft.Text("홈")),
                controls=[
                    ft.Text("여기는 홈 화면입니다.", size=20),
                    ft.ElevatedButton("상점으로 이동",
                                      on_click=lambda _: page.go("/store")),
                    ft.ElevatedButton("계정으로 이동",
                                      on_click=lambda _: page.go("/account")),
                    ft.Divider(),
                    current_route_info,
                    views_stack_info,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        # --- 수정된 로직 ---
        # startswith를 사용하여 현재 경로가 특정 경로로 시작하는지 확인하여
        # 계층적인 뷰 스택을 올바르게 구성합니다.

        # '/store' 경로 또는 그 하위 경로일 경우
        if page.route.startswith("/store"):
            page.views.append(
                ft.View(
                    route="/store",
                    appbar=ft.AppBar(title=ft.Text("상점")),
                    controls=[
                        ft.Text("여기는 상점입니다.", size=20),
                        ft.ElevatedButton("상품 1 보기", on_click=lambda _: page.go(
                            "/store/product/1")),
                        ft.ElevatedButton("상품 2 보기", on_click=lambda _: page.go(
                            "/store/product/2")),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        # '/store/product/:id' 형태의 동적 경로일 경우
        troute = TemplateRoute(page.route)
        if troute.match("/store/product/:id"):
            product_id = troute.id  # 경로에서 id 파라미터 추출
            page.views.append(
                ft.View(
                    route=f"/store/product/{product_id}",
                    appbar=ft.AppBar(title=ft.Text(f"상품 {product_id}")),
                    controls=[
                        ft.Text(f"상품 {product_id}의 상세 정보입니다.", size=20)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        # '/account' 경로일 경우
        if page.route == "/account":
            page.views.append(
                ft.View(
                    route="/account",
                    appbar=ft.AppBar(title=ft.Text("계정")),
                    controls=[
                        ft.Text("여기는 계정 화면입니다.", size=20)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        # 정보 텍스트와 페이지를 업데이트합니다.
        update_route_info()

    def view_pop(e: ft.ViewPopEvent):
        """
        AppBar의 뒤로가기 화살표를 눌렀을 때 실행됩니다.
        """
        print("View pop event")
        # 스택에서 가장 위의 뷰를 제거합니다.
        page.views.pop()
        # 이제 새로운 최상위 뷰의 경로로 이동합니다.
        top_view = page.views[-1]
        page.go(top_view.route)

    # 페이지 이벤트 핸들러 등록
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # 앱 시작 시, 브라우저의 현재 URL을 기반으로 첫 화면을 렌더링합니다.
    page.go(page.route)


# 웹 브라우저 뷰로 앱 실행
ft.app(target=main, view=ft.AppView.WEB_BROWSER)
