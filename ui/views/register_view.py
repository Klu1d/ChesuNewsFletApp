import re
import json
import requests
import flet as ft

from firebase.pyrebase import PyrebaseWrapper
from ui.customs.countdown import Countdown


def RegisterView(page: ft.Page, firebase: PyrebaseWrapper):
    def on_load_register_view():
        on_clear_view()

    def handle_sign_in(e):
        if firebase.account_info()['emailVerified'] == True:
            page.go('/news')
            on_clear_view()
        else:
            handle_sign_in_error('Ваш аккаунт не подтвержден. Проверьте почту')
        
    def handle_sign_up(e):
        try:
            forward_button.content = ft.ProgressRing(height=25, width=25)
            page.update()
            firebase.register_user(
                name=username.value.split()[0],
                lastname=username.value.split()[1],
                email=email.value,
                password=password.value,
                role=role.value,
                faculty=faculty.value
            )
            on_click_time(e)
            on_click_forward(e)
            forward_button.visible = False
            back_button.visible = False

        except requests.exceptions.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            if 'EMAIL_EXISTS' in error:
                handle_sign_in_error('Указанный адрес электронной почты уже используется')
                forward_button.content = ft.Text('Создать')
            elif 'INVALID_RECIPIENT_EMAIL' in error :
                handle_sign_in_error('Пользователя с такой почтой не существует')
                forward_button.content = ft.Text('Создать')
            else:
                handle_sign_in_error(error)
        finally:
            back_button.disabled = False
            
        page.update()
       
    def handle_sign_in_error(text='Что-то пошло не так. Пожалуйста, попробуйте еще раз'):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(text, color=ft.colors.WHITE),
            bgcolor=ft.colors.RED
        )

        page.snack_bar.open = True
        page.update()
    
    def on_clear_view():
        username.value, email.value, role.value, faculty.value, password.value = None, None, roles[3], faculties[3], None
        warn_email.visible, warn_name.visible, warn_password.visible = True, True, True
        back_button.visible, forward_button.disabled, forward_button.content = False, True, ft.Icon(ft.icons.ARROW_FORWARD_ROUNDED)
        forward_button.on_click=on_click_forward

        first_cards.offset = \
        ft.transform.Offset(0, 0)
        first_cards.offset = \
        ft.transform.Offset(0, 0)
        second_cards.offset = \
        ft.transform.Offset(0, 0)
        second_cards.offset = \
        ft.transform.Offset(0, 0)
        third_card.offset = \
        ft.transform.Offset(0, 0)
        page.update()
            
    def on_change_username(e):
        valid = bool(re.match(r'^[А-Яа-я]+\s[А-Яа-я]+$', e.control.value))
        if not valid and e.control.value:
            warn_name.visible = True
            forward_button.disabled = True
        elif len(e.control.value) < 2:
            warn_name.visible = True
            forward_button.disabled = True
        else:
            forward_button.disabled = False
            warn_name.visible = False
        page.update()

    def on_change_email(e):
        valid = bool(re.match(r'^\w+[\w\.\+\-]*@\w+\.[a-z]{2,3}$', e.control.value))
        if not valid and e.control.value:
            forward_button.disabled = True
            warn_email.visible = True
        elif len(e.control.value) == 0:
            forward_button.disabled = True
            warn_email.visible = True
        else:
            forward_button.disabled = False
            warn_email.visible = False

        if warn_password.visible:
            forward_button.disabled = True
        else:
            forward_button.disabled = False
        page.update()
    
    def on_change_password(e):
        valid = bool(re.match(r'^.{6,16}\s*$', e.control.value))
        if not valid and e.control.value:
            forward_button.disabled = True
            warn_password.visible = True
        elif len(e.control.value) == 0:
            forward_button.disabled = True
            warn_password.visible = True
        else:
            warn_password.visible = False
            if warn_email.visible:
                forward_button.disabled = True
            else:
                forward_button.disabled = False

        page.update()
    
    def on_click_forward(e):
        ind = first_cards.offset.x-1
        first_cards.offset = \
        ft.transform.Offset(ind, 0)
        first_cards.offset = \
        ft.transform.Offset(ind, 0)
        second_cards.offset = \
        ft.transform.Offset(ind, 0)
        second_cards.offset = \
        ft.transform.Offset(ind, 0)
        third_card.offset = \
        ft.transform.Offset(ind, 0)
        back_button.visible = True
        forward_button.disabled = True
        forward_button.content = ft.Text('Создать')
        forward_button.on_click = handle_sign_up
        page.update()

    def on_click_back(e):
        ind = first_cards.offset.x+1
        print(ind)
       
        first_cards.offset = \
        ft.transform.Offset(ind, 0)
        first_cards.offset = \
        ft.transform.Offset(ind, 0)
        second_cards.offset = \
        ft.transform.Offset(ind, 0)
        second_cards.offset = \
        ft.transform.Offset(ind, 0)
        third_card.offset = \
        ft.transform.Offset(ind, 0)
        back_button.visible = False
        forward_button.content = ft.Icon(ft.icons.ARROW_FORWARD_ROUNDED)
        forward_button.disabled = False
        forward_button.on_click = on_click_forward
        
        page.update()
        
    def on_change_faculty(e):
        faculty.value = faculties[int(e.data)]
        page.update()

    def on_change_role(e):
        role.value = roles[int(e.data)]
        page.update()

    def on_click_time(e):
        firebase.auth.send_email_verification(firebase.idToken)
        resend_button.running = True
        resend_button.seconds = resend_button.value
        resend_button.page.run_task(resend_button.update_timer)

    with open('assets/json/categories_info.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    faculties =  list(data['categories_info'].keys())
    roles = list(data['roles'].keys())

    back_button = ft.ElevatedButton(content=ft.Icon(ft.icons.ARROW_BACK_ROUNDED), on_click=on_click_back, visible=False)
    forward_button = ft.ElevatedButton(content=ft.Icon(ft.icons.ARROW_FORWARD_ROUNDED), on_click=on_click_forward, disabled=True)
    resend_button = Countdown(60, on_click_time)
    username = ft.TextField(
        label='Имя Фамилия', bgcolor='secondarycontainer, 0.225',
        dense=True, capitalization=ft.TextCapitalization.WORDS,
        on_change=on_change_username, height=40,
    )
    email = ft.TextField(
        label='Почта', bgcolor='secondarycontainer, 0.225',
        dense=True, suffix_icon=ft.icons.EMAIL,
        on_change=on_change_email, height=40,
    )
    password = ft.TextField(
        label='Пароль', bgcolor='secondarycontainer, 0.225',
        password=True, can_reveal_password=True, dense=True,
        on_change=on_change_password, height=40,
    )
    role = ft.Text(roles[3], weight=ft.FontWeight.BOLD)
    faculty = ft.Text(faculties[3], weight=ft.FontWeight.BOLD)

    picker_roles = ft.CupertinoPicker(
        selected_index=3,
        magnification=1.22,
        squeeze=1.2,
        use_magnifier=True,
        on_change=on_change_role,
        controls=[ft.Text(f) for f in roles],
    )
    picker_faculties = ft.CupertinoPicker(
        selected_index=3,
        magnification=1.22,
        squeeze=1.2,
        use_magnifier=True,
        on_change=on_change_faculty,
        controls=[ft.Text(f) for f in faculties],
    )

    warn_email = ft.Text('*Неверное или пустое значение электронной почты', size=10, visible=True)
    warn_name = ft.Text('*Только кириллицей, без спец. символов и цифр', size=10, visible=True)
    warn_password = ft.Text('*Длина пароля не меньше 6 символов и без пробелов', size=10, visible=True)

    name_input = ft.Card(
        height=170,
        width=page.width - (page.width * 0.05),
        content=ft.Container(
            margin=ft.margin.symmetric(10, 15),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.Container(expand=3, alignment=ft.alignment.top_center, content=ft.Text('Как вас зовут?', size=19)),
                    ft.Container(expand=7, alignment=ft.alignment.center, content=username),
                    ft.Container(expand=3, alignment=ft.alignment.top_center, content=warn_name),
                    
                ]
            ),
        )
    )
    role_selection = ft.Card(
        height=170,
        width=page.width - (page.width * 0.05),
        content=ft.Container(
            margin=ft.margin.symmetric(10, 15),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.Container(expand=3, alignment=ft.alignment.top_center, content=ft.Text('Кем вы являетесь?', size=19)),
                    ft.Row(expand=9,
                        spacing=0,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                content=ft.Row(
                                    spacing=0,
                                    controls=[
                                        ft.Text('Я', weight=ft.FontWeight.BOLD),
                                        ft.TextButton(adaptive=False,
                                            content=role,
                                            style = ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10),
                                                padding=5,
                                            ),
                                            on_click=lambda _: page.show_bottom_sheet(
                                                ft.CupertinoBottomSheet(
                                                    picker_roles,
                                                    height=216,
                                                    bgcolor=ft.cupertino_colors.SYSTEM_BACKGROUND,
                                                    padding=ft.padding.only(top=6),
                                                )
                                            )
                                        )
                                    ]
                                )
                            ),
                            ft.Container(
                                content=ft.Row(
                                    spacing=0,
                                    controls=[
                                        ft.Text('из', weight=ft.FontWeight.BOLD),
                                        ft.TextButton(adaptive=False,
                                            content=faculty,
                                            style = ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(radius=10),
                                                padding=5,
                                            ),
                                            on_click=lambda _: page.show_bottom_sheet(
                                                ft.CupertinoBottomSheet(
                                                    picker_faculties,
                                                    height=216,
                                                    bgcolor=ft.cupertino_colors.SYSTEM_BACKGROUND,
                                                    padding=ft.padding.only(top=6),
                                                )
                                            )
                                        )
                                    ]
                                )
                            )
                
                        ]
                    )  
                ]
            )
        )
    )
    email_input = ft.Card(
        height=170,
        width=page.width - (page.width * 0.05),
        content=ft.Container(
            margin=ft.margin.symmetric(10, 15),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.Container(expand=3, alignment=ft.alignment.top_center, content=ft.Text('Укажите почту', size=19)),
                    ft.Container(expand=7, alignment=ft.alignment.center, content=email),
                    ft.Container(expand=3, alignment=ft.alignment.top_center, content=warn_email),
                    
                ]
            ),
        )
    )
    password_input = ft.Card(
        height=170,
        width=page.width - (page.width * 0.05),
        content=ft.Container(
            margin=ft.margin.symmetric(10, 15),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.Container(expand=3, alignment=ft.alignment.top_center, content=ft.Text('Придумайте пароль', size=19)),
                    ft.Container(expand=7, alignment=ft.alignment.center, content=password),
                    ft.Container(expand=3, alignment=ft.alignment.top_center, content=warn_password),
                    
                ]
            ),
        )
    )

    first_cards = ft.Column(
        offset=ft.transform.Offset(0, 0),
        animate_offset=ft.animation.Animation(duration=1000, curve=ft.AnimationCurve.DECELERATE),
        animate_opacity=ft.animation.Animation(duration=1000, curve=ft.AnimationCurve.DECELERATE),
        controls=[name_input, role_selection]
    )
    second_cards = ft.Column(
        offset=ft.transform.Offset(0, 0),
        animate_offset=ft.animation.Animation(duration=1000, curve=ft.AnimationCurve.DECELERATE),
        animate_opacity=ft.animation.Animation(duration=1000, curve=ft.AnimationCurve.DECELERATE),
        controls=[email_input, password_input]
    )
    third_card = ft.Card(
        height=230,
        width=page.width - (page.width * 0.05),
        offset=ft.transform.Offset(0, 0),
        animate_offset=ft.animation.Animation(duration=1000, curve=ft.AnimationCurve.DECELERATE),
        animate_opacity=ft.animation.Animation(duration=1000, curve=ft.AnimationCurve.DECELERATE),
        content=ft.Container(
            margin=ft.margin.symmetric(10, 15),
            content=ft.Column(spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(alignment=ft.alignment.top_center, content=ft.Text('Верификация', size=19)),
                    ft.Container(alignment=ft.alignment.center, content=ft.Text(
                                    'На вашу почту отправлена ссылка для подтверждение аккаунта. \
                                    Пожалуйста, нажмите на ссылку и возвращайтесь', size=15, text_align=ft.TextAlign.CENTER)),
                    ft.Column(
                        spacing=0,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            resend_button,
                            ft.ElevatedButton('Войти', on_click=handle_sign_in)
                        ]
                    )
                ]
            )
        )
    )
    
    register_view = ft.View(
        route='/register',
        fullscreen_dialog=True, scroll='hidden', padding=ft.padding.symmetric(0,10),
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        appbar=ft.AppBar(
            center_title=True,
            title=ft.Text('Создание учетной записи'),
        ),
        controls=[
            ft.Row(
                adaptive=True,
                spacing=0,
                controls=[
                    first_cards, second_cards, third_card
                ]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                controls=[
                    ft.Container(expand=1, margin=ft.margin.symmetric(0,20),content=back_button),
                    ft.Container(expand=1, margin=ft.margin.symmetric(0,20),content=forward_button),
                ]
            )
        ]
    )

    
    return {
        'view': register_view,
        'load': on_load_register_view
    }
