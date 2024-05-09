
import flet as ft

from firebase.pyrebase import PyrebaseWrapper


def PersonView(page: ft.Page, firebase: PyrebaseWrapper):
    def on_load_person_view():
        page.update()

    person_view = ft.View(
        adaptive=True,
        route='/profile', padding=0, scroll='hidden',
        appbar=ft.AppBar(
            center_title=True,
            title=ft.Text('Персональные данные'), 
        ),
        controls=[
            ft.Column(
                spacing=5,
                controls=[
                    ft.ListTile(
                        leading=ft.Text('Статус: '),
                        title=ft.Text(page.client_storage.get('role'))
                    ),
                    ft.ListTile(
                        title=ft.Row([ft.Text('Почта: '), ft.Text(page.client_storage.get('email'))])
                    ),
                ]
            ),
            ft.Column(
                spacing=5,
                controls=[
                    ft.ListTile(
                        title=ft.Text('Изменить пароль'),
                        leading=ft.Icon(ft.icons.PASSWORD_ROUNDED),
                        on_click=lambda _: page.go('/change_pass'),
                    ),
                ]
            ),
        ]
    )
    return {
        'view':person_view,
        'load':on_load_person_view,
    }