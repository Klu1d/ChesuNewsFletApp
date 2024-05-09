import uuid
import flet as ft

from firebase.pyrebase import PyrebaseWrapper
from ui.customs.cards import CreateAnnounceCard
from ui.customs.announcements_lists import AnnouncementsLists


def AnnounceView(page: ft.Page, firebase: PyrebaseWrapper):
    def on_load_announce():
        try:
            if firebase.check_token() == 'Success':
                firebase.stream_user_account(build)
                announce_view.floating_action_button.visible = True
        except AttributeError as e:
            empty_list_icon.visible = True
        page.update()
    
    def build(stream_data):
        path = stream_data['path']
        if stream_data['event'] == 'put':
            if len(path) > 1:
                put = {'path':path.split('announcements')[1], 'data': None, 'event': 'put', 'stream_id': 'users'}
                announce_manager.stream_handler(put)
            else:
                put  = {'path': '/', 'data': stream_data['data'].get('announcements'), 'event': 'put', 'stream_id': 'users'}
                announce_manager.stream_handler(put)
        elif stream_data['event'] == 'patch':
            if len(path) > 1:
                patch = {'path': path.split('announcements')[1], 'data': stream_data['data'], 'event': 'patch', 'stream_id': 'users'}
                announce_manager.stream_handler(patch)
            else:
                announce_id = stream_data['data']['announce_id']
                patch = {'path': '/' + announce_id, 'data': stream_data['data'], 'event': 'patch', 'stream_id': 'users'}
                announce_manager.stream_handler(patch)
        page.update()

    def on_click_create_announce_form(e):
        page.bottom_sheet = CreateAnnounceCard(page, firebase)
        page.bottom_sheet.data = 'Создать'
        page.bottom_sheet.author = page.client_storage.get('username')
        page.bottom_sheet.role = page.client_storage.get('role')
        page.bottom_sheet.announce_id = str(uuid.uuid4())[:20]
        page.bottom_sheet.on_click_create = page.bottom_sheet.on_click_create_announce_card
        page.bottom_sheet.open = True
        page.update()

    announce_manager = AnnouncementsLists(page, firebase)

   
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

    announce_view = ft.View(
        route='/announce',
        padding=0, spacing=0,
        floating_action_button=ft.FloatingActionButton(
            height=50, width=100,
            visible=False, mini=True,
            on_click=on_click_create_announce_form,
            bgcolor=ft.colors.ON_INVERSE_SURFACE,
            content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=0,
                controls=[
                    ft.Icon(ft.icons.POST_ADD, color=ft.colors.INVERSE_SURFACE),
                    ft.Text('Создать', color=ft.colors.INVERSE_SURFACE, weight=ft.FontWeight.BOLD)
                ]
            ),
        ),
        floating_action_button_location = ft.FloatingActionButtonLocation.MINI_CENTER_FLOAT,
        appbar=ft.AppBar(
            center_title=True, adaptive=True,
            title=ft.Text('Объявления'),
                
        ),
        controls=[
            announce_manager,
        ]
    )
    
    
    return {
        'view':announce_view,
        'load':on_load_announce,
    }

