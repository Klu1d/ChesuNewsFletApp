import flet as ft

def IndexView(page, myPyrebase=None):
    title = 'Flet + Pyrebase'
   

    def on_load():
        try:
            preloader(True)
            if myPyrebase.check_token():
                page.go('/news')
            else:
                preloader(False)
        except Exception as e:
            preloader(False)

    def handle_sign_in_error():
        preloader(False)
        page.snack_bar = ft.SnackBar(
            content=ft.Text('Неправильный логин или пароль', color=ft.colors.WHITE),
            bgcolor=ft.colors.RED,
            behavior=ft.SnackBarBehavior.FLOATING,
        )
        page.snack_bar.open = True
        page.update()

    def handle_sign_in(e):
        try:
            preloader(True)
            myPyrebase.sign_in(email.value, password.value)
            password.value = ''
            page.go('/news')
        except:
            handle_sign_in_error()
            page.update()

    def handle_sign_in_anonymous(e):
        try:
            preloader(True)
            myPyrebase.login_in_anonymous()
            password.value = ''
            page.go('/news')
        except:
            handle_sign_in_error()
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

    def preloader(activate):
        if activate:
            page.overlay.append(ft.Container(bgcolor='background, 0.5', expand=True, disabled=True,alignment=ft.alignment.center, content=ft.ProgressRing()))
            page.update()
        else:
            page.overlay.clear()
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
        title=ft.Text('Важная информация!'),
        content=ft.Column(scroll='hidden',
            controls=[
                ft.Text('"Войти без аккаунта" — означает что вы можете пользоваться \
                        приложением без необходимости процесса регистрации. Что дает \
                        возможность просматривать текущие события в университете\n\nНо \
                        при наличии аккаунта в системе вы приобретаете особые регалии \
                        позволяющие взаимодействовать как с приложением, так и университетом', 
                        text_align='start')]),
        actions=[ft.TextButton('Хорошо!', on_click=close_dlg)],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    myPage = ft.Column(
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
                                alignment=ft.MainAxisAlignment.CENTER),
                        ]
                    )
                )
            )
        ]
    )
    
    return {
        'view':myPage,
        'title': title,
        'load': on_load
        }