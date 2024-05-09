import flet as ft
import pyrebase

from ui.views.news_view import NewsView
from ui.views.index_view import IndexView
from ui.views.person_view import PersonView
from ui.views.profile_view import ProfileView
from ui.views.settings_view import SettingsView
from ui.views.register_view import RegisterView
from ui.views.announce_view import AnnounceView
from ui.views.bookmarks_view import BookmarksView
from ui.views.forgot_password_view import ForgotPasswordView
from ui.views.events_pending_view import EventsPendingView
from ui.views.change_password_view import ChangePasswordView

from firebase.pyrebase import PyrebaseWrapper

class Controller:
    def __init__(self, page: ft.Page, firebase: PyrebaseWrapper):
        self.page = page
        self.firebase = firebase
        
        self.routes = {
            #'/': IndexView(page, firebase),
            '/register': RegisterView(page, firebase),
            '/forgot': ForgotPasswordView(page, firebase),
            '/change_pass': ChangePasswordView(page, firebase),

            '/news': NewsView(page, firebase),
            '/announce': AnnounceView(page, firebase),
            '/bookmarks': BookmarksView(page, firebase),

            '/review': EventsPendingView(page, firebase),
            
            '/profile': ProfileView(page, firebase),
            '/person': PersonView(page, firebase),
            '/settings': SettingsView(page, firebase),
            
        }
       
    def route_change(self, route: ft.RouteChangeEvent):
        route = route.route
        view_exists = any(view.route == route for view in self.page.views)
        
        if not view_exists and route != '':
            new_view = self.routes[route].get('view')
            self.page.views.append(new_view)
            self.routes[route].get('load')()
       
    def view_pop(self, view: ft.ViewPopEvent):
        self.page.views.pop()
        top_view = self.page.views[-1]
        self.page.go(top_view.route)
        
    def user_info_cache(self, firebase):
        account_info = firebase.account_info()
        for key, data in account_info.items():
            self.page.client_storage.set(key, data)
        
    def preloader(self, activate: bool):
        if activate:
            self.page.dialog = ft.Container(bgcolor='background, 0.6', expand=True, disabled=True,alignment=ft.alignment.center, content=ft.ProgressRing())
            self.page.update()
        else:
            self.page.dialog = None
            self.page.update()