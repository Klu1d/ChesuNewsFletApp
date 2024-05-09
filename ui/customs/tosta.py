import flet as ft
from aploa import AnnouncementsLists
from ... import PyrebaseWrapper

def main(page: ft.Page):
    def stream():
        firebase.stream_public_announcements(options.stream_handler)

    firebase = PyrebaseWrapper(page)
    options = AnnouncementsLists(firebase)
    page.add(options)

ft.app(target=main)