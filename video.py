import random
import flet as ft
import flet_video as fv


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "TheEthicalVideo"
    page.window.always_on_top = True
    page.spacing = 16
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- 샘플 미디어(그대로) ---
    sample_media = [
        fv.VideoMedia("https://user-images.githubusercontent.com/28951144/229373720-14d69157-1a56-4a78-a2f4-d7a134d7c3e9.mp4"),
        fv.VideoMedia("https://user-images.githubusercontent.com/28951144/229373718-86ce5e1d-d195-45d5-baa6-ef94041d0b90.mp4"),
        fv.VideoMedia("https://user-images.githubusercontent.com/28951144/229373716-76da0a4e-225a-44e4-9ee7-3e9006dbc3e3.mp4"),
        fv.VideoMedia("https://user-images.githubusercontent.com/28951144/229373695-22f88f13-d18f-4288-9bf1-c3e078d83722.mp4"),
        fv.VideoMedia(
            "https://user-images.githubusercontent.com/28951144/229373709-603a7a89-2105-4e1b-a5a5-a6c3567c9a59.mp4",
            extras={"artist": "Thousand Foot Krutch", "album": "The End Is Where We Begin"},
            http_headers={"Foo": "Bar", "Accept": "*/*"},
        ),
    ]

    # --- 비주얼 상태 ---
    info = ft.Text("", size=12, color=ft.Colors.GREY_700)
    err  = ft.Text("", size=12, color=ft.Colors.RED_600)

    # --- Video ---
    video = fv.Video(
        expand=True,
        playlist=sample_media,            # 전체를 초기 재생목록으로
        playlist_mode=fv.PlaylistMode.LOOP,
        fill_color=ft.Colors.BLUE_400,
        aspect_ratio=16 / 9,
        volume=100,
        autoplay=False,
        filter_quality=ft.FilterQuality.HIGH,
        muted=False,
        on_loaded=lambda e: (set_info("로딩 완료"), clear_err()),
        on_enter_fullscreen=lambda e: set_info("전체화면 진입"),
        on_exit_fullscreen=lambda e: set_info("전체화면 종료"),
        on_completed=lambda e: set_info("재생 완료"),
        on_error=lambda e: set_err(f"오류: {e.data or '알 수 없는 오류'}"),
    )

    # --- 유틸 ---
    def set_info(msg: str):
        info.value = msg; page.update()

    def set_err(msg: str):
        err.value = msg; page.update()

    def clear_err():
        err.value = ""; page.update()

    def pl_len() -> int:
        try:
            return len(video.playlist)
        except Exception:
            return 0

    def refresh_buttons():
        n = pl_len()
        prev_btn.disabled = n <= 1
        next_btn.disabled = n <= 1
        jump_btn.disabled = n == 0
        remove_btn.disabled = n == 0
        page.update()

    # --- 핸들러(동기 / 아이콘 버튼) ---
    def h_play(e):
        try:
            video.play(); set_info("재생")
        except Exception as ex:
            set_err(f"Play 실패: {ex}")

    def h_pause(e):
        try:
            video.pause(); set_info("일시 정지")
        except Exception as ex:
            set_err(f"Pause 실패: {ex}")

    def h_play_pause(e):
        try:
            video.play_or_pause(); set_info("토글 재생/정지")
        except Exception as ex:
            set_err(f"Play/Pause 실패: {ex}")

    def h_stop(e):
        try:
            video.stop(); set_info("정지")
        except Exception as ex:
            set_err(f"Stop 실패: {ex}")

    def h_next(e):
        if pl_len() <= 1: return
        try:
            video.next(); set_info("다음 트랙")
        except Exception as ex:
            set_err(f"Next 실패: {ex}")

    def h_prev(e):
        if pl_len() <= 1: return
        try:
            video.previous(); set_info("이전 트랙")
        except Exception as ex:
            set_err(f"Previous 실패: {ex}")

    def h_seek_forward(e):
        try:
            video.seek(10_000); set_info("＋10s")
        except Exception as ex:
            set_err(f"Seek 실패: {ex}")

    def h_seek_back(e):
        try:
            cur = video.get_current_position() or 0
            video.seek(max(0, cur - 10_000)); set_info("−10s")
        except Exception as ex:
            set_err(f"Seek(−10s) 실패: {ex}")

    def h_jump_first(e):
        n = pl_len()
        if n == 0:
            set_err("Jump 실패: 플레이리스트가 비어 있음"); return
        try:
            video.jump_to(0); set_info("첫 트랙으로 점프")
        except Exception as ex:
            set_err(f"Jump 실패: {ex}")

    def h_add_media(e):
        try:
            video.playlist_add(random.choice(sample_media))
            set_info(f"트랙 추가 (총 {pl_len()}개)"); refresh_buttons()
        except Exception as ex:
            set_err(f"추가 실패: {ex}")

    def h_remove_media(e):
        n = pl_len()
        if n == 0: return
        try:
            idx = random.randrange(n)
            video.playlist_remove(idx)
            set_info(f"트랙 제거: {idx} (총 {pl_len()}개)"); refresh_buttons()
        except Exception as ex:
            set_err(f"제거 실패: {ex}")

    def h_volume(e: ft.ControlEvent):
        try:
            video.volume = e.control.value; page.update()
        except Exception as ex:
            set_err(f"볼륨 실패: {ex}")

    def h_rate_dd(e: ft.ControlEvent):
        try:
            rate = float(e.control.value)
            video.playback_rate = rate
            page.update()
        except Exception as ex:
            set_err(f"배속 실패: {ex}")

    # --- UI ---
    prev_btn   = ft.IconButton(icon=ft.Icons.SKIP_PREVIOUS,  tooltip="Previous",           on_click=h_prev)
    seek_b_btn = ft.IconButton(icon=ft.Icons.REPLAY_10,      tooltip="Seek -10s",          on_click=h_seek_back)
    play_btn   = ft.IconButton(icon=ft.Icons.PLAY_ARROW,     tooltip="Play",               on_click=h_play)
    pause_btn  = ft.IconButton(icon=ft.Icons.PAUSE,          tooltip="Pause",              on_click=h_pause)
    pp_btn     = ft.IconButton(icon=ft.Icons.PLAY_CIRCLE,    tooltip="Play/Pause",         on_click=h_play_pause)
    stop_btn   = ft.IconButton(icon=ft.Icons.STOP,           tooltip="Stop",               on_click=h_stop)
    seek_f_btn = ft.IconButton(icon=ft.Icons.FORWARD_10,     tooltip="Seek +10s",          on_click=h_seek_forward)
    next_btn   = ft.IconButton(icon=ft.Icons.SKIP_NEXT,      tooltip="Next",               on_click=h_next)
    jump_btn   = ft.IconButton(icon=ft.Icons.RESTART_ALT,    tooltip="Jump to first",      on_click=h_jump_first)
    add_btn    = ft.IconButton(icon=ft.Icons.QUEUE_PLAY_NEXT,tooltip="Add random media",   on_click=h_add_media)
    remove_btn = ft.IconButton(icon=ft.Icons.DELETE,         tooltip="Remove random media",on_click=h_remove_media)

    # 볼륨 슬라이더 + 재생속도 드롭다운 (같은 Row)
    vol_slider = ft.Slider(
        min=0, max=100, value=100, divisions=10, width=320,
        label="Volume = {value}%", on_change=h_volume,
    )
    rate_dd = ft.Dropdown(
        width=110,
        value="1.0",
        options=[ft.dropdown.Option(v) for v in ["0.5","0.75","1.0","1.25","1.5","2.0"]],
        on_change=h_rate_dd,
    )

    page.add(
        video,
        ft.Row(
            wrap=True,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=6,
            controls=[
                prev_btn, seek_b_btn, play_btn, pause_btn, pp_btn, stop_btn,
                seek_f_btn, next_btn, jump_btn, add_btn, remove_btn,
            ],
        ),
        # ✅ 볼륨 앞에 스피커 아이콘, 옆에 배속 드롭다운
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
            controls=[
                ft.Icon(ft.Icons.VOLUME_UP, color=ft.Colors.GREY_700),
                vol_slider,
                ft.Text("배속", color=ft.Colors.GREY_700),
                rate_dd,
            ],
        ),
        ft.Row([info], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([err],  alignment=ft.MainAxisAlignment.CENTER),
    )

    refresh_buttons()


ft.app(main)
