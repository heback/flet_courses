import flet
from flet import *
import calendar
import datetime

# 상수
CELL_SIZE = (28, 28)
CELL_BG_COLOR = colors.WHITE10
TODAY_BG_COLOR = colors.TEAL_600


class SetCalendar(UserControl):
    def __init__(self):

        super().__init__()

    def build(self):
        return None


# 메인
def main(page: Page):
    page.horizontal_alignment = alignment.center
    page.vertical_alignment = alignment.center
    page.padding = 80


    page.add()
    page.update()


if __name__ == '__main__':
    flet.app(target=main)