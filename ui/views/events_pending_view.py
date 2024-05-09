import copy
import uuid
import datetime
import flet as ft
import pyrebase
import sys, errno, asyncio

from collections import  OrderedDict
from flet_contrib.shimmer import Shimmer

from firebase.pyrebase import Status, PyrebaseWrapper
from ui.customs.cards import AnnounceCard, CreateAnnounceCard
from ui.customs.announcements_lists import AnnouncementsLists

def EventsPendingView(page: ft.Page, firebase: PyrebaseWrapper):
    def on_load_announce():
        try:
            if firebase.check_token() == 'Success':
                firebase.stream_moderation_decisions(build)
        except AttributeError as e:
            empty_list_icon.visible = True
        page.update()

    def build(stream_data):
        announce_manager.stream_handler(stream_data)
        page.update()

    announce_manager = AnnouncementsLists(page, firebase, False)
    empty_list_icon = ft.Container(
        data='empty',
        visible=False,
        height=page.height - 80,
        alignment=ft.alignment.center,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
            controls=[
                ft.CircleAvatar(
                    radius=45,
                    bgcolor=ft.colors.with_opacity(0.3, ft.colors.GREY), 
                    content=ft.Icon(ft.icons.SIGN_LANGUAGE, size=40)
                ),
                ft.Text(value='Мероприятий не запланировано', size=17)
            ]
        )
    )

    
    events_pending_view = ft.View(
        route='/review',
        padding=0,
        appbar=ft.AppBar(
            center_title=True, adaptive=True,
            title=ft.Text('Ожидающие события'), 
        ),
        controls=[
            announce_manager
        ]
    )
    
    
    return {
        'view':events_pending_view,
        'load':on_load_announce,
    }

