import time
import flet as ft

from ui.controller.top_bar import TopBar
from ui.controller.announce import AnnounceCard
from ui.controller.tab_display import TabDisplay
from ui.widgets.custom_shimmer import CustomShimmer
from firebase.flet_pyrebase import PyrebaseWrapper


def NewsView(page: ft.Page, firebase: PyrebaseWrapper):
    def on_load_news_view():
        try:
            if firebase.check_token() == 'Success':
                firebase.stream_moderation_decisions()
                news_view.controls[1] = page_shimmer
                build()
        except AttributeError:
            print("Значения в firebase пусты")
            
    def announcements(message):
        announce_display: ft.Tab = all_tabs[1]
        if message['data'] != None:
            if message['event'] == 'put':
                if message['path'] == '/':
                    announce_display.content = ft.ListView(expand=True, padding=ft.padding.only(bottom=65), spacing=10)
                    for key in message['data'].keys():
                        card_content = message['data'][key]
                        card = AnnounceCard(
                            id=key, 
                            status='public',
                            margin=ft.margin.symmetric(vertical=5, horizontal=15),
                            options_visible=False,
                            maintain_state=True,
                            headline=card_content.get('headline'),
                            text=card_content.get('text'),
                            place=card_content.get('place'),
                            role=card_content.get('role'),
                            username=card_content.get('username'),
                            datetime=card_content.get('datetime'),
                            image=card_content.get('image'),
                            leading_button=ft.Icon(ft.icons.GROUP),
                            trailing_button=ft.OutlinedButton('Записаться', adaptive=False, 
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=14))),
                        )
                        announce_display.content.controls.append(card)
        else:
            announce_display.content = ft.Container(
                visible=True,
                alignment=ft.alignment.center,
                content=ft.Column(
                    scroll=None,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                    controls=[
                        ft.CircleAvatar(
                            radius=47.5,
                            bgcolor=ft.colors.with_opacity(0.3, ft.colors.GREY), 
                            content=ft.Icon(ft.icons.SPEAKER_NOTES_OFF_OUTLINED, size=45)
                        ),
                        ft.Text(value='В разделе пока тишина.', size=18)
                    ]
                )
            )
            
        page.update()

    def on_load_tab_content(index):
        current_tab = all_tabs[index]
        full_name = page.client_storage.get('tabs')[current_tab.tab_content.value] #полное имя текущей, выбранной аббревиатуры
        print(current_tab.tab_content.value)
        if current_tab.content.data == 'shimmer' and current_tab.tab_content.value != 'Анонсы':
            current_tab.content.data = 'content'
            current_tab.content=TabDisplay(page, full_name, firebase)

        if current_tab.tab_content.value == 'Анонсы':
            page.floating_action_button.visible = True
            # firebase.stream_public_announcements(announcements)
            # firebase.streams['public'].close
        else:
            page.floating_action_button.visible = False

            
        page.client_storage.set('current_index_tab', index)
        page.overlay.clear()
        page.update()

    def handle_logout(*e):
        clean_tabs()
        firebase.kill_all_streams()
        firebase.sign_out()
        page.controls[0].content.content.controls[1].controls[0].selected_index = 0
        page.floating_action_button.visible = False
        page.go('/')
    
    def on_click_category(e):
        categories.open=False
        categories.show_drag_handle=False
        page.update()
        
        categories.content.content.controls[page.client_storage.get('current_index_tab')].bgcolor=None
        categories.content.content.controls[e.control.key].bgcolor=ft.colors.BLACK12
        page.controls[0].content.content.controls[1].controls[0].selected_index = e.control.key
        page.update()
        
        on_load_tab_content(e.control.key)
    
    def on_click_categories(e):
        tabs = page.client_storage.get('tabs')
        categories.content.content.controls = []
        for i, category in enumerate(all_tabs):
            categories.content.content.controls.append(
                ft.Container(
                    key=i,
                    on_click=on_click_category,
                    alignment=ft.alignment.center_left, 
                    padding=ft.padding.only(left=15), 
                    bgcolor=None,
                    height=50, 
                    content=ft.Text(
                        value=tabs[category.tab_content.value], 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.colors.SECONDARY, 
                        size=18
                    )
                ),
            )
        page.overlay.clear()
        page.overlay.append(categories)
        categories.content.content.controls[page.client_storage.get('current_index_tab')].bgcolor=ft.colors.BLACK12
        categories.show_drag_handle=True
        categories.open = True
        page.update()
        
    def on_dismiss(e):
        categories.show_drag_handle=False
        categories.open = False
        page.overlay.clear()
        page.update()
        
    def build():
        all_tabs.clear()
        shimmer = CustomShimmer(height=page.window_height, first_big=True, tabs=False)
        for abbreviature in page.client_storage.get('tabs').keys():
            all_tabs.append(
                ft.Tab(
                    #adaptive=True,
                    tab_content=ft.Text(
                        size=20, 
                        value=abbreviature, 
                        weight=ft.FontWeight.W_900, 
                    ),
                    content=ft.Container(
                        data='shimmer', 
                        padding=ft.padding.only(left=15, right=15),
                        content=shimmer
                        
                        
                    )
                )
            )
       
        for i, category in enumerate(all_tabs):
            categories.content.content.controls.append(
                ft.Container(
                    key=i,
                    on_click=on_click_category,
                    alignment=ft.alignment.center_left, 
                    padding=ft.padding.only(left=15), 
                    bgcolor=None,
                    height=50, 
                    content=ft.Text(
                        value=page.client_storage.get('tabs')[category.tab_content.value], 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.colors.SECONDARY, 
                        size=18
                    )
                ),
            )

        news_view.controls[1] = ft.Stack(
            expand=True,
            controls=[tabs, button_categories]
        )
        on_load_tab_content(tabs.selected_index)

    def clean_tabs():
        all_tabs.clear()
        page.update()
    
    def go_regiser_view(e):
        page.floating_action_button.visible = False
        page.close_dialog()
        page.go('/index')
        
    def go_announce_view(e):
        if page.client_storage.get('role') != 'Аноним':
            page.go('/announce')
        else:
            page.dialog =  ft.AlertDialog(
                adaptive=True,
                open=True,
                title=ft.Text('Требуется авторизация', text_align=ft.TextAlign.CENTER),
                actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                
                content=ft.Text("Для доступа к функции создания мероприятий необходима регистрация. \
                                Пожалуйста, зарегистрируйтесь или войдите в систему, чтобы начать \
                                планирование событий", text_align=ft.TextAlign.CENTER),
                actions=[ft.TextButton('Отмена',on_click=lambda _: page.close_dialog()),
                         ft.TextButton('Регистрация', on_click=go_regiser_view)],
                
            )
            page.update()

    page.floating_action_button = ft.FloatingActionButton(
        visible=False,
        bgcolor=ft.colors.TERTIARY_CONTAINER,
        shape=ft.RoundedRectangleBorder(radius=5),
        width=135,
        mini=True,
        content=ft.Row(
            [ft.Text("Мои Анонсы"),ft.Icon(ft.icons.INPUT_ROUNDED)], alignment="center", spacing=3
        ),
        on_click=go_announce_view
    )
    
    logout_button = ft.TextButton('Выйти', on_click=handle_logout, style=ft.ButtonStyle(ft.colors.RED))
    all_tabs = []

    tabs = ft.Tabs(
        #adaptive=True,
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
        on_change=lambda e: on_load_tab_content(e.control.selected_index),
        tabs=all_tabs,
    )
    button_categories = ft.Container(
        
        padding=ft.padding.only(top=3),
        bgcolor=ft.colors.BACKGROUND,
        content=ft.IconButton(
            #добавляется кнопка, которая будет находится слева от категорий. Вызывающее BottomSheet
            style = ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=3),
                bgcolor=ft.colors.BACKGROUND,
                color=ft.colors.ON_SECONDARY_CONTAINER,
            ),
            icon=ft.icons.DEHAZE_OUTLINED,
            on_click=on_click_categories,
            height=40,
            width=50,
        ),
    ) 
    categories = ft.BottomSheet(
        open=True,
        enable_drag=True,
        show_drag_handle=True,
        maintain_bottom_view_insets_padding=True,
        on_dismiss=on_dismiss,
        content=ft.Container(
            padding=0,
            width=1000,
            height=1000,
            content=ft.Column(
                spacing=4,
                scroll=ft.ScrollMode.HIDDEN, 
            ),
        ),
    )

    page_shimmer = CustomShimmer(height=page.window_height, first_big=True, tabs=True)
    news_view = ft.Column(
        data='news',
        spacing=0,
        controls=[
            TopBar(exit_button=handle_logout),
            page_shimmer
        ],
    )

    return {
        'view': news_view,
        'load': on_load_news_view,
        'load_tab':on_load_tab_content, 
    }

