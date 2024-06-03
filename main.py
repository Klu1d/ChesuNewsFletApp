import pyrebase
import flet as ft
import json
from controller import Controller
from firebase.scrapper import scrap_news
from firebase.pyrebase import PyrebaseWrapper

def main(page: ft.Page):
    def on_load_main():
        try:
            if firebase.check_token():
                page.go('/news')
                controller.user_info_cache(firebase)
        except pyrebase.pyrebase.requests.exceptions.ConnectionError:
            handle_sign_in_error('Не соединения с интернетом')
        except pyrebase.pyrebase.HTTPError as e:
            print('Ошибка при входе пользователя: ', e)
    
            
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
            firebase.sign_in(email.value, password.value)
            controller.user_info_cache(firebase) 
            page.go('/news')
            password.value = ''
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
        on_click=lambda _: page.go('/register'), expand=True,  height=40,
        style=ft.ButtonStyle(side=ft.BorderSide(1, ft.colors.PRIMARY, ), shape=ft.RoundedRectangleBorder(radius=10)))
    
    sign_in_without = ft.TextButton(
        'Войти без аккаунта', 
        on_click=handle_sign_in_anonymous
    )
    forgot_password = ft.TextButton(
        'Забыли пароль?', 
        on_click=lambda _: page.go('/forgot')
    )

    firebase = PyrebaseWrapper(page)
    controller = Controller(page, firebase)
    page.on_route_change = controller.route_change
    page.on_view_pop = controller.view_pop

    page.fonts = {
        "Number": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        #"Tab": "https://raw.githubusercontent.com/google/fonts/master/ofl/russoone/RussoOne-Regular.ttf",
        "Tab": "https://raw.githubusercontent.com/google/fonts/master/ofl/ptsansnarrow/PT_Sans-Narrow-Web-Bold.ttf",
        "Headline": "https://raw.githubusercontent.com/google/fonts/master/ofl/ptsansnarrow/PT_Sans-Narrow-Web-Bold.ttf",
        "Textline": "https://raw.githubusercontent.com/google/fonts/master/ofl/ptserif/PT_Serif-Web-Regular.ttf",
    }
    page.theme = ft.Theme(
        visual_density=ft.ThemeVisualDensity.COMPACT,
        color_scheme_seed=ft.colors.TEAL_800,
        font_family="Textline",
        color_scheme=ft.ColorScheme(
            primary=ft.colors.TEAL_800,
            on_primary=ft.colors.GREY_50,
            primary_container=ft.colors.GREY_200,
        ),
    )
    page.theme_mode = page.client_storage.get('theme_mode') if page.client_storage.get('theme_mode') else ft.ThemeMode.SYSTEM
    page.update()
    page.theme.page_transitions.ios = ft.PageTransitionTheme.CUPERTINO
    page.theme.page_transitions.android = ft.PageTransitionTheme.OPEN_UPWARDS
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.controls=[
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
    on_load_main()
    page.update()

ft.app(target=main)
