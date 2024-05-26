
import flet as ft

from firebase.pyrebase import PyrebaseWrapper


def PersonView(page: ft.Page, firebase: PyrebaseWrapper):
    def on_load_person_view():
        page.update()

    person_view = ft.View(
        adaptive=True,
        route='/profile', padding=ft.padding.symmetric(vertical=5, horizontal=20), scroll='hidden',
        appbar=ft.AppBar(
            center_title=True,
            title=ft.Text('Персональные данные'), 
        ),
        spacing=15,
        controls=[
            ft.Container(
                border_radius=10,
                bgcolor=ft.colors.SECONDARY_CONTAINER,
                alignment=ft.alignment.center,
                content=ft.Column(
                    spacing=0,
                    controls=[
                        ft.ListTile(
                            dense=True,
                            title_alignment=ft.ListTileTitleAlignment.CENTER,
                            on_click=lambda _: print('Имя'),
                            title=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text('Имя', size=18, weight=ft.FontWeight.BOLD),
                                    ft.Text(page.client_storage.get('firstname') + ' ' + page.client_storage.get('lastname'), size=18) if page.client_storage.get('firstname') else ft.Text()
                                ]
                            )
                        ),
                        ft.Divider(height=1),
                        ft.ListTile(
                            dense=True,
                            title_alignment=ft.ListTileTitleAlignment.CENTER,
                            on_click=lambda _: print('Статус'),
                            title=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text('Статус', size=18, weight=ft.FontWeight.BOLD),
                                    ft.Text(page.client_storage.get('role'), size=18),
                                ]
                            )
                        ),
                        ft.Divider(height=1),
                        ft.ListTile(
                            dense=True,
                            title_alignment=ft.ListTileTitleAlignment.CENTER,
                            on_click=lambda _: print('Почта'),
                            title=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text('Почта', size=18, weight=ft.FontWeight.BOLD),
                                    ft.Text(page.client_storage.get('email'),  size=18),
                                ]
                            )
                        ),

                    ]
                )
            ),
            ft.Container(
                border_radius=10,
                bgcolor=ft.colors.SECONDARY_CONTAINER,
                content=ft.ListTile(
                    title=ft.Text('Изменить текущий пароль', size=18, weight=ft.FontWeight.BOLD),
                    on_click=lambda _: page.go('/change_pass'),
                ),
            )

        ]
    )
    return {
        'view':person_view,
        'load':on_load_person_view,
    }