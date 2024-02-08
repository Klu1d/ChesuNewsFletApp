
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
    page.theme = ft.Theme(
            visual_density=ft.ThemeVisualDensity.COMPACT,
            color_scheme_seed=ft.colors.GREEN,
            font_family="Museo",
            color_scheme=ft.ColorScheme(
                primary=ft.colors.GREEN,
                on_primary=ft.colors.GREY_50,
                primary_container=ft.colors.WHITE,
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

    