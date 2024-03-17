import copy
import uuid
import datetime
import flet as ft
import pyrebase
import sys, errno 

from collections import  OrderedDict
from flet_contrib.shimmer import Shimmer

from firebase.flet_pyrebase import Status, PyrebaseWrapper
from ui.controller.announce import AnnounceCard, CreateAnnounceCard

def AnnounceView(page: ft.Page, firebase: PyrebaseWrapper):
    def on_load_announce():
        try:
            if firebase.check_token() == 'Success':
                firebase.stream_user_draft_announcements(build)
        except AttributeError as e:
            empty_list_announces.visible = True
            page.update()

    def build(data):
        if data['data'] != None:
            if data['event'] == 'put':
                if data['path'] == '/':
                    for key, card in data['data'].items():
                        announces[key] = AnnounceCard(
                            id=key, options_visible = False if card.get('status') == Status.PENDING else True,
                            margin=ft.margin.symmetric(10,20),
                            status=card.get('status'),
                            headline=card.get('headline'),
                            text=card.get('text'),
                            datetime=card.get('datetime'),
                            place=card.get('place'),
                            role=card.get('role'),
                            username=card.get('username'),
                            image=card.get('image'),
                            status_label=status_label(card.get('status'), key),
                            title_button=card_button(card.get('status'), key),
                            on_click_change=on_click_edit_card,
                            on_click_delete=on_click_pre_delete,
                            maintain_state=False,
                        )
                else:
                    key = data['path'][1:]
                    announces[key] = AnnounceCard(
                        margin=ft.margin.symmetric(10,20),
                        id=key, options_visible= False if data['data'].get('status') == Status.PENDING else True,
                        headline=data['data']['headline'],
                        text=data['data']['text'],
                        status=data['data'].get('status'),
                        datetime=data['data']['datetime'],
                        place=data['data']['place'],
                        role=data['data']['role'],
                        username=data['data']['username'],
                        image=data['data'].get('image'),
                        status_label=status_label(data['data'].get('status'), key),
                        title_button=card_button(data['data'].get('status'), key),
                        on_click_change=on_click_edit_card,
                        on_click_delete=on_click_pre_delete,
                        maintain_state=True
                    )
                    announces.move_to_end(key, last=False)
            empty_list_announces.visible = False
        else:
            empty_list_announces.visible = True
            announces.clear()
        page.update()

    def shimmer_effect(count=2):
        first = ft.Container(
            data='shimmer_load', 
            bgcolor=ft.colors.SECONDARY_CONTAINER,
            border_radius=15, 
            padding=20,
            height=170,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                    alignment=ft.MainAxisAlignment.START, 
                    spacing=10,
                    controls=[
                        ft.Container(data='shimmer_load', height=12, width=210, border_radius=15,bgcolor=ft.colors.BACKGROUND), 
                        ft.Container(data='shimmer_load', height=12, width=70, border_radius=15, bgcolor=ft.colors.BACKGROUND),
                    ]
                ),
                    ft.Row(spacing=10, controls=[
                        ft.Container(data='shimmer_load', height=45, expand=2, border_radius=10, bgcolor=ft.colors.BACKGROUND),
                        ft.Container(data='shimmer_load', height=45, expand=5, border_radius=10, bgcolor=ft.colors.BACKGROUND),
                    ])
                ]
            )    
        )
        controls = [first for _ in range(count)]
        return Shimmer(
            control=ft.Container(
                padding=20,
                opacity=0.6,
                data='shimmer_load',  
                content=ft.Column(
                    spacing=10,
                    controls=controls
                )
            ),
        )

    def card_button(status, key):
        if status == Status.PENDING:
            return ft.FilledButton(key=key,
                text='Отправлен на проверку',
                data=key,
                icon=ft.icons.EMOJI_FOOD_BEVERAGE, 
                icon_color=ft.colors.ON_TERTIARY,
                style=ft.ButtonStyle(
                    color=ft.colors.ON_TERTIARY,
                    bgcolor=ft.colors.TERTIARY,
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            )
        elif status == Status.APPROVED:
            return ft.FilledButton(key=key,
                text='Опубликовать',
                data=key,
                on_click=on_click_publish,
                style=ft.ButtonStyle(
                    color=ft.colors.GREEN_900,
                    bgcolor=ft.colors.GREEN_ACCENT,
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            )
        elif status == Status.REJECTED:
            return ft.FilledButton(key=key,
                text='Изменить',
                data=key,
                on_click=on_click_edit_card,
                icon=ft.icons.EDIT_SQUARE,
                icon_color=ft.colors.ON_TERTIARY,
                style=ft.ButtonStyle(
                    color=ft.colors.ON_TERTIARY,
                    bgcolor=ft.colors.TERTIARY,
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            )
        else:
            return ft.FilledButton(key=key,
                text='Отправить на проверку',
                data=key,
                on_click=on_click_send_for_check,
                style=ft.ButtonStyle(
                    color=ft.colors.ON_TERTIARY,
                    bgcolor=ft.colors.TERTIARY,
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            )
    
    def status_label(status, key):
        if status == Status.APPROVED:
            return ft.Row(
                spacing=1,
                controls=[
                    ft.Icon(ft.icons.CHECK, color='green'),
                    ft.Text('Одобрено', color='green')
                ]
            )
        elif status == Status.REJECTED:
            return ft.Row(
                spacing=1,
                controls=[
                    ft.Icon(ft.icons.CLOSE, color='red'),
                    ft.Text('Отказано', color='red')
                ]
            )
        else:
            return None
    
    def on_click_publish(e):
        card = announces[e.control.key]
        try:
            firebase.publish_announcement(
                e.control.key, card.headline, 
                card.text, card.place,
                card.datetime, card.role,
                card.username, card.image,
            )
            del announces[e.control.key]
            page.update()
        except pyrebase.pyrebase.HTTPError:
            print('da')
    
    def on_click_after_rejected_edit(e):
        pass
    
    """Create Announcement Card"""
    def on_click_create_form(e):
        
        create_form_dialog.content = card_creator
        page.dialog = create_form_dialog
        card_creator.datetime_button.text = None
        create_form_dialog.open = True
        page.update()
    
    def on_click_create_card(e):
        id = str(uuid.uuid4())[:20]
        firebase.create_announcement(
            id,
            card_creator.headline,
            card_creator.text,
            card_creator.place,
            card_creator.datetime,
            page.client_storage.get('role'),
            page.client_storage.get('username'),
            card_creator.image,
        )
        
        on_click_cancel_card(e)

    def on_click_cancel_card(e):
        card_changing: CreateAnnounceCard = create_form_dialog.content
        card_changing.datetime_button.text = None
        card_changing.create_button.disabled = True
        card_changing.key = None
        page.dialog.open = False
        
        card_changing.update()
        page.update()

    def on_click_save_card(e):
        card_editor = create_form_dialog.content
        firebase.create_announcement(
            e.control.key,
            card_editor.headline,
            card_editor.text,
            card_editor.place,
            card_editor.datetime,
            page.client_storage.get('role'),
            page.client_storage.get('username'),
            card_editor.image,
            status=Status.PENDING if card_editor.status != 'local' else 'local'
            
        )
        if card_editor.status != 'local': 
            firebase.send_announcement(
                e.control.key,
                card_editor.headline,
                card_editor.text,
                card_editor.place,
                card_editor.datetime,
                page.client_storage.get('role'),
                page.client_storage.get('username'),
                card_editor.image,
                status=Status.PENDING,
            )
        page.dialog.open = False
        page.update()
    
    """Options AnnounceCard"""
    def on_click_edit_card(e):
        card: AnnounceCard = announces[e.control.data]
        text_create_button = 'На Проверку' if card.status != 'local' else 'Сохранить'
        card_editor = CreateAnnounceCard(
            cancel_button = ft.TextButton('Отменить', on_click=on_click_cancel_card),
            create_button = ft.TextButton(text_create_button, key=card.id, disabled=True, on_click=on_click_save_card)
        )
        card_editor.status = card.status
        card_editor.datetime_button.text = None
        card_editor.headline = card.headline
        card_editor.text = card.text
        card_editor.role = card.role
        card_editor.place = card.place
        card_editor.image = card.image
        card_editor.status = card.status

        create_form_dialog.content = card_editor
        page.dialog = create_form_dialog
        page.dialog.open = True
        page.update()

    def on_click_pre_delete(e):
        warning_pre_delete.actions[1].data = e.control.data
        page.dialog = warning_pre_delete
        warning_pre_delete.open = True
        page.update()
    
    def on_click_delete_card(e):
        try:
            del announces[e.control.data]
            page.dialog.open = False
            page.update()
            firebase.delete_announcement(e.control.data)
        except pyrebase.pyrebase.HTTPError as e:
            print(':::', e)
        
        
        
    """SEND FIREBASE"""
    def on_click_send_for_check(e):
        card: AnnounceCard = announces[e.control.key]
        announces[e.control.key] = AnnounceCard(
            id=e.control.key,
            status=card.status,
            margin=ft.margin.symmetric(10,20),
            headline=card.headline,
            text=card.text,
            datetime=card.datetime,
            place=card.place,
            role=page.client_storage.get('role'),
            username=page.client_storage.get('username'),
            image=card.image,
            options_visible=False,
            maintain_state=card.maintain_state,
            title_button=ft.FilledButton(
                text='Отправлен на проверку',
                icon=ft.icons.EMOJI_FOOD_BEVERAGE, 
                icon_color=ft.colors.ON_TERTIARY,
                style=ft.ButtonStyle(
                    color=ft.colors.ON_TERTIARY,
                    bgcolor=ft.colors.TERTIARY,
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
            on_click_change=on_click_edit_card,
            on_click_delete=on_click_pre_delete,
        )
        firebase.send_announcement(
            e.control.key,
            card.headline,
            card.text,
            card.place,
            card.datetime,
            page.client_storage.get('role'),
            page.client_storage.get('username'),
            card.image,
        )
        page.update()

    def on_click_close_dlg(e):
        page.dialog.open = False
        page.update()
        
    announces = OrderedDict()
    cancel_button = ft.TextButton('Отменить', on_click=on_click_cancel_card)
    create_button = ft.TextButton('Создать', disabled=True, on_click=on_click_create_card)
    card_creator = CreateAnnounceCard(create_button, cancel_button)

    create_form_button = ft.IconButton(icon='post_add', icon_color='onbackground', 
        on_click=on_click_create_form,
        style=ft.ButtonStyle(
            color='onbackground', 
            bgcolor=ft.colors.INVERSE_PRIMARY, 
            shape=ft.RoundedRectangleBorder(radius=5)
        )
    )
    create_form_dialog = ft.AlertDialog(
        content_padding=0,
        actions_padding=0,
        title_padding=0,
        inset_padding=ft.padding.only(20,35,20,5),
        content=card_creator,
        on_dismiss=on_click_cancel_card,
    )
    warning_pre_delete = ft.AlertDialog(
        title=ft.Text('Удалить анонс?'),
        content=ft.Text('Вы уверены что хотите удалить эту карточку?'),
        actions=[ft.TextButton('Нет', on_click=on_click_close_dlg), ft.TextButton('Да', on_click=on_click_delete_card, style=ft.ButtonStyle(color='red')),],
        actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    
    send_for_check_table = ft.FilledButton(
        text='Отправлен на проверку',
        icon=ft.icons.EMOJI_FOOD_BEVERAGE, 
        icon_color=ft.colors.ON_TERTIARY,
        style=ft.ButtonStyle(
            color=ft.colors.ON_TERTIARY,
            bgcolor=ft.colors.TERTIARY,
            shape=ft.RoundedRectangleBorder(radius=10)
        )
    )
    
    empty_list_announces = ft.Container(
        data='empty',
        visible=True,
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
    shimmer = ft.Container(shimmer_effect())

    build_announcement = ft.Column(controls=announces.values(), spacing=0, scroll='hidden')
    announce_view = ft.View(
        route='/announce',
        padding=0,
        spacing=0,
        controls=[
            ft.AppBar(
                center_title=True,
                title=ft.Text('Объявления', size=17),
                actions=[ft.Container(create_form_button, margin=ft.margin.symmetric(0, 15))]
                    
            ),
            ft.Stack(
                expand=True,
                controls=[
                    build_announcement,
                    empty_list_announces
                ]
            )
        ]
    )
    
    
    return {
        'view':announce_view,
        'load':on_load_announce,
    }

