import pyrebase
import flet as ft


def IndexView(page, firebase=None):
    def on_load_index():
        try:
            if firebase.check_token():
                page.go('/news')
        except pyrebase.pyrebase.requests.exceptions.ConnectionError:
            handle_sign_in_error('Не соединения с интернетом')
        except pyrebase.pyrebase.HTTPError as e:
            print('Ошибка при входе пользователя: ', e)
            
            page.update()
            #return [] потом убрать комент и оставить return !напоминание

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
            password.value = ''
            page.go('/news')
        except pyrebase.pyrebase.requests.exceptions.ConnectionError:
            handle_sign_in_error('Нет соединения с интернетом')
        except pyrebase.pyrebase.HTTPError as e:
            print('Неправильный логин или пароль: ', e)
            handle_sign_in_error()
            page.update()
    
    def handle_sign_in_anonymous(e):
        try:
            firebase.login_in_anonymous()
            email.value = ''
            password.value = ''
            page.go('/news')
            page.update()
        except pyrebase.pyrebase.requests.exceptions.ConnectionError:
            handle_sign_in_error('Нет соединения с интернетом')
        except pyrebase.pyrebase.HTTPError as e:
            print('Ошибка HTTPError при входе анонима:', e)
            page.update()

    def handle_register(e):
        page.go('/register')
        page.update()

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def close_dlg(e):
        dlg_modal.open = False
        page.update()


            
    banner = ft.Image(src='./logo/logo.png', expand=True, border_radius=5, fit=ft.ImageFit.COVER)
    welcome_text = ft.Text('Welcome', size=26, bottom=10, right=10, color=ft.colors.WHITE70)
    
    email = ft.TextField(label='Почта', border=ft.InputBorder.UNDERLINE, prefix_icon=ft.icons.EMAIL, expand=True)
    password = ft.TextField(label='Пароль', border=ft.InputBorder.UNDERLINE, prefix_icon=ft.icons.LOCK, password=True, can_reveal_password=True, expand=True)

    sign_in_button = ft.ElevatedButton('Войти', on_click=handle_sign_in, expand=True, height=40,
        style=ft.ButtonStyle(side=ft.BorderSide(1, ft.colors.PRIMARY, ), shape=ft.RoundedRectangleBorder(radius=10)))
        
    register_button = ft.ElevatedButton('Создать аккаунт', on_click=handle_register, expand=True,  height=40,
        style=ft.ButtonStyle(side=ft.BorderSide(1, ft.colors.PRIMARY, ), shape=ft.RoundedRectangleBorder(radius=10)))
    
    sign_in_without = ft.TextButton('Войти без аккаунта', on_click=handle_sign_in_anonymous)
    info = ft.IconButton(ft.icons.INFO_OUTLINE_ROUNDED, on_click=open_dlg_modal)
    
    dlg_modal = ft.AlertDialog(
        modal=True,
        adaptive=True,
        content_padding=15,
        title=ft.Text('Важная информация о вашем статусе'),
        content=ft.Column(scroll='hidden',
            controls=[
                ft.Text(
                    'Хотим обратить ваше внимание на то, что войдя в приложение анонимно, ' +
                    'вы можете пользоваться базовыми функциями, но у вас нет доступа ' +
                    'ко всем возможностям и преимуществам, которые предоставляет регистрация.\n\n' +
                    'Зарегистрированные пользователи имеют доступ к персонализированным настройкам,' +
                    'сохранению данных и предпочтений, а также к расширенным функциям приложения. ',
                 
                    text_align='start')]),
        actions=[ft.TextButton('Хорошо!', on_click=close_dlg)],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    def lll(e):
        firebase.sign_in('7576457@mail.ru', 'hgh28hh')
        page.go('/news')
        page.update()
        
    textButton = ft.TextButton('са логини пароли', on_click=lll)
    not_have_connect = ft.Container(
        alignment=ft.alignment.center,
        content=ft.Column(
            [
                ft.Text('Нет соединения с интернетом!'),
                ft.ElevatedButton('Повторить попытку'),
            ]
        )
        
    )
    index_view = ft.Column(
        expand=True,
        data='index',
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Container(
                    padding=20,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text('Вход в систему', size=26),
                            ft.Card(
                                width=400,
                                height=300,
                                content=ft.Container(
                                    padding=25,
                                    content=ft.Column([
                                        ft.Row([email],
                                            alignment=ft.MainAxisAlignment.CENTER),
                                        ft.Row([password],
                                            alignment=ft.MainAxisAlignment.CENTER),
                                        ft.Row([sign_in_button],
                                            alignment=ft.MainAxisAlignment.CENTER),
                                        ft.Row([register_button],
                                            alignment=ft.MainAxisAlignment.CENTER),
                                        ],
                                        
                                    ),
                                ),
                            ),
                            ft.Row([sign_in_without, info, textButton],
                                spacing=0,
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                        ]
                    )
                )
            )
        ]
    )
    
    return {
        'view': index_view,
        'load': on_load_index
    }