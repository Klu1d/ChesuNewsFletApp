import flet as ft

from ui.views.news_view import NewsView
from ui.views.index_view import IndexView
from ui.views.account_view import AccountView
from ui.views.register_view import RegisterView
from ui.views.announce_view import AnnounceView
from ui.views.bookmarks_view import BookmarksView
from ui.views.verification_view import VerificationView

class Router:
    def __init__(self, page, firebase):
        self.page = page
        self.firebase = firebase
        self.routes = {
            '/': IndexView(page, firebase),
            '/register': RegisterView(page, firebase),
            '/verification': VerificationView(page, firebase),
            '/news': NewsView(page, firebase),
            '/bookmarks': BookmarksView(page, firebase),
            '/account': AccountView(page, firebase),
            '/announce': AnnounceView(page, firebase)
            
        }
        self.body = ft.Container(content=self.routes['/']['view'])
        self.additional_views =  ['/bookmarks', '/account', '/announce']
    
    def route_change(self, route: ft.RouteChangeEvent):
        self.preloader(True)
        if route is not None:
            if route.route == '/news':
                #self.preloader(True)
                self.on_load_client_storage(self.firebase)
            elif route.route == '':
                print('Да дошел')
                self.routes['/news'].get('load_tab')(self.page.client_storage.get('current_index_tab'))
                self.page.update()
                
            if route.route in self.additional_views:
                self.page.views.append(self.routes[route.route].get('view'))
                self.page.update()
                self.routes[route.route].get('load')()
            elif route.route in self.routes:
                self.body.content = self.routes[route.route].get('view') 
                if self.routes[route.route].get('load'):
                    self.routes[route.route].get('load')()

                    
        self.page.update()
        self.preloader(False)
       
        
    def view_pop(self, view: ft.ViewPopEvent):
        view.page.views.pop()
        top_view = view.page.views[-1]
        view.page.go(top_view.route)
        
    def on_load_client_storage(self, firebase):
        self.page.client_storage.set('theme', 'light')
        self.page.client_storage.set('firstname', firebase.get_username()[0])
        self.page.client_storage.set('lastname', firebase.get_username()[1])
        self.page.client_storage.set('username', firebase.get_username()[1] + ' ' + firebase.get_username()[0])
        self.page.client_storage.set('role', firebase.get_username()[2])
        self.page.client_storage.set('bookmarks', firebase.get_bookmarks())
        self.page.client_storage.set('tabs', {'Новости':'Новости', 'Анонсы':'Анонсы'} | firebase.get_users_tabs())
        
    def preloader(self, activate: bool):
        if activate:
            self.page.overlay.append(ft.Container(bgcolor='background, 0.6', expand=True, disabled=True,alignment=ft.alignment.center, content=ft.ProgressRing()))
            self.page.update()
        else:
            self.page.overlay.clear()
            self.page.update()