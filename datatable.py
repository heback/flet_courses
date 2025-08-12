import flet as ft

def main(page: ft.Page):
    page.title = "DataTable demo (fixed)"
    page.padding = 16
    page.scroll = "auto"

    # 데모 데이터
    data = [
        {"id": 101, "name": "Alice",   "score": 87, "active": True},
        {"id": 102, "name": "Bob",     "score": 73, "active": False},
        {"id": 103, "name": "Charlie", "score": 92, "active": True},
        {"id": 104, "name": "Daisy",   "score": 64, "active": False},
        {"id": 105, "name": "Ethan",   "score": 81, "active": True},
    ]
    selected_ids: set[int] = set()

    # 정렬 상태
    sort_column_index = 1  # 0=Select, 1=ID, 2=Name, 3=Score, 4=Active
    sort_ascending = True

    status = ft.Text(color=ft.Colors.GREY_700)

    # --- 정렬 핸들러 팩토리 (table 필요하므로 이후에 바인딩) ---
    def on_sort_factory(col_idx: int):
        def _on_sort(e):
            nonlocal sort_column_index, sort_ascending
            if sort_column_index == col_idx:
                sort_ascending = not sort_ascending
            else:
                sort_column_index = col_idx
                sort_ascending = True
            table.sort_column_index = sort_column_index
            table.sort_ascending = sort_ascending
            build_rows()
        return _on_sort

    # --- DataTable: 생성 시 columns를 미리 채워둠(중요!) ---
    table = ft.DataTable(
        sort_column_index=sort_column_index,
        sort_ascending=sort_ascending,
        columns=[
            ft.DataColumn(ft.Text("Select")),                                # 0
            ft.DataColumn(ft.Text("ID"),    numeric=True,  on_sort=on_sort_factory(1)),
            ft.DataColumn(ft.Text("Name"),                  on_sort=on_sort_factory(2)),
            ft.DataColumn(ft.Text("Score"), numeric=True,  on_sort=on_sort_factory(3)),
            ft.DataColumn(ft.Text("Active"),               on_sort=on_sort_factory(4)),
        ],
        rows=[],  # 빈 rows는 허용
    )

    # --- rows를 재구성하는 함수 ---
    def build_rows():
        # 정렬 반영
        key_funcs = {
            1: lambda r: r["id"],
            2: lambda r: r["name"].lower(),
            3: lambda r: r["score"],
            4: lambda r: r["active"],
        }
        if sort_column_index in key_funcs:
            d_sorted = sorted(data, key=key_funcs[sort_column_index], reverse=not sort_ascending)
        else:
            d_sorted = list(data)

        rows: list[ft.DataRow] = []

        def close_dialog(dialog: ft.AlertDialog):
            dialog.open = False
            page.update()

        for row in d_sorted:
            row_id = row["id"]
            is_sel = row_id in selected_ids

            # 선택 체크박스
            sel_cell = ft.DataCell(
                ft.Checkbox(
                    value=is_sel,
                    on_change=lambda e, rid=row_id: toggle_select(rid, e.control.value),
                )
            )

            id_cell = ft.DataCell(ft.Text(str(row["id"])))

            # 이름 셀(수정 다이얼로그)
            def make_name_cell(r):
                name_field = ft.TextField(label="Name", autofocus=True, width=260)

                def open_edit_dialog(e):
                    name_field.value = r["name"]
                    dlg.data = r
                    dlg.open = True
                    page.open(dlg)
                    page.update()

                def save_name(e):
                    rec = dlg.data
                    newv = (name_field.value or "").strip()
                    if newv:
                        rec["name"] = newv
                    dlg.open = False
                    build_rows()
                    page.update()

                dlg = ft.AlertDialog(
                    modal=True,
                    title=ft.Text(f"Edit name (ID {r['id']})"),
                    content=name_field,
                    actions=[
                        ft.TextButton("Cancel", on_click=lambda e: close_dialog(dlg)),
                        ft.FilledButton("Save", on_click=save_name),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )
                # Flet는 page.dialog에 단일 다이얼로그를 할당
                # 열 때마다 바꿔 끼우면 됩니다.
                def show_dialog(e):
                    page.dialog = dlg
                    open_edit_dialog(e)

                return ft.DataCell(
                    ft.Row(
                        [
                            ft.Text(r["name"]),
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Edit",
                                on_click=show_dialog,
                                icon_color=ft.Colors.BLUE_400,
                                width=34,
                                height=34,
                            ),
                        ],
                        spacing=6,
                    )
                )

            name_cell = make_name_cell(row)

            # 점수 +1
            def inc_score(e, r=row):
                r["score"] += 1
                build_rows()
                page.update()

            score_cell = ft.DataCell(
                ft.Row(
                    [
                        ft.Text(str(row["score"])),
                        ft.IconButton(
                            icon=ft.Icons.ADD,
                            tooltip="+1",
                            on_click=inc_score,
                            icon_color=ft.Colors.GREEN,
                            width=34,
                            height=34,
                        ),
                    ],
                    spacing=6,
                )
            )

            # Active 스위치 + 칩 스타일
            def make_active_cell(r):
                # 상태 텍스트와 컨테이너를 별도로 변수로 둠
                status_text = ft.Text(
                    "Active" if r["active"] else "Inactive",
                    color=ft.Colors.GREEN_700 if r[
                        "active"] else ft.Colors.GREY_600,
                    size=12,
                )
                status_container = ft.Container(
                    bgcolor=ft.Colors.GREEN_100 if r[
                        "active"] else ft.Colors.GREY_200,
                    border_radius=999,
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                    content=status_text,
                )

                def toggle_active(e):
                    r["active"] = e.control.value
                    status.value = f"ID {r['id']} active = {r['active']}"
                    # 텍스트/색상 갱신
                    status_text.value = "Active" if r["active"] else "Inactive"
                    status_text.color = ft.Colors.GREEN_700 if r[
                        "active"] else ft.Colors.GREY_600
                    status_container.bgcolor = ft.Colors.GREEN_100 if r[
                        "active"] else ft.Colors.GREY_200
                    page.update()

                return ft.DataCell(
                    ft.Row(
                        [
                            ft.Switch(value=r["active"],
                                      on_change=toggle_active),
                            status_container
                        ],
                        spacing=8,
                    )
                )

            active_cell = make_active_cell(row)

            rows.append(
                ft.DataRow(
                    selected=is_sel,
                    cells=[sel_cell, id_cell, name_cell, score_cell, active_cell],
                )
            )

        table.rows = rows
        table.update()

    # --- 콜백들 ---
    def toggle_select(rid: int, val: bool):
        if val:
            selected_ids.add(rid)
        else:
            selected_ids.discard(rid)
        status.value = f"선택됨: {sorted(selected_ids)}"
        build_rows()
        page.update()

    def add_row(e=None):
        new_id = (max([r["id"] for r in data]) + 1) if data else 100
        data.append({"id": new_id, "name": f"User {new_id}", "score": 50, "active": False})
        status.value = f"행 추가: ID {new_id}"
        build_rows()
        page.update()

    def delete_selected(e=None):
        if not selected_ids:
            status.value = "선택된 행이 없습니다."
            page.update()
            return
        ids = set(selected_ids)
        remaining = [r for r in data if r["id"] not in ids]
        data.clear()
        data.extend(remaining)
        selected_ids.clear()
        status.value = "선택된 행 삭제 완료"
        build_rows()
        page.update()

    def add_one_to_all(e=None):
        for r in data:
            r["score"] += 1
        status.value = "모든 행 점수 +1"
        build_rows()
        page.update()

    # --- UI 구성 ---
    page.add(
        ft.Text("DataTable 작동 방식 데모", weight=ft.FontWeight.BOLD, size=18),
        ft.Text("• 정렬(on_sort) • 선택/일괄 삭제 • 셀 위젯(버튼/스위치/다이얼로그) • 실시간 갱신"),
        ft.Divider(),
        ft.Row(
            [
                ft.FilledButton("행 추가", icon=ft.Icons.ADD, on_click=add_row),
                ft.OutlinedButton("선택 삭제", icon=ft.Icons.DELETE, on_click=delete_selected),
                ft.TextButton("모두 +1", icon=ft.Icons.EXPOSURE_PLUS_1, on_click=add_one_to_all),
            ],
            spacing=10,
            wrap=True,
        ),
        ft.Container(height=8),
        table,
        ft.Divider(),
        status,
    )

    # 최초 rows 채우기
    build_rows()

ft.app(target=main)
