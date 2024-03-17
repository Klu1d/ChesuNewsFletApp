
import flet as ft

from firebase.flet_pyrebase import PyrebaseWrapper

def AccountView(page: ft.Page, firebase: PyrebaseWrapper):
    def on_load_account():
        if page.client_storage.get('role') == 'Аноним':
            pass
        else:
            page.client_storage.get('username')

    def build():
        pass
    
    
    def handle_logout(*e):
        firebase.kill_all_streams()
        firebase.sign_out()
        page.floating_action_button.visible = False
        del page.views[1]
        page.go('/')
        
    
    board_info = ft.Container(
        
        
        border_radius=15,
        padding=10,
        bgcolor=ft.colors.with_opacity(0.5, ft.colors.SECONDARY_CONTAINER),
        content=ft.Column(
            spacing=5,
            controls=[
                ft.Text(page.client_storage.get('username'), weight=ft.FontWeight.W_700, size=23),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        ft.Column(
                            [
                                ft.ListTile(leading=ft.Text(page.client_storage.get('role'), size=16))
                            ]
                        )
                    ]
                )
            ]
        ),

    )
    change_passwod_button = ft.TextButton('Изменить пароль')
    account_view = ft.View(
        route='/account',
        scroll='hidden',
        controls=[
            ft.AppBar(
                center_title=True,
                title=ft.Text('Личный кабинет', size=16), 
            ),

            ft.Container(
                height=page.height - 80,
                content=ft.Column(
                    scroll=None,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    
                    controls=[
                        board_info,
                        ft.Column([
                            ft.Row([change_passwod_button], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Row([ft.TextButton('Выйти', on_click=handle_logout, style=ft.ButtonStyle(color='error'))], alignment=ft.MainAxisAlignment.CENTER),
                           
                        ])
                    ]
                )
            )
            
        ]
    )
    return {
        'view':account_view,
        'load':on_load_account,
    }