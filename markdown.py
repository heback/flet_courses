import flet as ft


def main(page: ft.Page):
    page.title = "Flet Markdown — 올인원 데모"
    page.padding = 16
    page.scroll = "auto"

    # 샘플 마크다운 (GitHub 스타일 요소 포함: 테이블, 취소선 등)
    SAMPLE_MD = r"""
# Markdown 데모

**굵게** / *기울임* / ~~취소선~~ / `인라인 코드`

> 인용구: “문서는 읽기 쉬워야 합니다.”

---

## 목록
- 항목 A
- 항목 B
  - 하위 항목 B-1
1. 순서 목록 1
2. 순서 목록 2

## 링크 & 이미지
- [Flet 공식 문서](https://flet.dev)
- 내부 앵커 링크: [표 섹션으로 이동](#table-section)
- 이미지:
![무작위 이미지](https://picsum.photos/seed/flet/640/240 "랜덤 이미지")

## 코드 블록 (Python)
```python
def fib(n: int) -> list[int]:
    a, b = 0, 1
    seq = []
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq

print(fib(10))
```

## 가상환경 생성 & 활성화
```python -m venv .venv
source .venv/bin/activate  
# Windows: .venv\Scripts\activate
pip install flet
```

## 표 섹션 {#table-section}
| 기능            | 지원 여부 | 비고                     |
|----------------|-----------|--------------------------|
| **굵게/기울임** | ✅         | CommonMark                |
| ~~취소선~~     | ✅         | GitHub 확장               |
| 테이블         | ✅         | GitHub 확장               |
| 코드 하이라이트| ✅         | code_theme 으로 테마 설정 |
"""

    # -------------------------
    # Markdown 컨트롤 인스턴스
    # -------------------------
    def on_tap_link(e: ft.ControlEvent):
        url = e.data or ""
        if url.startswith("http"):
            # 외부 URL은 새 탭/창으로 오픈
            page.launch_url(url)
        elif url.startswith("#"):
            # 앵커는 데모로만 처리 (스낵바 표시)
            page.snack_bar = ft.SnackBar(ft.Text(f"내부 앵커 클릭: {url}"))
            page.snack_bar.open = True
            page.update()

    md = ft.Markdown(
        value=SAMPLE_MD,
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,  # 테이블/취소선 등 GitHub 스타일
        code_theme=ft.MarkdownCodeTheme.GITHUB,           # 기본 코드 하이라이트 테마
        selectable=True,                                  # 텍스트 선택 가능
        on_tap_link=on_tap_link,                          # 링크 클릭 핸들러
        # 필요 시: auto_follow_links=True, auto_follow_links_target=ft.UrlTarget.BLANK
    )

    # -------------------------
    # UI 컨트롤: 테마/확장 전환 + 편집 모드
    # -------------------------
    theme_options = {
        "GitHub": ft.MarkdownCodeTheme.GITHUB,
        "Monokai": ft.MarkdownCodeTheme.MONOKAI,
        "Nord": ft.MarkdownCodeTheme.NORD,
        "Xcode": ft.MarkdownCodeTheme.XCODE,
        "Tomorrow Night Eighties": ft.MarkdownCodeTheme.TOMORROW_NIGHT_EIGHTIES,
    }

    ext_options = {
        "GitHub Web": ft.MarkdownExtensionSet.GITHUB_WEB,
        "GitHub Flavored": ft.MarkdownExtensionSet.GITHUB_FLAVORED,
        "CommonMark": ft.MarkdownExtensionSet.COMMON_MARK,
        "None": ft.MarkdownExtensionSet.NONE,
    }

    theme_dd = ft.Dropdown(
        label="코드 하이라이트 테마 (code_theme)",
        value="GitHub",
        options=[ft.dropdown.Option(k) for k in theme_options.keys()],
        width=340,
    )

    ext_dd = ft.Dropdown(
        label="마크다운 확장 (extension_set)",
        value="GitHub Web",
        options=[ft.dropdown.Option(k) for k in ext_options.keys()],
        width=260,
    )

    edit_switch = ft.Switch(label="편집 모드", value=True)

    # 편집기(TextField)
    editor = ft.TextField(
        label="Markdown 원문 편집",
        value=SAMPLE_MD,
        multiline=True,
        min_lines=12,
        max_lines=30,
        expand=True,
        visible=True,  # 기본은 숨김
        on_change=lambda e: (setattr(md, "value", e.control.value), page.update()),
    )

    def on_change_theme(e: ft.ControlEvent):
        selected = e.control.value
        md.code_theme = theme_options[selected]
        page.update()

    def on_change_ext(e: ft.ControlEvent):
        selected = e.control.value
        md.extension_set = ext_options[selected]
        page.update()

    def on_toggle_edit(e: ft.ControlEvent):
        editor.visible = e.control.value
        page.update()

    theme_dd.on_change = on_change_theme
    ext_dd.on_change = on_change_ext
    edit_switch.on_change = on_toggle_edit

    reset_btn = ft.ElevatedButton(
        "샘플로 되돌리기",
        on_click=lambda _: (
            setattr(editor, "value", SAMPLE_MD),
            setattr(md, "value", SAMPLE_MD),
            page.update(),
        ),
    )

    controls_bar = ft.Row(
        controls=[theme_dd, ext_dd, edit_switch, reset_btn],
        wrap=True,
        spacing=12,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # 미리보기 영역을 보기 좋게 감싸기
    preview = ft.Container(
        content=md,
        padding=16,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=8,
        bgcolor=ft.Colors.GREY_50,
        expand=True,
    )

    page.add(
        ft.Column(
            controls=[
                ft.Text("Flet Markdown 컨트롤 — 실전 데모", size=22, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "아래에서 확장 세트/코드 테마를 바꾸고, 편집 모드로 원문을 수정해 보세요. "
                    "링크 클릭 시 on_tap_link 핸들러가 동작합니다.",
                    size=14,
                ),
                controls_bar,
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(editor, col={"sm": 12, "md": 6}),
                        ft.Container(preview, col={"sm": 12, "md": 6}),
                    ],
                    columns=12,
                ),
            ],
            expand=True,
            spacing=12,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)