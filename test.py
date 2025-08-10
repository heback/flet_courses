import flet as ft

def make_tab(idx: int) -> ft.Tab:
    return ft.Tab(
        text=f"Tab {idx}",
        icon=ft.Icons.LABEL,
        content=ft.Container(
            padding=12,
            content=ft.Column(
                [
                    ft.Text(f"콘텐츠: Tab {idx}", weight=ft.FontWeight.BOLD),
                    ft.TextField(label="이 탭만의 입력"),
                ],
                spacing=8,
            ),
        ),
    )

def main(page: ft.Page):
    page.title = "Tabs toggle demo (rebuild)"
    page.padding = 16

    status = ft.Text(color=ft.Colors.GREY_700)

    # 데모용: 헤더가 넘치도록 탭 여러 개 준비
    tab_list = [make_tab(i) for i in range(1, 13)]
    selected_index = 0
    scrollable = True
    anim_ms = 300

    # Tabs를 담는 홀더: content를 새 Tabs로 교체하는 방식
    tabs_holder = ft.Container(width=520)  # 폭 제한으로 헤더 넘치게
    def build_tabs():
        nonlocal selected_index
        t = ft.Tabs(
            tabs=tab_list,
            selected_index=min(selected_index, len(tab_list)-1) if tab_list else 0,
            scrollable=scrollable,
            animation_duration=anim_ms,
        )
        # 선택 변경 표시
        def on_change(e):
            nonlocal selected_index
            selected_index = t.selected_index
            cur = t.tabs[selected_index] if 0 <= selected_index < len(t.tabs) else None
            status.value = f"선택: index={selected_index}, text='{cur.text if cur else '-'}'"
            page.update()
        t.on_change = on_change
        tabs_holder.content = t
        page.update()
        return t

    tabs = build_tabs()  # 초기 구성

    # 조작 함수들
    def toggle_scrollable(e=None):
        nonlocal scrollable, tabs
        scrollable = not scrollable
        status.value = f"scrollable = {scrollable}"
        tabs = build_tabs()  # ▶ Tabs 재생성으로 즉시 반영

    def toggle_anim(e=None):
        nonlocal anim_ms, tabs, selected_index
        anim_ms = 0 if anim_ms else 300
        status.value = f"animation_duration = {anim_ms} ms"
        tabs = build_tabs()  # ▶ 재생성

        # 애니메이션 체감: 자동 전환(왕복)
        if len(tab_list) >= 2:
            cur = selected_index
            tabs.selected_index = (cur + 1) % len(tab_list)
            tabs.update()
            tabs.selected_index = cur
            tabs.update()

    def add_tab(e=None):
        nonlocal tabs, selected_index
        new_idx = (len(tab_list) + 1)
        tab_list.append(make_tab(new_idx))
        selected_index = len(tab_list) - 1
        tabs = build_tabs()

    def remove_tab(e=None):
        nonlocal tabs, selected_index
        if not tab_list:
            return
        del tab_list[selected_index]
        selected_index = max(0, min(selected_index, len(tab_list)-1))
        tabs = build_tabs()

    def rename_tab(e=None):
        if not tab_list:
            return
        name_field.value = tab_list[selected_index].text
        page.open(dlg)

    def save_rename(e=None):
        if not tab_list:
            page.close(dlg)
            return
        new_name = (name_field.value or "").strip()
        if new_name:
            tab_list[selected_index].text = new_name
            build_tabs()
            status.value = f"이름 변경: '{new_name}'"
        page.close(dlg)

    name_field = ft.TextField(label="새 탭 이름", autofocus=True, width=260)
    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("탭 이름 변경"),
        content=name_field,
        actions=[ft.TextButton("취소", on_click=lambda e: page.close(dlg)),
                 ft.FilledButton("저장", on_click=save_rename)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.add(
        ft.Text("Tabs 토글이 바로 보이게: 재생성 방식", weight=ft.FontWeight.BOLD),
        ft.Text("• scrollable/animation 변경 시 Tabs를 재생성하여 헤더를 강제 리렌더링"),
        ft.Divider(),
        ft.Row(
            [
                ft.FilledButton("탭 추가", icon=ft.Icons.ADD, on_click=add_tab),
                ft.OutlinedButton("선택 탭 삭제", icon=ft.Icons.DELETE, on_click=remove_tab),
                ft.TextButton("이름 변경", icon=ft.Icons.DRIVE_FILE_RENAME_OUTLINE, on_click=rename_tab),
                ft.TextButton("scrollable 토글", icon=ft.Icons.SWIPE, on_click=toggle_scrollable),
                ft.TextButton("애니메이션 토글", icon=ft.Icons.ANIMATION, on_click=toggle_anim),
            ],
            spacing=10,
            wrap=True,
        ),
        ft.Container(height=8),
        status,
        ft.Container(height=8),
        tabs_holder,  # 여기에 항상 최신 Tabs가 들어갑니다
    )

ft.app(target=main)
