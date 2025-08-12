import flet as ft

def main(page: ft.Page):
    page.title = "4.1 텍스트 입력의 모든 것: TextField"
    page.padding = 20
    page.scroll = "auto"

    # ===== 상태/로그 =====
    log = ft.Text("이벤트 로그가 여기에 표시됩니다.", color=ft.Colors.GREY_700)
    def write_log(msg: str):
        log.value = msg
        page.update()

    # ===== 공통 이벤트 핸들러 =====
    def on_change(e: ft.ControlEvent):
        # 입력값이 바뀔 때마다 호출
        write_log(f"[on_change] {e.control.label} = '{e.control.value}'")

    def on_submit(e: ft.ControlEvent):
        # Enter로 제출
        write_log(f"[on_submit] {e.control.label} = '{e.control.value}'")
        # e.control.focus()  # 포커스 유지

    def on_focus(e: ft.ControlEvent):
        write_log(f"[on_focus] {e.control.label}")

    def on_blur(e: ft.ControlEvent):
        write_log(f"[on_blur] {e.control.label}")

    # ===== 1) 사용자 이름 (기본 한 줄 입력 + 스타일 + 유효성) =====
    tf_username = ft.TextField(
        label="사용자 이름",
        hint_text="영문자/숫자 4–16자",
        max_length=16,
        prefix_icon=ft.Icons.PERSON,
        border=ft.InputBorder.UNDERLINE,   # 스타일: 밑줄
        border_radius=8,                   # (UNDERLINE에도 radius 적용 가능)
        color=ft.Colors.BLACK,             # 텍스트 색
        on_change=on_change,
        on_submit=on_submit,
        on_focus=on_focus,
        on_blur=on_blur,
        autofocus=True,
    )
    # 카운터 텍스트 갱신
    def username_counter(e):
        tf_username.counter_text = f"{len(e.control.value)}/16"
        page.update()
    tf_username.on_change = lambda e: (on_change(e), username_counter(e))

    # ===== 2) 비밀번호 (password + can_reveal_password + 유효성) =====
    tf_password = ft.TextField(
        label="비밀번호",
        hint_text="8자 이상, 대/소문자+숫자 권장",
        password=True,
        can_reveal_password=True,      # 눈 아이콘으로 보기/숨기기
        prefix_icon=ft.Icons.LOCK,
        border=ft.InputBorder.UNDERLINE,
        on_change=on_change,
        on_submit=on_submit,
        on_focus=on_focus,
        on_blur=on_blur,
        max_length=32,
    )
    def password_counter(e):
        tf_password.counter_text = f"{len(e.control.value)}/32"
        page.update()
    tf_password.on_change = lambda e: (on_change(e), password_counter(e))

    # ===== 3) 검색창 (Enter로 검색 트리거) =====
    tf_search = ft.TextField(
        label="검색어",
        hint_text="무엇을 찾고 계신가요?",
        prefix_icon=ft.Icons.SEARCH,
        # suffix_icon=ft.Icons.CLEAR,    # (아이콘 클릭 이벤트는 별도로 제공되지 않음)
        border=ft.InputBorder.OUTLINE, # 다른 스타일 예시
        border_radius=12,
        on_change=on_change,
        on_submit=lambda e: write_log(f"[검색 실행] '{e.control.value}'"),
    )
    # 지우기 버튼 별도로 제공
    clear_btn = ft.IconButton(
        icon=ft.Icons.CLEAR,
        tooltip="검색어 지우기",
        on_click=lambda e: (setattr(tf_search, "value", ""), write_log("[검색어 초기화]"), page.update()),
    )

    # ===== 4) 긴 메모 (multiline + max_length + 스타일/배경) =====
    tf_memo = ft.TextField(
        label="메모",
        hint_text="여러 줄로 입력할 수 있습니다.",
        multiline=True,
        min_lines=3,
        max_lines=6,
        max_length=200,
        bgcolor=ft.Colors.GREY_50,        # 배경색
        border=ft.InputBorder.OUTLINE,
        border_radius=12,
        on_change=on_change,
        on_focus=on_focus,
        on_blur=on_blur,
    )
    def memo_counter(e):
        tf_memo.counter_text = f"{len(e.control.value)}/200"
        page.update()
    tf_memo.on_change = lambda e: (on_change(e), memo_counter(e))

    # ===== 유효성 검사: error_text 사용 =====
    def validate_form() -> bool:
        ok = True
        # 사용자 이름: 4~16, 영문/숫자만
        u = (tf_username.value or "").strip()
        if not u:
            tf_username.error_text = "사용자 이름을 입력하세요."
            ok = False
        elif not (4 <= len(u) <= 16) or not u.isalnum():
            tf_username.error_text = "영문자/숫자 4~16자로 입력하세요."
            ok = False
        else:
            tf_username.error_text = None

        # 비밀번호: 8자 이상
        p = (tf_password.value or "")
        if len(p) < 8:
            tf_password.error_text = "비밀번호는 8자 이상이어야 합니다."
            ok = False
        else:
            tf_password.error_text = None

        # 메모는 선택 사항: 예시로 5자 미만이면 경고
        m = (tf_memo.value or "")
        if 0 < len(m) < 5:
            tf_memo.error_text = "메모는 5자 이상 또는 비워두세요."
            ok = False
        else:
            tf_memo.error_text = None

        page.update()
        return ok

    def submit_all(e=None):
        if validate_form():
            write_log(f"[제출 성공] username='{tf_username.value}', password='{'*'*len(tf_password.value)}', 검색어='{tf_search.value}', 메모={len(tf_memo.value or '')}자")
        else:
            write_log("[제출 실패] 빨간 에러 메시지를 확인하세요.")

    def reset_all(e=None):
        for tf in (tf_username, tf_password, tf_search, tf_memo):
            tf.value = ""
            tf.error_text = None
            tf.counter_text = None
        write_log("[초기화] 모든 필드가 비워졌습니다.")
        page.update()

    # ===== 레이아웃 =====
    page.add(
        ft.Text("4.1. 텍스트 입력의 모든 것: TextField", size=20, weight=ft.FontWeight.BOLD),
        ft.Text("• 스타일(UNDERLINE/OUTLINE/색상) • 비밀번호 • 다중 줄 • 길이 제한 • 이벤트 • error_text 유효성", color=ft.Colors.GREY_700),
        ft.Divider(),

        # 사용자 이름 / 비밀번호
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("계정 정보", weight=ft.FontWeight.BOLD),
                    tf_username,
                    tf_password,
                ],
                spacing=10,
            ),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=12,
        ),

        ft.Container(height=12),

        # 검색창
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("검색", weight=ft.FontWeight.BOLD),
                    ft.Row([tf_search, clear_btn], spacing=8),
                ],
                spacing=10,
            ),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=12,
        ),

        ft.Container(height=12),

        # 메모
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("메모", weight=ft.FontWeight.BOLD),
                    tf_memo,
                ],
                spacing=10,
            ),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=12,
        ),

        ft.Container(height=12),

        # 액션
        ft.Row(
            [
                ft.FilledButton("제출", icon=ft.Icons.CHECK, on_click=submit_all),
                ft.OutlinedButton("초기화", icon=ft.Icons.RESTART_ALT, on_click=reset_all),
            ],
            spacing=10,
        ),

        ft.Divider(),
        log,
    )

ft.app(target=main)
