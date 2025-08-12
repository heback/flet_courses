# app.py
import flet as ft

def main(page: ft.Page):
    page.title = "Flet: Checkbox / Switch / RadioGroup 가로 배열 데모"
    page.padding = 16
    page.scroll = "auto"
    page.theme_mode = ft.ThemeMode.LIGHT

    # ---- 공용 로그 함수 -------------------------------------------------------
    log_view = ft.ListView(expand=1, spacing=4, auto_scroll=True)
    def write_log(msg: str):
        log_view.controls.append(ft.Text(msg))
        page.update()

    # ==========================================================================
    # 1) Checkbox (가로 배열)
    # ==========================================================================
    def on_cb_basic_change(e: ft.ControlEvent):
        write_log(f"[Checkbox-basic] value={e.control.value}")

    cb_basic = ft.Checkbox(label="기본 체크박스", value=False, on_change=on_cb_basic_change)

    def on_cb_tri_change(e: ft.ControlEvent):
        write_log(f"[Checkbox-tristate] value={e.control.value}")

    cb_tri = ft.Checkbox(
        label="삼상 체크박스 (tristate=True)",
        tristate=True,
        value=None,
        on_change=on_cb_tri_change,
    )

    # 마스터-자식 체크박스
    child_checks = [
        ft.Checkbox(label="항목 A", value=False),
        ft.Checkbox(label="항목 B", value=True),
        ft.Checkbox(label="항목 C", value=False),
    ]
    cb_master = ft.Checkbox(label="전체 선택", tristate=True)

    def refresh_master_from_children():
        values = [c.value for c in child_checks]
        if all(values):
            cb_master.value = True
        elif not any(values):
            cb_master.value = False
        else:
            cb_master.value = None
        cb_master.update()

    def on_master_change(e: ft.ControlEvent):
        master_val = cb_master.value
        broadcast = True if master_val is None else master_val
        for c in child_checks:
            c.value = broadcast
            c.update()
        write_log(f"[Checkbox-master] set all -> {broadcast}")
        refresh_master_from_children()

    def on_child_change(e: ft.ControlEvent):
        write_log(f"[Checkbox-child] {e.control.label} -> {e.control.value}")
        refresh_master_from_children()

    cb_master.on_change = on_master_change
    for c in child_checks:
        c.on_change = on_child_change

    # 가로 배열 UI (Row + wrap)
    checkbox_section = ft.Card(
        content=ft.Container(
            padding=16,
            content=ft.Column(
                [
                    ft.Text("1) Checkbox (가로 배열)", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("✔ 기본 / ✔ 삼상(tristate) / ✔ 마스터-자식(전체선택·혼합상태) - 모두 가로 배열"),
                    # 기본/삼상 체크박스 가로 배열
                    ft.Row([cb_basic, cb_tri, cb_master] + child_checks,
                    spacing=10, wrap=False),
                ],
                tight=True,
            ),
        )
    )

    # ==========================================================================
    # 2) Switch (그대로, 참고용)
    # ==========================================================================
    theme_status = ft.Text("현재 테마: LIGHT")

    def on_theme_switch(e: ft.ControlEvent):
        dark = e.control.value
        page.theme_mode = ft.ThemeMode.DARK if dark else ft.ThemeMode.LIGHT
        theme_status.value = f"현재 테마: {'DARK' if dark else 'LIGHT'}"
        theme_status.update()
        page.update()
        write_log(f"[Switch-theme] DARK={dark}")

    sw_theme = ft.Switch(label="다크 모드", value=False, on_change=on_theme_switch)

    demo_rows = [
        {"id": 101, "name": "Alice", "active": True},
        {"id": 102, "name": "Bob", "active": False},
        {"id": 103, "name": "Charlie", "active": True},
    ]
    row_controls = []

    def make_row(i: int, row: dict):
        name_txt = ft.Text(f"{row['name']} (id={row['id']})")
        sw = ft.Switch(value=row["active"])

        def on_row_switch(e: ft.ControlEvent, i=i):
            demo_rows[i]["active"] = e.control.value
            name_txt.value = f"{demo_rows[i]['name']} (id={demo_rows[i]['id']}) - active={demo_rows[i]['active']}"
            name_txt.update()
            write_log(f"[Switch-row] id={demo_rows[i]['id']} -> active={demo_rows[i]['active']}")

        sw.on_change = on_row_switch
        return ft.Row([sw, name_txt], alignment=ft.MainAxisAlignment.START)

    for idx, r in enumerate(demo_rows):
        row_controls.append(make_row(idx, r))

    switch_section = ft.Card(
        content=ft.Container(
            padding=16,
            content=ft.Column(
                [
                    ft.Text("2) Switch", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("✔ 이진 토글(True/False) · ✔ 테마 토글 · ✔ 행별 토글(인덱스 안전 콜백)"),
                    ft.Row([sw_theme, theme_status]),
                    ft.Divider(),
                    ft.Text("행별 활성화 토글 데모"),
                    ft.Column(row_controls, spacing=4),
                ],
                tight=True,
            ),
        )
    )

    # ==========================================================================
    # 3) RadioGroup (가로 배열)
    # ==========================================================================
    size_preview = ft.Text("선택: (없음)")
    price_preview = ft.Text("가격: -")

    def on_size_change(e: ft.ControlEvent):
        val = rg_size.value
        size_preview.value = f"선택: {val}"
        price_map = {"Small": "₩3,000", "Medium": "₩3,800", "Large": "₩4,500"}
        price_preview.value = f"가격: {price_map.get(val, '-')}"
        size_preview.update()
        price_preview.update()
        write_log(f"[RadioGroup] selected={val}")

    # 라디오 버튼을 Row로 가로 배열 (wrap=True로 줄바꿈 허용)
    rg_size = ft.RadioGroup(
        value=None,
        on_change=on_size_change,
        content=ft.Row(
            [
                ft.Radio(value="Small", label="Small"),
                ft.Radio(value="Medium", label="Medium"),
                ft.Radio(value="Large", label="Large"),
            ],
            wrap=False,
            spacing=24,
        ),
    )

    radiogroup_section = ft.Card(
        content=ft.Container(
            padding=16,
            content=ft.Column(
                [
                    ft.Text("3) RadioGroup (가로 배열)", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("✔ 단일 선택 · ✔ 그룹 on_change · ✔ 선택값에 따른 UI 반응"),
                    rg_size,
                    ft.Row([size_preview, price_preview], spacing=24, wrap=True),
                ],
                tight=True,
            ),
        )
    )

    # ---- 페이지 레이아웃 ------------------------------------------------------
    page.add(
        checkbox_section,
        switch_section,
        radiogroup_section,
        ft.Text("이벤트 로그", size=18, weight=ft.FontWeight.BOLD),
        ft.Container(log_view, height=220, bgcolor=ft.Colors.GREY_100, padding=8, border_radius=8),
    )

    # 모든 컨트롤 추가 후 초기 마스터 상태 갱신
    refresh_master_from_children()

if __name__ == "__main__":
    ft.app(target=main)
