import flet as ft

def make_tile(idx: int) -> ft.Container:
    """세로 ListView용 아이템"""
    return ft.Container(
        bgcolor=ft.Colors.BLUE_50 if idx % 2 == 0 else ft.Colors.AMBER_50,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=8,
        padding=12,
        content=ft.Row(
            [
                ft.Icon(ft.Icons.LIST, color=ft.Colors.BLUE_400),
                ft.Text(f"항목 #{idx}", weight=ft.FontWeight.BOLD),
                ft.Text("  ← ListView는 아이템을 계속 추가할 수 있어요.", color=ft.Colors.GREY_700),
            ],
            spacing=8,
        ),
    )

def make_chip(idx: int) -> ft.Container:
    """가로 스크롤용 작은 칩(가로 Row에 넣을 요소)"""
    return ft.Container(
        bgcolor=ft.Colors.CYAN_50,
        border=ft.border.all(1, ft.Colors.CYAN_200),
        border_radius=999,
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        content=ft.Row([ft.Icon(ft.Icons.TAG), ft.Text(f"Chip {idx}")], spacing=6),
    )

def main(page: ft.Page):
    page.title = "ListView demo"
    page.padding = 16
    page.scroll = "auto"

    # --- 상태 표시 ---
    status = ft.Text(color=ft.Colors.GREY_700)

    # --- 세로 ListView ---
    lv = ft.ListView(
        expand=1,          # 남은 공간을 채우도록 확장
        spacing=8,         # 아이템 간 간격
        padding=10,        # 내부 패딩
        auto_scroll=True,  # 아이템 추가 시 자동으로 맨 아래로 스크롤
    )

    # 초기 아이템
    counter = 0
    for _ in range(5):
        lv.controls.append(make_tile(counter))
        counter += 1

    # --- 가로 스크롤 패턴: Row(scroll=...) 사용 ---
    chips_row = ft.Row(
        controls=[make_chip(i) for i in range(1, 18)],
        spacing=8,
        scroll=ft.ScrollMode.AUTO,   # 가로로 넘겨 보기
        # 필요하면 ALWAYS로 고정 스크롤바, HIDDEN으로 숨김
    )

    horizontal_scroller = ft.Container(
        content=ft.Column(
            [
                ft.Text("가로 스크롤 예시 (Row(scroll=ft.ScrollMode.AUTO))"),
                chips_row,
            ],
            spacing=8,
        ),
        padding=12,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=12,
        bgcolor=ft.Colors.GREY_50,
    )

    # --- 조작 컨트롤 ---
    batch_size = 5
    auto_scroll_switch = ft.Switch(label="auto_scroll", value=True)
    spacing_slider = ft.Slider(min=0, max=24, divisions=12, value=8, label="{value}")
    padding_slider = ft.Slider(min=0, max=32, divisions=16, value=10, label="{value}")

    def add_one(e=None):
        nonlocal counter
        lv.controls.append(make_tile(counter))
        counter += 1
        status.value = f"아이템 1개 추가 → 총 {len(lv.controls)}개"
        page.update()

    def add_batch(e=None):
        nonlocal counter
        for _ in range(batch_size):
            lv.controls.append(make_tile(counter))
            counter += 1
        status.value = f"아이템 {batch_size}개 추가 → 총 {len(lv.controls)}개"
        page.update()

    def clear_list(e=None):
        nonlocal counter
        lv.controls.clear()
        counter = 0
        status.value = "리스트 비움"
        page.update()

    def toggle_auto_scroll(e):
        lv.auto_scroll = auto_scroll_switch.value
        status.value = f"auto_scroll = {lv.auto_scroll}"
        page.update()

    def change_spacing(e):
        lv.spacing = int(spacing_slider.value)
        status.value = f"spacing = {lv.spacing}"
        page.update()

    def change_padding(e):
        lv.padding = int(padding_slider.value)
        status.value = f"padding = {lv.padding}"
        page.update()

    # 버튼/슬라이더 UI
    controls_bar = ft.Row(
        [
            ft.ElevatedButton("Add 1", icon=ft.Icons.ADD, on_click=add_one),
            ft.FilledButton(f"Add {batch_size}", icon=ft.Icons.ADD_CIRCLE, on_click=add_batch),
            ft.OutlinedButton("Clear", icon=ft.Icons.DELETE, on_click=clear_list),
            auto_scroll_switch,
        ],
        spacing=10,
        wrap=True,
    )
    auto_scroll_switch.on_change = toggle_auto_scroll

    sliders = ft.Row(
        [
            ft.Column([ft.Text("아이템 간 간격 (spacing)"), spacing_slider], spacing=6, width=260),
            ft.Column([ft.Text("내부 패딩 (padding)"), padding_slider], spacing=6, width=260),
        ],
        wrap=True,
        spacing=20,
    )
    spacing_slider.on_change = change_spacing
    padding_slider.on_change = change_padding

    # 레이아웃 배치
    page.add(
        ft.Text("ListView 작동 방식 데모", weight=ft.FontWeight.BOLD),
        ft.Text("• 동적 추가 / auto_scroll / spacing & padding / expand / 가로 스크롤(Row(scroll))"),
        ft.Divider(),
        controls_bar,
        sliders,
        status,
        ft.Container(
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=12,
            padding=10,
            content=ft.Column(
                [
                    ft.Text("세로 ListView"),
                    ft.Container(
                        content=lv,
                        height=300,   # 데모를 위해 고정 높이 → 내부가 스크롤됩니다.
                    ),
                ],
                spacing=8,
            ),
        ),
        ft.Container(height=12),
        horizontal_scroller,  # 가로 스크롤 예시
    )

ft.app(target=main)
