import pyrebase
import flet as ft
import json
from firebase.pyrebase import PyrebaseWrapper

def IndexView(page: ft.Page, firebase: PyrebaseWrapper):
    def on_load_index():
        try:
            page.dialog = verification_warn
            if firebase.check_token():
                if firebase.account_info().get('emailVerified'):
                    if firebase.check_token():
                        page.go('/news')
                else:
                    verification_warn.open = True
        except pyrebase.pyrebase.requests.exceptions.ConnectionError:
            handle_sign_in_error('Не соединения с интернетом')
        except pyrebase.pyrebase.HTTPError as e:
            print('Ошибка при входе пользователя: ', e)
            page.update()
            

    def handle_sign_in_error(text='Неправильный логин или пароль'):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(text, color=ft.colors.WHITE),
            bgcolor=ft.colors.RED,
            behavior=ft.SnackBarBehavior.FLOATING,
        )
        page.snack_bar.open = True
        page.update()

    def handle_sign_in(e):
        try:
            page.dialog = verification_warn
            firebase.sign_in(email.value, password.value)
            password.value = ''
            if firebase.account_info().get('emailVerified'):
                page.go('/news')
            else:
                verification_warn.open = True
        except pyrebase.pyrebase.requests.exceptions.ConnectionError:
            handle_sign_in_error('Нет соединения с интернетом')
        except pyrebase.pyrebase.HTTPError as e:
            error_json = json.loads(e.strerror)
            error_message = error_json["error"]["message"]
            print('Неправильный логин или парольHANLE:', error_message)
            handle_sign_in_error()
            page.update()
    
    def handle_sign_in_anonymous(e):
        try:
            page.client_storage.clear()
            firebase.login_in_anonymous()
            email.value = ''
            password.value = ''
            page.go('/news')
        except pyrebase.pyrebase.requests.exceptions.ConnectionError:
            handle_sign_in_error('Нет соединения с интернетом')
        except pyrebase.pyrebase.HTTPError as e:
            error_json = json.loads(e.strerror)
            error_message = error_json["error"]["message"]
            print('Ошибка HTTPError при входе анонима:', error_message)
            page.update()

    def handle_register(e):
        page.go('/register')
        page.update()
    
    def on_click_forgot_password(e):
        page.go('/forgot')
     
    verification_warn = ft.AlertDialog(
        adaptive=True, modal=True,
        title=ft.Text('Верификация', text_align=ft.TextAlign.CENTER),
        content=ft.Text('Указанный адрес электронной почты не прошел проверку верификации. Мы можем отправить на этот адрес ссылку для верификации', text_align=ft.TextAlign.CENTER),
        actions=[
            ft.TextButton('Отмена', on_click=lambda _: page.close_dialog()),
            ft.TextButton('Отправить', on_click=lambda _: firebase.auth.send_email_verification(firebase.idToken)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    email = ft.TextField(
        label='Почта', bgcolor='secondarycontainer, 0.225', 
        adaptive=True, dense=True, border_radius=8, border_color='grey, 0.5',
        prefix_icon=ft.icons.EMAIL, height=40, 
    )
    password = ft.TextField(
        label='Пароль', bgcolor='secondarycontainer, 0.225', 
        adaptive=True, dense=True, border_radius=8, border_color='grey, 0.5',
        prefix_icon=ft.icons.LOCK, password=True, height=40,  can_reveal_password=True, 
        content_padding=ft.padding.only(right=15), 
    )
    sign_in_button = ft.ElevatedButton(
        'Войти', 
        on_click=handle_sign_in, 
        expand=True, height=40,
        style=ft.ButtonStyle(side=ft.BorderSide(1, ft.colors.PRIMARY), 
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )
        
    register_button = ft.ElevatedButton(
        content=ft.Text('Регистрация'),
        on_click=handle_register, expand=True,  height=40,
        style=ft.ButtonStyle(side=ft.BorderSide(1, ft.colors.PRIMARY, ), shape=ft.RoundedRectangleBorder(radius=10)))
    
    sign_in_without = ft.TextButton(
        'Войти без аккаунта', 
        on_click=handle_sign_in_anonymous
    )
    forgot_password = ft.TextButton(
        'Забыли пароль?', 
        on_click=on_click_forgot_password
    )
  
    index_view = ft.View(
        route='/', 
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text('Вход в систему', size=26),
            ft.Card(
                width=310,
                content=ft.Container(
                    margin=ft.margin.symmetric(10, 10),
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Container(alignment=ft.alignment.center, content=email),
                            ft.Container(alignment=ft.alignment.center, content=password),
                            ft.Container(alignment=ft.alignment.center, content=ft.Row([register_button, sign_in_button])),
                            
                        ]
                    ),
                )
            ),
            ft.Row([sign_in_without, forgot_password],
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER
            ),
        ]
    )
    return {
        'view': index_view,
        'load': on_load_index
    }