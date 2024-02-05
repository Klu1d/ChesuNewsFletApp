import flet as ft


def VerificationView(page, firebase):    
    def handle_sign_up(e):
        try:
            preloader()
            print(firebase.account_info()['emailVerified'])
            if firebase.account_info()['emailVerified'] == True:
                page.go('/news')
            else:
                handle_sign_in_error()
        except Exception as e:
            print(e)
        finally:
            preloader(False)
    
    def handle_sign_in_error(text='Ваш аккаунт не подтвержден'):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(text, color=ft.colors.WHITE),
            bgcolor=ft.colors.RED
        )
        page.snack_bar.open = True
        page.update()
    
    def preloader(boolevo = True):
        login_button.content.controls[0].visible = not (boolevo)
        login_button.content.controls[1].visible = boolevo
        page.update()   
        
    def on_click_back(e):
        firebase.remove_user()
        page.go('/register')
    
    back_button = ft.TextButton('Изменить почту', expand=1, on_click=on_click_back)
    login_button = ft.ElevatedButton(content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text('Войти', visible=True), ft.ProgressRing(visible=False, width=30, height=30)]), on_click=handle_sign_up, expand=2,  height=40,
        style=ft.ButtonStyle(side=ft.BorderSide(1, ft.colors.PRIMARY, ), shape=ft.RoundedRectangleBorder(radius=10)))
    
    myPage = ft.Column(
        data='verification',
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Container(
                    padding=15,
                    content=ft.Column(
                        scroll='hidden', #без него не получается поднять форму регистрации вверх
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text('Верификация', size=26),
                            ft.Card(
                                width=410,
                                content=ft.Container(
                                    padding=20,
                                    content=ft.Column(
                                        controls=[
                                            ft.Text('На вашу почту отправлена ссылка для подтверждение аккаунта. Пожалуйста, нажмите на ссылку и возвращайтесь'),
                                            ft.Row([back_button, login_button],
                                                alignment=ft.MainAxisAlignment.CENTER),
                                        ],
                                    ),
                                ),
                            )
                        ]
                    )
                )
            )
        ]
    )
    
    
    return {
        'view': myPage,
    }