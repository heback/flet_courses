import flet as ft
import base64
import urllib.request
import ssl

# SSL 인증서 검증 비활성화 (테스트 용도)
ssl._create_default_https_context = ssl._create_unverified_context


def main(page: ft.Page):
    page.title = "Flet Image 예제 (가로 레이아웃 + 가로 스크롤 갤러리)"
    page.scroll = "adaptive"
    page.padding = 20

    # ✅ 실제 로드 가능한 이미지
    IMG_OK_SMALL = "https://picsum.photos/200/100"
    IMG_OK_SQUARE = "https://picsum.photos/300"
    IMG_OK_FIXED = "https://picsum.photos/id/237/400/300"
    IMG_FAIL = "https://invalid-domain.example.com/nonexistent.png"

    # URL → Base64 변환
    def url_to_base64(url: str) -> str:
        with urllib.request.urlopen(url) as response:
            data = response.read()
        return base64.b64encode(data).decode("utf-8")

    base64_str = url_to_base64(IMG_OK_SMALL)

    # 공통: (제목, 컨트롤) 쌍을 하나의 카드 컨테이너로 만드는 헬퍼
    def make_card(title: str, control: ft.Control, width: int = 220, height: int | None = None) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(title, size=14, weight=ft.FontWeight.BOLD),
                    control,
                ],
                spacing=6,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=width,
            height=height,
            padding=10,
            bgcolor=ft.Colors.GREY_50,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
        )

    # --- 상단: 이미지 갤러리 (가로 스크롤) ---
    gallery_row = ft.Row(
        controls=[
            make_card("1. 기본 이미지 (웹 URL)", ft.Image(src=IMG_OK_SQUARE, width=200, height=200, fit=ft.ImageFit.CONTAIN), width=240),
            make_card("2. 크기/fit = CONTAIN", ft.Image(src=IMG_OK_FIXED, width=200, height=120, fit=ft.ImageFit.CONTAIN), width=240),
            make_card("3. 크기/fit = COVER", ft.Image(src=IMG_OK_FIXED, width=200, height=120, fit=ft.ImageFit.COVER), width=240),
            make_card("4. 둥근 모서리", ft.Image(src=IMG_OK_FIXED, width=160, height=160, fit=ft.ImageFit.COVER, border_radius=20), width=220),
            make_card("5. 원형 이미지", ft.Image(src=IMG_OK_FIXED, width=160, height=160, fit=ft.ImageFit.COVER, border_radius=80), width=220),
            make_card("6. Base64 인코딩 이미지", ft.Image(src_base64=base64_str, width=120, height=120, fit=ft.ImageFit.CONTAIN), width=200),
        ],
        spacing=12,
        wrap=False,                       # 줄바꿈 없이 가로로만 배치
        scroll=ft.ScrollMode.AUTO,        # ✅ 가로 스크롤 활성화
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    # --- 하단: Base64 문자열 + error_content ---
    error_demo_title = ft.Text("7. error_content 데모", size=14, weight=ft.FontWeight.BOLD)
    error_switch = ft.Switch(label="이미지 로드 실패 시뮬레이션", value=False)
    error_image = ft.Image(
        src=IMG_OK_SMALL,
        width=220,
        height=140,
        fit=ft.ImageFit.CONTAIN,
        error_content=ft.Container(
            content=ft.Text("이미지를 불러올 수 없습니다.", color=ft.Colors.RED),
            alignment=ft.alignment.center,
            bgcolor=ft.Colors.GREY_200,
            border_radius=8,
            padding=10,
        ),
    )

    def toggle_error(e: ft.ControlEvent):
        error_image.src = IMG_FAIL if error_switch.value else IMG_OK_SMALL
        page.update()

    error_switch.on_change = toggle_error

    # Base64 문자열 스크롤 가능 표시 (세로 스크롤)
    base64_list = ft.ListView(
        controls=[ft.Text(base64_str, selectable=True, size=10)],
        expand=False,
        height=200,
        width=500,
        spacing=0,
        padding=10,
        auto_scroll=False,
    )

    bottom_row = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Text("Base64 문자열 (IMG_OK_SMALL 변환)", size=14, weight=ft.FontWeight.BOLD),
                    base64_list,
                ],
                spacing=8,
                expand=True,
            ),
            ft.VerticalDivider(width=1),
            ft.Column(
                controls=[error_demo_title, error_switch, error_image],
                spacing=8,
                tight=True,
            ),
        ],
        spacing=16,
        expand=True,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    # --- 전체 배치 ---
    page.add(
        ft.Column(
            controls=[
                ft.Text("Flet Image 컨트롤 예제 (가로 스크롤 갤러리)", size=22, weight=ft.FontWeight.BOLD),
                gallery_row,
                ft.Divider(),
                bottom_row,
            ],
            spacing=16,
            expand=True,
        )
    )


ft.app(target=main)
