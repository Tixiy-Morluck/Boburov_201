import flet as ft


class TitleText(ft.Text):
    def __init__(self, value):
        super().__init__(value=value, size=24,
                         weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700)


class LabelText(ft.Text):
    def __init__(self, value):
        super().__init__(value=value, size=14, color=ft.Colors.GREY_800)


class StyledButton(ft.Button):
    def __init__(self, text, on_click=None, icon=None):
        super().__init__(content=text, icon=icon, on_click=on_click,
                         bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE)


class SearchField(ft.TextField):
    def __init__(self, on_change=None):
        super().__init__(label="Поиск по названию", width=300,
                         on_change=on_change, border_radius=8, filled=True)


class FilterDropdown(ft.Dropdown):
    def __init__(self, label, options, value, on_select=None, width=200):
        super().__init__(
            label=label, width=width, value=value,
            options=[ft.dropdown.Option(k, v) for k, v in options],
            on_select=on_select,
        )


class TaskListView(ft.ListView):
    def __init__(self):
        super().__init__(spacing=6, padding=10, height=300, auto_scroll=True)


class TaskRow(ft.Container):
    def __init__(self, task, priority_names=None, on_click=None):
        pname = (priority_names.get(task.priority, str(task.priority))
                 if priority_names else str(task.priority))
        bg = ft.Colors.GREEN_50 if task.completed else ft.Colors.GREY_100
        info = ft.Column([
            ft.Text(task.title, weight=ft.FontWeight.BOLD),
            ft.Text(task.description, size=12, color=ft.Colors.GREY_600),
            ft.Text(f"{task.type} | {task.project} | Приоритет: {pname}",
                    size=11, color=ft.Colors.GREY_500),
        ], spacing=2, expand=True)
        super().__init__(
            content=ft.Row(
                [ft.Checkbox(value=task.completed, disabled=True), info],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=10, border_radius=8, bgcolor=bg, on_click=on_click,
        )


class TopBar(ft.Row):
    def __init__(self, controls):
        super().__init__(controls=controls, width=800,
                         alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                         vertical_alignment=ft.CrossAxisAlignment.CENTER)


class MainColumn(ft.Column):
    def __init__(self, controls):
        super().__init__(controls=controls, spacing=12,
                         horizontal_alignment=ft.CrossAxisAlignment.CENTER)


class LoginCard(ft.Container):
    def __init__(self, content):
        super().__init__(content=content, padding=30, border_radius=12,
                         bgcolor=ft.Colors.WHITE, width=380,
                         shadow=ft.BoxShadow(blur_radius=15,
                                             color=ft.Colors.BLACK_12))