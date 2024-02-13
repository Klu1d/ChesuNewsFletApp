import flet as ft
import pyrebase
def IndexView(page, firebase=None):
    def on_load_index():
        try:
            if firebase.check_token():
                page.go('/news')
        except pyrebase.pyrebase.HTTPError as e:
            if e.response.status_code == 401:
                print("Ошибка аутентификации: Неверный токен или отсутствует аутентификация")
            else:
                print(f"Произошла ошибка HTTP: {e.response.status_code}")
            return []

    def handle_sign_in_error():
        page.snack_bar = ft.SnackBar(
            content=ft.Text('Неправильный логин или пароль', color=ft.colors.WHITE),
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
        except Exception as e:
            print('User IndexView: ', e)
            handle_sign_in_error()
            page.update()

    def handle_sign_in_anonymous(e):
        firebase.login_in_anonymous()
        email.value = ''
        password.value = ''
        page.go('/news')
        page.update()

    def handle_register(e):
        page.go('/register')

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
    )
    
    index_view = ft.Column(
        data='index',
        expand=True,
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
                            ft.Row([sign_in_without, info],
                                spacing=0,
                                alignment=ft.MainAxisAlignment.CENTER),
                        ]
                    )
                )
            )
        ]
    )
    
    return {
        'view':index_view,
        'load': on_load_index
    }