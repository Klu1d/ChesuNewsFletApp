
import flet as ft
from ui.views.FletRouter import Router
from ui.widgets.custom_shimmer import CustomShimmer
from firebase.flet_pyrebase import PyrebaseWrapper
from firebase.scrapper import scrap_news

def main(page: ft.Page):
    page.window_width, page.window_height = 475, 1150
    page.window_left = 10
    page.window_top = 120
    page.padding = 0
    page.update()
    page.fonts = {
        "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
        "Aleo Bold Italic": "https://raw.githubusercontent.com/google/fonts/master/ofl/aleo/Aleo-BoldItalic.ttf",
        "PTSerif": "./assets/font/PTSerif-Bold.ttf",
        "Oswald":"./assets/font/Oswald.ttf",
        "Spaceland":"./assets/font/Spaceland.ttf",
    }
    page.theme = ft.Theme(
        visual_density=ft.ThemeVisualDensity.COMPACT,
        color_scheme_seed=ft.colors.TEAL_800,  # Темно-бирюзовый как цветовой акцент
        font_family="PTSerif",  # Изменяем шрифт на Montserrat
        color_scheme=ft.ColorScheme(
            primary=ft.colors.TEAL_800,  # Основной цвет - темно-бирюзовый
            on_primary=ft.colors.GREY_50,  # Светлый серый для текста на темно-бирюзовом фоне
            primary_container=ft.colors.GREY_200,  # Светло-серый для контейнеров
        ),
    )
    page.theme.page_transitions.ios = ft.PageTransitionTheme.CUPERTINO
    page.theme.page_transitions.android = ft.PageTransitionTheme.OPEN_UPWARDS
    page.theme.page_transitions.macos = ft.PageTransitionTheme.FADE_UPWARDS
    page.theme.page_transitions.linux = ft.PageTransitionTheme.ZOOM
    page.theme.page_transitions.windows = ft.PageTransitionTheme.NONE
   
    firebase = PyrebaseWrapper(page)
    #scrap_news(page, firebase)
    router = Router(page, firebase) 

    page.on_route_change = router.route_change
    page.on_view_pop = router.view_pop
    page.add(
        ft.SafeArea(
            expand=True,
            content=router.body
        )
    )
    page.go('/')
if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets')

    