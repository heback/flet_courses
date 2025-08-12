import flet as ft

def main(page: ft.Page):
    page.title = "Flet Dropdown 예제"
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.START

    # 상태를 표시할 텍스트
    result_text = ft.Text(value="아직 선택하지 않았습니다.", size=16)

    # on_change 이벤트 핸들러
    def dropdown_changed(e: ft.ControlEvent):
        # e.control.value → 선택된 Option의 key 값
        selected_key = e.control.value

        # Option의 key → 사용자에게 보여질 text 찾기
        selected_text = next(
            (opt.text for opt in country_dropdown.options if opt.key == selected_key),
            "(알 수 없음)"
        )

        # 상태 출력
        result_text.value = f"선택된 국가: key={selected_key}, text={selected_text}"
        page.update()

    # Dropdown 생성
    country_dropdown = ft.Dropdown(
        label="국가 선택",
        hint_text="원하는 국가를 선택하세요",
        options=[
            ft.dropdown.Option(key="KR", text="대한민국"),
            ft.dropdown.Option(key="US", text="미국"),
            ft.dropdown.Option(key="JP", text="일본"),
            ft.dropdown.Option(key="FR", text="프랑스"),
        ],
        on_change=dropdown_changed,
        width=200
    )

    # 페이지에 컨트롤 추가
    page.add(
        ft.Text("Dropdown 동작 원리 예제", size=20, weight=ft.FontWeight.BOLD),
        country_dropdown,
        result_text
    )

# 앱 실행
if __name__ == "__main__":
    ft.app(target=main)
