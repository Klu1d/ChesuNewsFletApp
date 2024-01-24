import flet as ft


from ui.views.index_view import IndexView
from ui.views.news_view import NewsView
from ui.views.register_view import RegisterView
from ui.views.bookmarks_view import BookmarksView
from ui.views.verification_view import VerificationView

class Router:
    def __init__(self, page, myPyrebase):
        self.page = page
        self.routes = {
            '/': IndexView(page, myPyrebase),
            '/register': RegisterView(page, myPyrebase),
            '/bookmarks': BookmarksView(page, myPyrebase),
            '/news': NewsView(page, myPyrebase),
            '/verification': VerificationView(page, myPyrebase)
        }
        self.page.views[0].route = '/'
        self.body = ft.Container(content=self.routes['/']['view'])
        

    def route_change(self, route: ft.RouteChangeEvent):
        if route.route == '/bookmarks':
            self.page.views.append(
                ft.View(
                    route.route,
                    [
                        ft.AppBar(title=ft.Text('Bookmarks'), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.TextButton('lala', on_click=lambda e:e.page.go('/news')),
                    ],
                )
            )
        else:
            #чтобы контент в модуле news_view каждый раз не
            #обновлялся, когда к нему перехожу из bookmarks_view, 
            #я сохраняю прошедший route и сравниваю с нынешним
            self.page.views[0].route = route.route 
            prev_body_content = self.body.content.data 
            self.body.content = self.routes[route.route].get('view') 
            if self.routes[route.route].get('load') and prev_body_content != 'news':
                self.routes[route.route].get('load')()
        self.page.update()

    def view_pop(self, view: ft.ViewPopEvent):
        view.page.views.pop()
        top_view = view.page.views[-1]
        view.page.go(top_view.route)
        view.page.update()
   
    