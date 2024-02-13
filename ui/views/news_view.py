import time
import flet as ft

from flet_contrib.shimmer import Shimmer
from ui.controller.top_bar import TopBar
from ui.controller.tab_display import TabDisplay
from ui.widgets.custom_shimmer import CustomShimmer

def NewsView(page, firebase):
    def handle_stream(message):
        build_tabs()
        page.update()

    def on_load_news():
        if firebase.check_token() == 'Success':
            news_view.controls[1] = page_shimmer
            page.update()
            firebase.stream_data(handle_stream)
            page.update()

    def handle_logout(*e):
        clean_tabs()
        firebase.kill_all_streams()
        firebase.sign_out()
        page.controls[0].content.content.controls[1].controls[0].selected_index = 0
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
        
    def on_load_tab_content(index):
        current_tab = all_tabs[index]
        full_name = page.client_storage.get('tabs')[current_tab.tab_content.value] #полное имя текущей, выбранной аббревиатуры
        if current_tab.content.data == 'shimmer':
            current_tab.content.data = 'content'
            current_tab.content=TabDisplay(page, full_name, firebase)
            
        page.client_storage.set('current_index_tab', index)
        page.floating_action_button.visible = True if current_tab.tab_content.value == 'Анонсы' else False
        page.overlay.clear()
        page.update()
        
    def build_tabs():
        all_tabs.clear()
        shimmer = CustomShimmer(height=page.window_height, first_big=True, tabs=False)
        for abbreviature in page.client_storage.get('tabs').keys():
            all_tabs.append(
                ft.Tab(
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
                ),
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

    page.floating_action_button = ft.FloatingActionButton(
        visible=False,
        bgcolor=ft.colors.TERTIARY_CONTAINER,
        shape=ft.RoundedRectangleBorder(radius=5),
        width=100,
        mini=True,
        content=ft.Row(
            [ft.Icon(ft.icons.POST_ADD), ft.Text("Создать")], alignment="center", spacing=3
        ),
        on_click=lambda _: page.go('/announce')
    )
    
    logout_button = ft.TextButton('Выйти', on_click=handle_logout, style=ft.ButtonStyle(ft.colors.RED))
    all_tabs = []

    tabs = ft.Tabs(
        expand=1,
        selected_index=1,
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
            #ft.ProgressBar(value=None, bgcolor=ft.colors.ON_SECONDARY),
            TopBar(exit_button=ft.PopupMenuItem(icon=ft.icons.EXIT_TO_APP, text='выйти', on_click=handle_logout)),
            page_shimmer
        ],
    )
    
    return {
        'view': news_view,
        'load': on_load_news,
    }

