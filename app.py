import datetime

import flet as ft

from models import CustomMap, Task, Session
from storage import TaskStorage, SessionStorage, ReportStorage
from ui_components import (
    TitleText, LabelText, StyledButton, SearchField, FilterDropdown,
    TaskListView, TaskRow, TopBar, MainColumn, LoginCard,
)


class DailyPlannerApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Ежедневник"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.window.prevent_close = True
        self.page.window.on_event = self._on_close

        self.login = ""
        self.session = None
        self.tasks = []
        self.selected = None
        self.search_query = ""
        self.filter_mode = "all"
        self.sort_mode = "high"

        self.priority_names = CustomMap()
        self.priority_names.set(1, "Высокий")
        self.priority_names.set(2, "Средний")
        self.priority_names.set(3, "Низкий")

        self._show_login()

    # ---------- Экран входа ----------
    def _show_login(self):
        self.page.controls.clear()
        self.login_field = ft.TextField(label="Логин", width=300, autofocus=True)
        self.login_error = ft.Text("", color=ft.Colors.RED, size=12)
        card = LoginCard(ft.Column([
            TitleText("Вход в ежедневник"),
            self.login_field,
            self.login_error,
            StyledButton("Войти", icon=ft.Icons.LOGIN, on_click=self._on_login),
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        self.page.add(ft.Column(
            [card], expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ))
        self.page.update()

    def _on_login(self, e):
        name = self.login_field.value.strip()
        if not name:
            self.login_error.value = "Введите логин"
            self.page.update()
            return
        self.login = name
        self.session = Session(name)
        self._show_main()

    # ---------- Главный экран ----------
    def _show_main(self):
        self.page.controls.clear()
        self.tasks = TaskStorage.load()
        if not self.tasks:
            self.tasks = [
                Task("Купить молоко", "2 литра", "обычная", "Дом", 2),
                Task("Сдать отчёт", "Квартальный", "рабочая", "Работа", 1),
                Task("Готовиться к экзамену", "Главы 5-7", "учебная", "Универ", 1),
            ]
            for i, t in enumerate(self.tasks, 1):
                t.id = i
            TaskStorage.save(self.tasks)

        self.search_field = SearchField(on_change=self._on_search)
        self.filter_dd = FilterDropdown(
            "Статус",
            [("all", "Все задачи"), ("done", "Выполненные"), ("todo", "Оставшиеся")],
            "all", on_select=self._on_filter,
        )
        self.sort_dd = FilterDropdown(
            "Сортировка",
            [("high", "Сначала высокий"), ("low", "Сначала низкий")],
            "high", on_select=self._on_sort,
        )
        self.stats_text = LabelText("")
        self.tasks_view = TaskListView()

        btns = ft.Row([
            StyledButton("Добавить", icon=ft.Icons.ADD, on_click=self._on_add),
            StyledButton("Изменить", icon=ft.Icons.EDIT, on_click=self._on_edit),
            StyledButton("Удалить", icon=ft.Icons.DELETE, on_click=self._on_delete),
            StyledButton("Отметить выполненной", icon=ft.Icons.CHECK,
                         on_click=self._on_toggle),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)

        box = ft.Container(
            content=self.tasks_view, width=800, padding=8,
            border=ft.Border.all(1, ft.Colors.GREY_300), border_radius=8,
        )

        self.page.add(MainColumn([
            TitleText("Мой ежедневник"),
            TopBar([self.search_field, self.filter_dd, self.sort_dd]),
            self.stats_text,
            box,
            btns,
        ]))
        self._refresh()

    # ---------- Отображение ----------
    def _filtered(self):
        res = []
        for t in self.tasks:
            if self.search_query and self.search_query.lower() not in t.title.lower():
                continue
            if self.filter_mode == "done" and not t.completed:
                continue
            if self.filter_mode == "todo" and t.completed:
                continue
            res.append(t)
        res.sort(key=lambda t: t.priority, reverse=(self.sort_mode == "high"))
        return res

    def _refresh(self):
        shown = self._filtered()
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t.completed)
        self.stats_text.value = (
            f"Всего: {total}   |   Выполнено: {done}   |   Осталось: {total - done}"
        )
        self.tasks_view.controls.clear()
        for t in shown:
            self.tasks_view.controls.append(
                TaskRow(t, self.priority_names,
                        on_click=(lambda task=t: lambda e: self._select(task))())
            )
        self.page.update()

    def _select(self, task):
        self.selected = task
        self.stats_text.value = f"Выбрана: {task.title}"
        self.page.update()

    # ---------- Обработчики ----------
    def _on_search(self, e):
        self.search_query = e.control.value
        self._refresh()

    def _on_filter(self, e):
        self.filter_mode = e.control.value
        self._refresh()

    def _on_sort(self, e):
        self.sort_mode = e.control.value
        self._refresh()

    def _on_add(self, e):
        self._open_dialog(None)

    def _on_edit(self, e):
        if not self.selected:
            self.stats_text.value = "Сначала выберите задачу"
            self.page.update()
            return
        self._open_dialog(self.selected)

    def _on_delete(self, e):
        if not self.selected:
            self.stats_text.value = "Сначала выберите задачу"
            self.page.update()
            return
        self.tasks.remove(self.selected)
        self.selected = None
        TaskStorage.save(self.tasks)
        self._refresh()

    def _on_toggle(self, e):
        if not self.selected:
            self.stats_text.value = "Сначала выберите задачу"
            self.page.update()
            return
        self.selected.completed = not self.selected.completed
        TaskStorage.save(self.tasks)
        self._refresh()

    # ---------- Диалог добавления/редактирования ----------
    def _open_dialog(self, task):
        title_f = ft.TextField(label="Название", value=task.title if task else "")
        desc_f = ft.TextField(label="Описание", value=task.description if task else "")
        type_dd = ft.Dropdown(
            label="Тип", value=task.type if task else "обычная",
            options=[ft.dropdown.Option(t) for t in Task.TYPES],
        )
        proj_f = ft.TextField(label="Проект", value=task.project if task else "")
        prio_dd = ft.Dropdown(
            label="Приоритет",
            value=str(task.priority) if task else "2",
            options=[
                ft.dropdown.Option("1", "Высокий"),
                ft.dropdown.Option("2", "Средний"),
                ft.dropdown.Option("3", "Низкий"),
            ],
        )

        def save(e):
            t = task or Task()
            if not title_f.value.strip():
                return
            t.title = title_f.value.strip()
            t.description = desc_f.value.strip()
            t.type = type_dd.value
            t.project = proj_f.value.strip()
            t.priority = int(prio_dd.value)
            if task is None:
                t.id = max([x.id for x in self.tasks], default=0) + 1
                self.tasks.append(t)
            TaskStorage.save(self.tasks)
            self.page.pop_dialog()
            self._refresh()

        dlg = ft.AlertDialog(
            title=ft.Text("Добавить задачу" if task is None else "Изменить задачу"),
            content=ft.Column([title_f, desc_f, type_dd, proj_f, prio_dd],
                              spacing=10, width=400),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: self.page.pop_dialog()),
                ft.TextButton("Сохранить", on_click=save),
            ],
        )
        self.page.show_dialog(dlg)

    # ---------- Закрытие ----------
    async def _on_close(self, e: ft.WindowEvent):
        if e.type == ft.WindowEventType.CLOSE:
            if self.session:
                self.session.time_out = datetime.datetime.now()
                SessionStorage.log(self.session)
                ReportStorage.write(self.session)

            self.page.window.prevent_close = False
            self.page.window.on_event = None
            self.page.update()
            await self.page.window.destroy()