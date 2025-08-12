import flet as ft

def main(page: ft.Page):
    page.title = "Flet 버튼 데모"
    page.scroll = "adaptive"
    page.padding = 20
    page.spacing = 20

    status = ft.Text("상태: 아직 클릭된 버튼이 없습니다.", color=ft.Colors.GREY_700)

    # 클릭된 컨트롤의 "종류"와 "라벨"을 설명 텍스트로 반환
    def describe_control(ctrl: ft.Control) -> tuple[str, str]:
        # 종류(타입) 판별
        if isinstance(ctrl, (ft.ElevatedButton, ft.Button)):      kind = "ElevatedButton"
        elif isinstance(ctrl, ft.FilledButton):                    kind = "FilledButton"
        elif isinstance(ctrl, ft.FilledTonalButton):               kind = "FilledTonalButton"
        elif isinstance(ctrl, ft.OutlinedButton):                  kind = "OutlinedButton"
        elif isinstance(ctrl, ft.TextButton):                      kind = "TextButton"
        elif isinstance(ctrl, ft.IconButton):                      kind = "IconButton"
        elif isinstance(ctrl, ft.FloatingActionButton):            kind = "FloatingActionButton"
        else:                                                      kind = ctrl.__class__.__name__

        # 라벨(표시 텍스트 또는 아이콘)
        label = getattr(ctrl, "text", None) or getattr(ctrl, "icon", "") or ""
        return kind, str(label)

    # 공통 클릭 핸들러
    def on_click(e: ft.ControlEvent):
        kind, label = describe_control(e.control)
        suffix = f" (라벨: {label})" if label else ""
        status.value = f"상태: {kind} 버튼을 클릭했습니다.{suffix}"
        page.update()

    # 버튼들
    elevated_btn = ft.ElevatedButton(
        text="로그인",
        icon=ft.Icons.LOGIN,
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE,
        on_click=on_click,
    )

    filled_btn = ft.FilledButton(
        text="제출",
        icon=ft.Icons.SEND,
        bgcolor=ft.Colors.GREEN,
        color=ft.Colors.WHITE,
        on_click=on_click,
    )

    tonal_btn = ft.FilledTonalButton(
        text="저장",
        icon=ft.Icons.SAVE,
        on_click=on_click,
    )

    outlined_btn = ft.OutlinedButton(
        text="취소",
        icon=ft.Icons.CLOSE,
        on_click=on_click,
    )

    text_btn = ft.TextButton(
        text="닫기",
        on_click=on_click,
    )

    icon_btn = ft.IconButton(
        icon=ft.Icons.EDIT,
        icon_color=ft.Colors.PURPLE,
        tooltip="편집",
        on_click=on_click,
    )

    # FloatingActionButton도 동일 핸들러 사용
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        tooltip="새 항목 추가",
        on_click=on_click,
    )

    page.add(
        ft.Text("Flet 버튼 예제", size=24, weight=ft.FontWeight.BOLD),
        ft.Row([elevated_btn, filled_btn, tonal_btn], spacing=10),
        ft.Row([outlined_btn, text_btn, icon_btn], spacing=10),
        ft.Divider(),
        status,
        ft.Text("※ 오른쪽 하단의 FAB(원형 버튼)도 클릭해보세요.", size=12, italic=True),
    )

ft.app(target=main)
