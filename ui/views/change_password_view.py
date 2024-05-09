import flet as ft
import re
from firebase.pyrebase import PyrebaseWrapper

def ChangePasswordView(page: ft.Page, firebase: PyrebaseWrapper):  
    def on_load_change_password_view():
        page.update()

    def on_click_save_password(e: ft.ControlEvent): 
        try:
            if warn_new_password.data :
                firebase.auth.sign_in_with_email_and_password(
                    page.client_storage.get('email'),
                    old_password.value
                )
            elif len(old_password.value) == 0:
                warn_old_password.visible = True
                warn_old_password.value = '*Заполните это поле' 
            elif len(new_password.value) == 0:
                warn_new_password.visible = True
                warn_new_password.value = '*Заполните это поле'

            page.update()

        except Exception as e:
            print(e)


    def on_change_new_password(e: ft.ControlEvent):
        len_password = bool(re.match(r'^.{6,16}$', new_password.value))
        spaces = bool(re.match(r'^\s*$', new_password.value))
        if len_password:
            warn_new_password.spans[0].color = 'error'
        else:
            warn_new_password.spans[0].color = None

        if spaces:
            warn_new_password.spans[1].color = 'error'
        else:
            warn_new_password.spans[1].color = None

        if len_password and spaces:
            warn_new_password.data = True
        else:
            warn_new_password.data = False

    def on_change_old_password(e: ft.ControlEvent):
        warn_old_password.visible = False
        page.update()
    
    info_alert = ft.AlertDialog(
        adaptive=True,
        content_padding=15,
        title=ft.Text('Смена пароля', text_align=ft.TextAlign.CENTER),
        content=ft.Column(scroll='hidden',
            controls=[
                ft.Text('Пароль успешно изменен',text_align=ft.TextAlign.CENTER)]),
        actions=[ft.TextButton('Хорошо!', on_click=lambda _: page.close_dialog())],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    old_password = ft.TextField(
        label='Текущий',  border_color='grey, 0.5',
        bgcolor='secondarycontainer, 0.225', border_radius=8,
        on_change=on_change_old_password, height=40, 
    )
    new_password = ft.TextField(
        label='Новый',  border_color='grey, 0.5',
        bgcolor='secondarycontainer, 0.225', border_radius=8,
        on_change=on_change_new_password, height=40, 
    )


    warn_old_password = ft.Text('', color='error')
    warn_new_password = ft.Text(  
        value='Придумайте пароль от',
        data=False,
        spans=[
            ft.TextSpan('6 знаков', style=ft.TextStyle(color=ft.colors.ERROR)), 
            ft.TextSpan('и'), 
            ft.TextSpan('без пробелов', style=ft.TextStyle(color=ft.colors.ERROR)), 
        ]
    )
    forgot_password_view = ft.View(
        route='/change_pass', fullscreen_dialog=True,
        appbar=ft.AppBar(adaptive=False), adaptive=False,
        vertical_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                [
                    ft.Text('Придумайте новый пароль', size=36, 
                        weight=ft.FontWeight.BOLD
                    ),
                    old_password,
                    new_password
                ]
            ),
            ft.ElevatedButton(
                text='Сохранить', bgcolor=ft.colors.SECONDARY_CONTAINER, 
                on_click=on_click_save_password, color=ft.colors.ON_BACKGROUND,
            )
        ]
        
    )
    
    
    return {
        'view': forgot_password_view,
        'load': on_load_change_password_view
    }