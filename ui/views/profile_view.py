
import flet as ft
import json

from firebase.pyrebase import PyrebaseWrapper
from ui.customs.cards import OldCard

def ProfileView(page: ft.Page, firebase: PyrebaseWrapper):
    def on_load_account():
        firebase.stream_user_account(build)
        

    def build(stream_data):
        if stream_data['data'] and not(stream_data['data'].get('status')):
            user_name = stream_data['data'].get('firstname') + ' ' + stream_data['data'].get('lastname')
            user_role = stream_data['data'].get('role') + ' из ' + stream_data['data'].get('faculty')
            profile_view.controls[0].controls[0].title = ft.Text(value=user_name, weight=ft.FontWeight.W_700, size=23)
            profile_view.controls[0].controls[0].subtitle = ft.Text(value=user_role, size=15)
        page.update()

    def on_click_logout_alert(e):
        page.dialog = quit_alert
        page.dialog.open = True
        page.update()

    def on_click_logout(e):
        page.close_dialog()
        page.client_storage.clear()
        del page.views[1:]
        page.go('')
        
        firebase.kill_all_streams()
        firebase.sign_out()
    

    quit_alert = ft.AlertDialog(
        adaptive=True,
        content=ft.Text('Вы уверены, что хотите выйти из своего аккаунта?'),
        actions_alignment=ft.MainAxisAlignment.SPACE_AROUND,
        actions=[
            ft.TextButton('Отменить', on_click=lambda _: page.close_dialog()),  
            ft.TextButton('Выйти', style=ft.ButtonStyle(color='error'), on_click=on_click_logout),  
        ]
    )


    profile_view = ft.View( 
        adaptive=True,
        route='/profile', 
        appbar=ft.AppBar(
            center_title=True,
            title=ft.Text('Профиль'), 
        ),
        vertical_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Column(adaptive=True,
                controls=[
                    ft.ListTile(
                        title_alignment=ft.ListTileTitleAlignment.THREE_LINE,
                    ),
                    # ft.ListTile(
                    #     content_padding=0,
                    #     title_alignment=ft.ListTileTitleAlignment.THREE_LINE,
                    #     title=ft.Container(ft.Text('Мои события', weight=ft.FontWeight.W_700, size=23), padding=ft.padding.only(left=20)),
                    #     subtitle=not_history,
                    # ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.PERSON_ROUNDED, color=ft.colors.INVERSE_SURFACE),
                        title=ft.Text('Персональные данные', color=ft.colors.INVERSE_SURFACE),
                        trailing=ft.Icon(ft.icons.KEYBOARD_ARROW_RIGHT, color=ft.colors.INVERSE_SURFACE),
                        on_click=lambda _: page.go('/person')
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.SETTINGS_ROUNDED, color=ft.colors.INVERSE_SURFACE),
                        title=ft.Text('Настроки приложения', color=ft.colors.INVERSE_SURFACE),
                        trailing=ft.Icon(ft.icons.KEYBOARD_ARROW_RIGHT, color=ft.colors.INVERSE_SURFACE),
                        on_click=lambda _: page.go('/settings')
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.INFO_OUTLINE_ROUNDED, color=ft.colors.INVERSE_SURFACE),
                        title=ft.Text('О приложении', color=ft.colors.INVERSE_SURFACE),
                        trailing=ft.Icon(ft.icons.KEYBOARD_ARROW_RIGHT, color=ft.colors.INVERSE_SURFACE),
                    ),
                ]
            ),
            ft.Column(
                spacing=5,
                controls=[
                    ft.ListTile(
                        title=ft.Text('Обратная связь', color=ft.colors.INVERSE_SURFACE),
                        leading=ft.Icon(ft.icons.SUPPORT, color=ft.colors.INVERSE_SURFACE),
                        #on_click=lambda _: page.go('/change_pass'),
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.EXIT_TO_APP_ROUNDED, color='error'),
                        title=ft.Text('Выйти', color='error'),
                        on_click=on_click_logout_alert
                    ),
                ]
            )
            
        
        
        ]
    )
    return {
        'view':profile_view,
        'load':on_load_account,
    }