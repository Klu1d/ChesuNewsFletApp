import re
import json
import requests
import flet as ft


def RegisterView(page, firebase):
    def handle_sign_up(e):
        try:
            preloader()
            back_button.disabled = True #чтобы нельзя было нажать на стрелку назад, во время создания аккаунта
            back_button.update()
            firebase.register_user(name.value.title(), last_name.value.title(), role.value, email.value, password.value)
            email.value, confirm.value, password.value  = '', '', '',         
            page.go('/verification')
        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            if error == 'EMAIL_EXISTS':
                handle_sign_in_error('Электронный адрес уже существует')
            else:
                print(error)
        except Exception as e:
            handle_sign_in_error()
        finally:
            back_button.disabled = False
            preloader(False)
        
        #не понимаю зачем использовать эти две строки, если в finally я использую preloader. 
        #Но иначе кнопка 'Создать аккаунт' не становится disabled=True, когда иду обратно из верификации в регистрацию 
        register_button.disabled = True
        page.update()
       

    def handle_sign_in_error(text='Что-то пошло не так. Пожалуйста, попробуйте еще раз'):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(text, color=ft.colors.WHITE),
            bgcolor=ft.colors.RED
        )
        page.snack_bar.open = True
        page.update()
         
    def preloader(boolevo = True):
        register_button.disabled = boolevo
        register_button.content.controls[0].visible = not (boolevo)
        register_button.content.controls[1].visible = boolevo
        page.update()

    def valid_username(e):
        valid_fields()
        validate_input(e, r'^[А-Яа-я]+$', '*Только кириллицей, без спец. символов и цифр')

    def valid_email(e):
        valid_fields()
        validate_input(e, r'^\w+[\w\.\+\-]*@\w+\.[a-z]{2,3}$', '*Некорректный адрес электронной почты')
   
    def validate_input(e, pattern, match_error):
        valid = bool(re.match(pattern, e.control.value))
        e.control.error_text = match_error if not valid and e.control.value != '' else ''
        valid_fields()
        page.update()

    def valid_password(e):
        second_password = e.control.value
        match_error = 'Пароли не совпадают*'
        password.error_text = confirm.error_text = match_error if second_password != password.value else ''
        valid_fields()
        page.update()

    def valid_fields():
        #Проверяет нет ли ошибок и не пуста ли форма, иначе кнопку нельзя нажать
        textfields = [name, last_name, email, password]
        not_emptys = all(value != '' for value in [field.value for field in textfields])
        not_errors = all(value == '' for value in [field.error_text for field in textfields])
        register_button.disabled = not (not_emptys and not_errors)
        
    def on_click_back(e):
        name.value, name.error_text = '', ''
        last_name.value, last_name.error_text = '', ''
        role.value, role.error_text = '', ''
        password.value, password.error_text = '', ''
        confirm.value, confirm.error_text = '', ''
        email.value, email.error_text = '', ''
        page.go('/')
        
    
    banner = ft.Image(src='./logo/logo.png', width=250, border_radius=5, fit=ft.ImageFit.COVER)
    welcome_text = ft.Text('User Registration', size=26, bottom=10, right=10, color=ft.colors.WHITE70)
    
    name = ft.TextField(label='Имя', on_change=valid_username, border=ft.InputBorder.UNDERLINE, expand=True)
    last_name = ft.TextField(label='Фамилия', on_change=valid_username, border=ft.InputBorder.UNDERLINE, expand=True)
    role = ft.Dropdown(label='Кто вы?', prefix_text='Я ', options=[ft.dropdown.Option('Студент'), ft.dropdown.Option('Маг 3 уровня'), ft.dropdown.Option('Преподаватель')], border=ft.InputBorder.UNDERLINE, expand=True)
    email = ft.TextField(label='Почта', on_change=valid_email, border=ft.InputBorder.UNDERLINE, prefix_icon=ft.icons.EMAIL, expand=True)
    password = ft.TextField(label='Пароль',border=ft.InputBorder.UNDERLINE, expand=True, password=True, can_reveal_password=True)
    confirm = ft.TextField(label='Подтвердить пароль', border=ft.InputBorder.UNDERLINE, on_change=valid_password, expand=True, password=True, can_reveal_password=True)
    back_button = ft.TextButton(' ',icon=ft.icons.ARROW_BACK_ROUNDED, expand=1, on_click=on_click_back)
    register_button = ft.ElevatedButton(content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Text('Создать аккаунт', visible=True), ft.ProgressRing(visible=False, width=30, height=30, )]), 
        disabled=True, on_click=handle_sign_up, expand=3, height=40,
        style=ft.ButtonStyle(side=ft.BorderSide(1, ft.colors.PRIMARY, ), shape=ft.RoundedRectangleBorder(radius=10)))
    

    myPage = ft.Column(
        data='register',
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.alignment.center,
                content=ft.Container(
                    padding=15,
                    content=ft.Column(
                        scroll='hidden', #без него не получается поднять форму регистрации вверх
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text('Создание учетной записи', size=26),
                            ft.Card(
                                width=400,

                                content=ft.Container(
                                    padding=20,
                                    content=ft.Column(
                                        controls=[
                                            ft.Row([name],
                                                alignment=ft.MainAxisAlignment.CENTER),
                                            ft.Row([last_name],
                                                alignment=ft.MainAxisAlignment.CENTER),
                                            ft.Row([role],
                                                alignment=ft.MainAxisAlignment.CENTER),
                                            ft.Row([email],
                                                alignment=ft.MainAxisAlignment.CENTER),
                                            ft.Row([password],
                                                alignment=ft.MainAxisAlignment.CENTER),
                                            ft.Row([confirm],
                                                alignment=ft.MainAxisAlignment.CENTER),
                                            ft.Row([back_button, register_button],
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
        'view':myPage,
    }
