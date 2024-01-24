
import flet as ft

from ui.views.FletRouter import Router
from firebase.flet_pyrebase import PyrebaseWrapper
from firebase.scrapper import scrap_news

def checkout_client_storage(page, db):
    list_tabs = list(db.get_tabs().keys())
    if page.client_storage.get("abbreviature") == None:
        for i in range(len(list_tabs)):
            if list_tabs[i] == 'Новости':
                list_tabs[i] = list_tabs[0]
                list_tabs[0] = 'Новости'
            elif list_tabs[i] == 'Анонсы':
                list_tabs[i] = list_tabs[1]
                list_tabs[1] = 'Анонсы'
            elif list_tabs[i] == 'Наука':
                list_tabs[i] = list_tabs[2]
                list_tabs[2] = 'Наука'
            else:
                list_tabs.append(list_tabs[i])
        page.client_storage.set("abbreviature", list_tabs)

def main(page: ft.Page):
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
    page.window_width, page.window_height = 400, 700
    page.theme_mode = "light"
    page.padding = 0
    
    myPyrebase = PyrebaseWrapper(page)
    #scrap_news(page, myPyrebase)
    myRouter = Router(page, myPyrebase) 
    
    page.client_storage.clear()
    checkout_client_storage(page, myPyrebase)
    
    page.on_route_change = myRouter.route_change
    page.on_view_pop = myRouter.view_pop
    page.add(
        ft.SafeArea(
            expand=True,
            content=myRouter.body
        )
    )
    page.go('/')
    
if __name__ == "__main__":
    ft.app(target=main, assets_dir='assets')

    