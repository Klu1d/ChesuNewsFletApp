import flet as ft
import re

def ForgotPasswordView(page: ft.Page, firebase):
    def on_load_forgot_password():
        page.update() 
           
    def on_click_send_email(e: ft.ControlEvent):
        valid = bool(re.match(r'^\w+[\w\.\+\-]*@\w+\.[a-z]{2,3}$', email_input.value))
        if valid:
            page.dialog = info_alert
            page.dialog.open = True
            firebase.auth.send_password_reset_email(email_input.value)
        elif len(email_input.value) == 0:
            warn_text.visible = True
            warn_text.value = '*Заполните это поле'
        else:
            warn_text.visible = True
            warn_text.value = '*Адрес написан с ошибкой'
        page.update()

    def on_change_email_input(e: ft.ControlEvent):
        warn_text.visible = False
        warn_text.update()

    info_alert = ft.AlertDialog(
        adaptive=True,
        content_padding=15,
        title=ft.Text('Сброс пароля', text_align=ft.TextAlign.CENTER),
        content=ft.Column(scroll='hidden',
            controls=[
                ft.Text('Ссылка для сброса пароля была отправлена на вашу электронную почту',text_align=ft.TextAlign.CENTER)]),
        actions=[ft.TextButton('Хорошо!', on_click=lambda _: page.close_dialog())],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    email_input = ft.TextField(
        label='Почта',  border_color='grey, 0.5',
        bgcolor='secondarycontainer, 0.225', border_radius=8,
        on_change=on_change_email_input, height=40, 
    )
    warn_text = ft.Text('', color='error')
    forgot_password_view = ft.View(
        route='/forgot', fullscreen_dialog=True,
        appbar=ft.AppBar(adaptive=False), adaptive=True,
        vertical_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Column(
                [
                    ft.Text('Восстановления пароля', size=36, 
                        weight=ft.FontWeight.BOLD
                    ),
                    email_input,
                    warn_text
                ]
            ),
            ft.ElevatedButton(
                text='Отправить', bgcolor=ft.colors.SECONDARY_CONTAINER, 
                on_click=on_click_send_email, color=ft.colors.ON_BACKGROUND,
            )
        ]
        
    )
    
    
    return {
        'view': forgot_password_view,
        'load': on_load_forgot_password
    }