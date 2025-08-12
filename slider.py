import flet as ft

def main(page: ft.Page):
    page.title = "Slider / RangeSlider 동작 원리 예제"
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Slider 값 표시
    slider_value_text = ft.Text(value="단일 값: 50", size=16)
    # RangeSlider 값 표시
    range_value_text = ft.Text(value="범위 값: (20, 80)", size=16)

    # Slider 값 변경 시 실행
    def slider_changed(e: ft.ControlEvent):
        # e.control.value -> 현재 슬라이더 값 (float)
        slider_value_text.value = f"단일 값: {e.control.value:.0f}"
        page.update()

    # RangeSlider 값 변경 시 실행
    def range_slider_changed(e: ft.ControlEvent):
        # e.control.start_value -> 시작 값
        # e.control.end_value -> 끝 값
        range_value_text.value = (
            f"범위 값: ({e.control.start_value:.0f}, {e.control.end_value:.0f})"
        )
        page.update()

    # Slider 생성
    slider = ft.Slider(
        min=0,
        max=100,
        divisions=10,       # 눈금 개수
        value=50,           # 초기 값
        label="{value}%",   # 현재 값 표시 형식
        on_change=slider_changed,
        width=300
    )

    # RangeSlider 생성
    range_slider = ft.RangeSlider(
        min=0,
        max=100,
        divisions=20,
        start_value=20,     # 시작 값 초기 설정
        end_value=80,       # 끝 값 초기 설정
        label="{value}%",   # 각 핸들 값에 표시
        on_change=range_slider_changed,
        width=300
    )

    # 페이지에 추가
    page.add(
        ft.Text("Slider / RangeSlider 동작 원리", size=20, weight=ft.FontWeight.BOLD),
        ft.Text("1. Slider (단일 값 선택)"),
        slider,
        slider_value_text,
        ft.Divider(),
        ft.Text("2. RangeSlider (범위 값 선택)"),
        range_slider,
        range_value_text
    )

# 실행
if __name__ == "__main__":
    ft.app(target=main)
