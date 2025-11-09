import flet as ft
from flet import View, Page, AppBar, ElevatedButton, Text, RouteChangeEvent, \
    ViewPopEvent
from typing import Dict, Type


# ---------------------------------------------------------------------------
# 1단계: 각 페이지(View)를 독립적인 클래스로 정의
# 각 View 클래스는 자신의 UI를 구성하는 책임을 가집니다.
# ---------------------------------------------------------------------------

class ViewBase:
    """
    모든 View 클래스들이 상속받을 기본 클래스입니다.
    라우터 인스턴스를 받아 페이지 이동(go) 메서드를 사용할 수 있도록 합니다.
    """

    def __init__(self, router: 'Router'):
        self._router = router
        self.view = View()
        self.controls = []  # 각 View의 컨트롤을 담을 리스트
        self.appbar: AppBar | None = None
        self.build_view()  # 자식 클래스에서 이 메서드를 오버라이드하여 UI를 구성합니다.

    @property
    def route(self) -> str:
        return self.view.route

    def build_view(self):
        """
        자식 클래스에서 이 메서드를 오버라이드하여 AppBar와 Controls를 설정해야 합니다.
        """
        raise NotImplementedError(
            "build_view() must be implemented in the child class.")

    def get_view(self) -> View:
        """
        설정된 AppBar와 Controls를 바탕으로 최종 ft.View 객체를 반환합니다.
        """
        self.view.appbar = self.appbar
        self.view.controls = self.controls
        return self.view


class HomeView(ViewBase):
    """홈 페이지 UI 및 로직을 담당하는 클래스"""

    def build_view(self):
        self.view.route = "/"
        self.appbar = AppBar(title=Text("Flet 홈"),
                             bgcolor=ft.Colors.ON_SURFACE_VARIANT)
        self.controls = [
            Text("여기는 홈 화면입니다.", size=20),
            ElevatedButton(
                "상점으로 이동",
                on_click=lambda _: self._router.page.go("/store")
            ),
            ElevatedButton(
                "사용자 'kim' 프로필 보기",
                on_click=lambda _: self._router.page.go("/users/kim")
            ),
        ]


class StoreView(ViewBase):
    """상점 페이지 UI 및 로직을 담당하는 클래스"""

    def build_view(self):
        self.view.route = "/store"
        self.appbar = AppBar(title=Text("상점"),
                             bgcolor=ft.Colors.ON_SURFACE_VARIANT)
        self.controls = [
            Text("여기는 상점입니다.", size=20),
            ElevatedButton("홈으로 돌아가기",
                           on_click=lambda _: self._router.page.go("/")),
        ]


class UserProfileView(ViewBase):
    """사용자 프로필 페이지 UI 및 로직을 담당하는 클래스"""

    def __init__(self, router: 'Router', user_name: str):
        self.user_name = user_name
        super().__init__(router)

    def build_view(self):
        # 템플릿 라우트를 사용하여 동적으로 경로를 설정합니다.
        self.view.route = f"/users/{self.user_name}"
        self.appbar = AppBar(title=Text(f"{self.user_name}의 프로필"),
                             bgcolor=ft.Colors.ON_SURFACE_VARIANT)
        self.controls = [
            Text(f"안녕하세요, {self.user_name}님!", size=20),
            ElevatedButton("홈으로 돌아가기",
                           on_click=lambda _: self._router.page.go("/")),
        ]


# ---------------------------------------------------------------------------
# 2단계: 내비게이션을 총괄하는 Router 클래스 정의
# ---------------------------------------------------------------------------

class Router:
    """
    페이지의 경로 변경을 감지하고, 적절한 View를 생성하여 화면에 표시하는
    '교통 관제사' 역할을 합니다.
    """

    def __init__(self, page: Page):
        self.page = page
        # 경로와 해당 경로를 처리할 View 클래스를 딕셔너리로 매핑합니다.
        # 이렇게 하면 새로운 페이지를 추가할 때 이 딕셔너리에 한 줄만 추가하면 됩니다.
        self.routes: Dict[str, Type[ViewBase]] = {
            "/": HomeView,
            "/store": StoreView,
        }

    def on_route_change(self, e: RouteChangeEvent) -> None:
        """URL 경로가 변경될 때마다 Flet에 의해 호출되는 핸들러"""
        # 현재 경로를 파싱하기 위해 매번 TemplateRoute 인스턴스를 생성합니다.
        troute = ft.TemplateRoute(e.route)

        self.page.views.clear()

        # 홈 뷰는 항상 기본으로 추가합니다 (계층 구조의 루트)
        home_view_instance = self.routes["/"](self)
        self.page.views.append(home_view_instance.get_view())

        # --- 동적 경로 처리 (TemplateRoute) ---
        # match() 메서드에는 템플릿 문자열을 전달하는 것이 올바른 사용법입니다.
        if troute.match("/users/:user_name"):
            user_name = troute.user_name
            # URL 파라미터를 사용하여 View 인스턴스를 생성합니다.
            user_view = UserProfileView(self, user_name)
            self.page.views.append(user_view.get_view())
        # --- 정적 경로 처리 ---
        elif e.route in self.routes and e.route != "/":
            # 딕셔너리에서 경로에 맞는 View 클래스를 찾아 인스턴스를 생성합니다.
            view_class = self.routes[e.route]
            view_instance = view_class(self)
            self.page.views.append(view_instance.get_view())

        self.page.update()

    def on_view_pop(self, e: ViewPopEvent) -> None:
        """AppBar의 뒤로가기 버튼이 클릭되었을 때 호출되는 핸들러"""
        self.page.views.pop()
        # 스택에서 가장 위의 View를 가져옵니다.
        top_view = self.page.views[-1]
        # 해당 View의 경로로 이동합니다.
        self.page.go(top_view.route)


# ---------------------------------------------------------------------------
# 3단계: Flet 앱 메인 함수에서 Router 연결
# ---------------------------------------------------------------------------

def main(page: Page):
    page.title = "객체지향 라우터 예제"

    # Router 인스턴스를 생성하고 Flet 페이지의 이벤트 핸들러에 연결합니다.
    router = Router(page)
    page.on_route_change = router.on_route_change
    page.on_view_pop = router.on_view_pop

    # 앱 시작 시 초기 경로로 이동하여 첫 화면을 렌더링합니다.
    page.go(page.route)


# Flet 앱을 웹 브라우저에서 실행합니다.
if __name__ == "__main__":
    ft.app(target=main)

