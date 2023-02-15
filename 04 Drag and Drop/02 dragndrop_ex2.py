import flet as ft


def main(page: ft.Page):
    page.title = "Drag and Drop example 2"
    src_txt = ft.Text('1', size=20)
    target_txt = ft.Text('0', size=20)

    def drag_accept(e):

        tmp = target_txt.value
        target_txt.value = src_txt.value
        src_txt.value = tmp
        # get draggable (source) control by its ID
        src = page.get_control(e.src_id)
        # update text inside draggable control
        src.content.content.value = src_txt.value
        # reset source group, so it cannot be dropped to a target anymore
        # src.group = ""
        # update text inside drag target control
        e.control.content.content.value = target_txt.value
        # reset border
        e.control.content.border = None

        page.update()

    def drag_will_accept(e):
        # black border when it's allowed to drop and red when it's not
        e.control.content.border = ft.border.all(
            2, ft.colors.BLACK45 if e.data == "true" else ft.colors.RED
        )
        e.control.update()

    def drag_leave(e):
        e.control.content.border = None
        page.update()


    page.add(
        ft.Row(
            [
                src_txt,
                target_txt
            ]
        )
    )
    page.add(
        ft.Row(
            [
                ft.Draggable(
                    group="number",
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.colors.CYAN_200,
                        border_radius=5,
                        content=ft.Text(src_txt.value, size=20),
                        alignment=ft.alignment.center,
                    ),
                    content_when_dragging=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.colors.BLUE_GREY_200,
                        border_radius=5,
                    ),
                    content_feedback=ft.Text(src_txt.value, size=20),
                ),
                ft.Container(width=100),
                ft.DragTarget(
                    group="number",
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.colors.PINK_200,
                        border_radius=5,
                        content=ft.Text(target_txt.value, size=20),
                        alignment=ft.alignment.center,
                    ),
                    on_accept=drag_accept,
                    on_will_accept=drag_will_accept,
                    on_leave=drag_leave,
                ),
            ]
        )
    )


ft.app(target=main)

