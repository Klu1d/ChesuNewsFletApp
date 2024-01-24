import flet as ft

def BookmarksView(page, myPyrebase=None):
    title = 'Закладки'
    myPage = ft.Column(
        controls=[
            ft.Text('Привет мир!'),
            ft.Text(page.views),
            ft.TextButton('Пока мир!', on_click=lambda _: page.go('/news'))
        ]
    )
    return {
        'view':myPage,
        'title': title
        }