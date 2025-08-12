import asyncio
import flet as ft


def main(page: ft.Page):
    page.title = "진행 상태 시각화 — ProgressBar & ProgressRing (Flet)"
    page.padding = 16
    page.scroll = "auto"

    # =========================
    # 공통 안내
    # =========================
    page.add(
        ft.Text(
            "확정적(Determinate): value=0.0~1.0  |  불확정적(Indeterminate): value=None",
            weight=ft.FontWeight.BOLD,
            size=16,
        ),
        ft.Divider(),
    )

    # =============================================================================
    # 섹션 A — 확정적(Determinate) 데모: 진행률이 알려진 작업 (예: 파일 다운로드)
    # =============================================================================
    a_title = ft.Text("A. 확정적(Determinate) 진행", size=18, weight=ft.FontWeight.BOLD)
    a_desc = ft.Text("진행률을 알고 있을 때: value를 0.0 → 1.0으로 올리며 표시")

    # 진행 표시 위젯
    a_label = ft.Text("대기 중", color=ft.Colors.GREY_700)
    a_bar = ft.ProgressBar(
        value=0.0, width=420, color=ft.Colors.BLUE, bgcolor=ft.Colors.GREY_300
    )
    a_ring = ft.ProgressRing(value=0.0, color=ft.Colors.BLUE, stroke_width=6)

    # 상태/제어
    a_speed = ft.Slider(
        min=0.01,
        max=0.2,
        divisions=19,
        value=0.05,
        label="업데이트 간격 (초): {value}",
        width=420,
    )

    a_start_btn = ft.ElevatedButton("시작", icon=ft.Icons.PLAY_ARROW)
    a_cancel_btn = ft.OutlinedButton("취소", icon=ft.Icons.STOP, disabled=True)
    a_reset_btn = ft.TextButton("초기화", icon=ft.Icons.RESTART_ALT)

    # 취소 플래그
    a_cancelled = {"flag": False}
    a_running = {"flag": False}

    async def run_determinate():
        a_running["flag"] = True
        a_cancelled["flag"] = False
        a_start_btn.disabled = True
        a_cancel_btn.disabled = False
        a_reset_btn.disabled = True
        page.update()

        # 0% → 100%
        for i in range(101):
            if a_cancelled["flag"]:
                a_label.value = "취소됨"
                break

            progress = i / 100
            a_bar.value = progress
            a_ring.value = progress
            a_label.value = f"{int(progress * 100)}%"

            # 슬라이더로 지정한 간격만큼 대기
            await asyncio.sleep(float(a_speed.value))
            page.update()

        # 완료 처리
        if not a_cancelled["flag"]:
            a_bar.value = 1.0
            a_ring.value = 1.0
            a_label.value = "완료!"
            page.update()

        a_running["flag"] = False
        a_start_btn.disabled = False
        a_cancel_btn.disabled = True
        a_reset_btn.disabled = False
        page.update()

    def a_on_start(_):
        if not a_running["flag"]:
            page.run_task(run_determinate)

    def a_on_cancel(_):
        if a_running["flag"]:
            a_cancelled["flag"] = True

    def a_on_reset(_):
        a_cancelled["flag"] = False
        a_running["flag"] = False
        a_bar.value = 0.0
        a_ring.value = 0.0
        a_label.value = "대기 중"
        a_start_btn.disabled = False
        a_cancel_btn.disabled = True
        a_reset_btn.disabled = False
        page.update()

    a_start_btn.on_click = a_on_start
    a_cancel_btn.on_click = a_on_cancel
    a_reset_btn.on_click = a_on_reset

    a_controls = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    a_title,
                    a_desc,
                    ft.Row(
                        controls=[a_ring, ft.Container(a_bar, expand=True), a_label],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(controls=[a_speed]),
                    ft.Row(
                        controls=[a_start_btn, a_cancel_btn, a_reset_btn],
                        spacing=10,
                    ),
                ],
                spacing=14,
            ),
            padding=16,
        )
    )

    page.add(a_controls)

    # =============================================================================
    # 섹션 B — 불확정적(Indeterminate) 데모: 진행률을 모를 때 (예: 서버 응답 대기)
    # =============================================================================
    b_title = ft.Text("B. 불확정적(Indeterminate) 진행", size=18, weight=ft.FontWeight.BOLD)
    b_desc = ft.Text("진행률을 모를 때: value=None 으로 애니메이션만 보여줌")

    b_label = ft.Text("대기 중", color=ft.Colors.GREY_700)
    b_bar = ft.ProgressBar(value=None, width=420, color=ft.Colors.DEEP_PURPLE, bgcolor=ft.Colors.GREY_300)
    b_ring = ft.ProgressRing(value=None, color=ft.Colors.DEEP_PURPLE, stroke_width=6)

    b_toggle = ft.Switch(label="작업 중", value=False)

    async def fake_unknown_work():
        # 알 수 없는 시간의 작업을 흉내: 최대 8초 동안 대기
        b_label.value = "작업 중… (불확정)"
        page.update()
        for _ in range(80):
            if not b_toggle.value:
                break
            await asyncio.sleep(0.1)
        # 작업 종료 시
        if b_toggle.value:
            # 자연 종료
            b_toggle.value = False
        page.update()

    def b_on_toggle(e: ft.ControlEvent):
        if e.control.value:
            # 시작: 불확정 모드로 전환 (value=None)
            b_bar.value = None
            b_ring.value = None
            b_label.value = "작업 중… (불확정)"
            page.update()
            page.run_task(fake_unknown_work)
        else:
            # 중지: value를 0으로 돌려 애니메이션 정지
            b_bar.value = 0.0
            b_ring.value = 0.0
            b_label.value = "대기 중"
            page.update()

    b_toggle.on_change = b_on_toggle

    b_controls = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    b_title,
                    b_desc,
                    ft.Row(
                        controls=[b_ring, ft.Container(b_bar, expand=True), b_label],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(controls=[b_toggle]),
                ],
                spacing=14,
            ),
            padding=16,
        )
    )

    page.add(b_controls)

    # =============================================================================
    # 섹션 C — 스타일링 예시: 색/배경색 바꾸기
    # =============================================================================
    c_title = ft.Text("C. 스타일링: color / bgcolor", size=18, weight=ft.FontWeight.BOLD)
    c_desc = ft.Text("색상 선택으로 진행 바/링의 색을 변경합니다.")

    c_bar = ft.ProgressBar(value=0.5, width=420, color=ft.Colors.GREEN, bgcolor=ft.Colors.GREY_200)
    c_ring = ft.ProgressRing(value=0.5, color=ft.Colors.GREEN, stroke_width=6)

    color_dd = ft.Dropdown(
        label="color",
        value="GREEN",
        options=[
            ft.dropdown.Option("GREEN"),
            ft.dropdown.Option("BLUE"),
            ft.dropdown.Option("ORANGE"),
            ft.dropdown.Option("RED"),
            ft.dropdown.Option("DEEP_PURPLE"),
        ],
        width=200,
    )

    bgcolor_dd = ft.Dropdown(
        label="bgcolor (ProgressBar만)",
        value="GREY_200",
        options=[
            ft.dropdown.Option("GREY_50"),
            ft.dropdown.Option("GREY_100"),
            ft.dropdown.Option("GREY_200"),
            ft.dropdown.Option("GREY_300"),
        ],
        width=220,
    )

    def c_on_change(_):
        # 선택된 이름을 ft.Colors 네임스페이스에서 가져와 적용
        c = getattr(ft.Colors, color_dd.value)
        bg = getattr(ft.Colors, bgcolor_dd.value)
        c_bar.color = c
        c_bar.bgcolor = bg
        c_ring.color = c
        page.update()

    color_dd.on_change = c_on_change
    bgcolor_dd.on_change = c_on_change

    c_controls = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    c_title,
                    c_desc,
                    ft.Row(
                        controls=[c_ring, ft.Container(c_bar, expand=True)],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Row(controls=[color_dd, bgcolor_dd], spacing=8),
                ],
                spacing=14,
            ),
            padding=16,
        )
    )

    page.add(c_controls)


if __name__ == "__main__":
    ft.app(target=main)
