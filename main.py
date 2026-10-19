import flet as ft

from app import DailyPlannerApp


def main(page: ft.Page):
    DailyPlannerApp(page)


if __name__ == "__main__":
    ft.run(main)