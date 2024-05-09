import json
import flet as ft

from ui.customs.top_bar import TopPanel
from ui.customs.news_lists import NewsLists 
from ui.customs.announcements_lists import AnnouncementsLists
from ui.customs.categories import Categories
from firebase.pyrebase import PyrebaseWrapper


def NewsView(page: ft.Page, firebase: PyrebaseWrapper):
    def on_load_news_view():
        page.dialog = status_info
        if firebase.check_token() == 'Success':
            # Если роли нет, значит это анонимный пользователь. Выводится окно с информцией об ограничениях.
            anonymous = not(bool(page.client_storage.get('role')))
            page.dialog.open = anonymous
            exit.visible = anonymous
            page.update()

            # Если пользователь не анонимный, отображается активная кнопка
            news_view.floating_action_button.visible = not(anonymous)
            if bool(page.client_storage.get('role')) and '-Активист' in page.client_storage.get('role'):
                pending_events.visible = True
                firebase.stream_moderation_decisions(notification_counts)
                firebase.streams['moderations'].close
            else:
                pending_events.visible = False
            firebase.stream_public_announcements(build_announcements)
            firebase.streams['chesu'].close
            
            build_tabs()
        page.update()

    def build_announcements(stream_data):
        announce_manager.stream_handler(stream_data)
        page.update()

    def notification_counts(stream_data):
        path = stream_data['path']
        moder_events = 0

        if stream_data['event'] == 'patch' and stream_data['data']:
            for msg in stream_data['data'].values():
                if msg == firebase.uuid:
                    moder_events += 1
            if len(path) > 1:
                count = int(pending_events.text)
                count += 1 - moder_events
                pending_events.text = count
                pending_events.label_visible = bool(count)
            else:
                print('как ты тут оказался?', stream_data)
        elif stream_data['event'] == 'put' and stream_data['data']:
            for msg in stream_data['data'].values():
                if msg.get('author_id') == firebase.uuid:
                    moder_events += 1
            if len(path) > 1:
                count = int(pending_events.text)
                count -= 1 - moder_events
                pending_events.text = count
                pending_events.label_visible = bool(count)
            else:          
                print(moder_events)           
                count = len(stream_data.get('data')  or []) - moder_events
                pending_events.text = count
                pending_events.label_visible = bool(count)
                
        page.update()

    def build_tabs():
        for short_name in categories_info:
            if categories_info[short_name]['visible']:
                news_tabs.tabs.append(
                    ft.Tab(
                        tab_content=ft.Text(
                            size=25, 
                            value=short_name, 
                            weight=ft.FontWeight.W_900, 
                            font_family='Headline'
                        ),
                        content=ft.Container(
                            content=ft.ListView(
                                controls=[],
                                spacing=10,
                            )
                        )
                    )
                )
                button_categories.controls.append(
                    ft.Container(
                        height=50, key=len(news_tabs.tabs)-1,
                        alignment=ft.alignment.center_left, 
                        padding=ft.padding.only(left=15), 
                        on_click=on_click_category,
                        content=ft.Text(
                            value=categories_info[short_name]['full_name'], 
                            weight=ft.FontWeight.BOLD, 
                            color=ft.colors.SECONDARY, 
                            size=18
                        )
                    )
                )
        page.update()

    def news_loader(index):
        if index not in [0, 1]:
            if news_tabs.tabs[index].content.data != 'news':
                current_tab: ft.Tab = news_tabs.tabs[index]
                full_name = categories_info[current_tab.tab_content.value]['full_name']
                current_tab.content = NewsLists(page, firebase, full_name)
                page.update()

    def on_click_category(e):
        news_tabs.selected_index = e.control.key
        page.bottom_sheet.open = False
        page.update()
        news_loader(e.control.key)

    def on_click_logout(e):
        page.close_dialog()
        page.client_storage.clear()
        del page.views[1:]
        page.go('')
        
        firebase.kill_all_streams()
        firebase.sign_out()
        
        
    with open('assets/json/categories_info.json', 'r', encoding='utf-8') as json_file:
        categories_info = json.load(json_file)['categories_info']
    
    exit = ft.IconButton(ft.icons.EXIT_TO_APP_ROUNDED, icon_color='error', on_click=on_click_logout, visible=False)

    status_info = ft.AlertDialog(
        adaptive=True, content_padding=15,
        title=ft.Text('Важная информация о вашем статусе', text_align=ft.TextAlign.CENTER),
        content=ft.Column(scroll='hidden',
            controls=[
                ft.Text(
                    'Хотим привлечь ваше внимание на то, что при входе в приложение анонимно ' +
                    'вы можете получать свежие новости и актуальные события из университета.\n\n'+
                    'Однако, если у вас есть аккаунт, вы получаете возможность не только сохранять ' +
                    'интересные новости в закладки, но и предлагать собственные мероприятия для проведения.',
                 
                    text_align=ft.TextAlign.CENTER)]),
        actions=[ft.TextButton('Хорошо!', on_click=lambda _: page.close_dialog())],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    announce_manager = AnnouncementsLists(page, firebase)
    news_tabs = ft.Tabs(
        expand=1,
        selected_index=0,
        indicator_padding=10,
        animation_duration=600,
        indicator_border_radius=15,
        tab_alignment=ft.TabAlignment.START_OFFSET,
        indicator_color=ft.colors.ON_SURFACE_VARIANT,
        label_color=ft.colors.ON_SURFACE_VARIANT,
        unselected_label_color=ft.colors.SURFACE_VARIANT,
        divider_color=ft.colors.BACKGROUND,
        overlay_color=ft.colors.BACKGROUND,
        on_change=lambda e: news_loader(e.control.selected_index),
        tabs=[
            ft.Tab(
                tab_content=ft.Text(
                    size=25, 
                    value='Новости', 
                    weight=ft.FontWeight.W_900, 
                    font_family='Headline'
                ),
                content=NewsLists(page, firebase, 'Новости')
            ),
            ft.Tab(
                tab_content=ft.Text(
                    size=25, 
                    value='Анонсы', 
                    weight=ft.FontWeight.W_900, 
                    font_family='Headline'
                ),
                content=announce_manager
            ),
        ]
    )
    button_categories = Categories()
    button_categories.controls = [
        ft.Container(
            height=50, key=0,
            alignment=ft.alignment.center_left, 
            padding=ft.padding.only(left=15), 
            on_click=on_click_category,
            content=ft.Text(
                value='Новости', 
                weight=ft.FontWeight.BOLD, 
                color=ft.colors.SECONDARY, 
                size=18
            )
        ),
        ft.Container(
            height=50, key=1,
            alignment=ft.alignment.center_left, 
            padding=ft.padding.only(left=15), 
            on_click=on_click_category,
            content=ft.Text(
                value='Анонсы', 
                weight=ft.FontWeight.BOLD, 
                color=ft.colors.SECONDARY, 
                size=18
            )
        )
    ]
    

    button_announces = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        on_click=lambda _: page.go('/announce'),
        content=ft.Column(
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.icons.ANNOUNCEMENT_ROUNDED,color=ft.colors.INVERSE_SURFACE),
                ft.Text('События', color=ft.colors.INVERSE_SURFACE, size=9, weight=ft.FontWeight.BOLD)
            ]
        ),
    )
    
    button_bookmarks=ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        on_click=lambda _: page.go('/bookmarks'),
        content=ft.Column(
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.icons.BOOKMARKS_ROUNDED,color=ft.colors.INVERSE_SURFACE),
                ft.Text('Закладки', color=ft.colors.INVERSE_SURFACE, size=9, weight=ft.FontWeight.BOLD)
            ]
        ),
    )

    pending_events = ft.Badge(
        label_visible=False, visible=False,
        alignment=ft.alignment.Alignment(0.6, -0.6),
        content=ft.IconButton(icon=ft.icons.SIGNPOST_ROUNDED, icon_color='onbackground', 
            on_click=lambda _: page.go('/review'), adaptive=False,
            style=ft.ButtonStyle(
                color='onbackground', 
                shape=ft.RoundedRectangleBorder(radius=5)
            )
        )
    )

    news_view =  ft.View(
        route='/news',
        padding=0,
        fullscreen_dialog=True,
        floating_action_button=ft.FloatingActionButton(
            height=50, width=page.width-page.width/2.4, visible=False,
            bgcolor=ft.colors.ON_INVERSE_SURFACE, mini=True,
            content=ft.Row(expand=True,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[button_announces, button_bookmarks]
            )
        ),
        floating_action_button_location = ft.FloatingActionButtonLocation.MINI_CENTER_FLOAT,
        appbar=TopPanel(pending_events, exit),
        controls=[
            ft.Stack(
                expand=True,
                controls=[
                    news_tabs,
                    #bottom_bar,
                    button_categories
                ]
            )
        ]
    )
    return {
        'view': news_view,
        'load': on_load_news_view,
    }

