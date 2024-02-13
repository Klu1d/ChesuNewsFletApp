import flet as ft

def AccountView(page, firebase):
    def on_load_account():
        pass
    
    account_view = ft.View(
        route='/account',
        scroll='hidden',
        controls=[
            ft.AppBar(
                center_title=True,
                title=ft.Text('Личный кабинет', size=16), 
            ),
        ] 
    )
    return {
        'view':account_view,
        'load':on_load_account,
    }