import json
import flet as ft

from firebase.pyrebase import PyrebaseWrapper


def SettingsView(page: ft.Page, firebase: PyrebaseWrapper):
    def on_load_settings_view():
        page.update()
    
    def on_change_slider(e):
        e.page.client_storage.set('slider_value', e.control.value)
        e.page.update()
    
    def on_click_theme_mode(e):
        e.page.theme_mode = list(e.control.selected)[0]
        e.page.client_storage.set('theme_mode', e.page.theme_mode)
        page.update()

    with open('assets/json/categories_info.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    faculties =  data['categories_info']
    roles = list(data['roles'].keys())

    faculty_fullname_alert = ft.AlertDialog(
        adaptive=True,
        actions_alignment=ft.MainAxisAlignment.SPACE_AROUND,
        actions=[
            ft.TextButton('Ок', on_click=lambda _: page.close_dialog()),  
        ]
    )
    resize_default_text = ft.Row(
        height=50,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=0,
        controls=[
            ft.Text('T', size=16), 
            ft.Slider(
                min=10, 
                max=100,
                value=32.5,
                divisions=4, 
                width=250, 
                height=100, 
                adaptive=True,
                label='{value}%',
                on_change=on_change_slider,
            ), 
            ft.Text('T', size=23)
        ]
    ) 
    settings_view = ft.View(
        adaptive=True,
        route='/profile',
        appbar=ft.AppBar(
            center_title=True,
            title=ft.Text('Настройки приложения'), 
        ),
        vertical_alignment=ft.MainAxisAlignment.START,
        spacing=25,
        controls=[
           ft.ListTile(
                title=ft.Text('Рубрики новостей'),
                trailing=ft.Icon(ft.icons.KEYBOARD_ARROW_RIGHT),
            ),
            ft.ListTile(
                title=ft.Text('Уведомления'),
                trailing=ft.Switch(
                    value=False,
                    thumb_icon= {
                        ft.MaterialState.SELECTED: ft.icons.CHECK,
                        ft.MaterialState.DISABLED: ft.icons.CLOSE,
                    }
                )
            ),
            ft.ListTile(
                title = ft.Text('Размер текста по-умолчанию'),
                subtitle=resize_default_text,
            ),
            ft.ListTile(
                title = ft.Text('Тема оформления'),
                subtitle=ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.SegmentedButton(
                        width=200,
                        on_change=on_click_theme_mode,
                        show_selected_icon=False,
                        selected={page.client_storage.get('theme_mode')},
                        segments=[
                            ft.Segment(
                                value=ft.ThemeMode.DARK.value,
                                icon=ft.Icon(ft.icons.DARK_MODE_ROUNDED),
                            ),
                            ft.Segment(
                                value=ft.ThemeMode.LIGHT.value,
                                icon=ft.Icon(ft.icons.LIGHT_MODE_ROUNDED),
                                
                            ),
                            ft.Segment(
                                value=ft.ThemeMode.SYSTEM.value,
                                icon=ft.Icon(ft.icons.CONTRAST_OUTLINED),
                            ),
                        ],
                    ),
                )
            ),
        ]
    )
    return {
        'view':settings_view,
        'load':on_load_settings_view,
    }