import time
import flet as ft

from ui.controller.top_bar import TopBar
from ui.controller.tab_display import TabDisplay
from ui.controller.shimmer import Shimmer

def NewsView(page, myPyrebase):
    
    def handle_stream(message):
        try:
            build_tabs()
            page.update()
        except:
            pass

    def on_page_load():
        if myPyrebase.check_token() == 'Success':
            myPyrebase.stream_data(handle_stream)
            handle = myPyrebase.get_username()
            page.update()

    def handle_logout(*e):
        clean_tabs()
        myPyrebase.kill_all_streams()
        myPyrebase.sign_out()
        page.controls[0].content.content.controls[1].controls[0].selected_index = 0
        page.go('/')
    
    def on_click_category(e):
        categories.content.content.controls[page.client_storage.get('current_index_tab')].bgcolor=None
        categories.content.content.controls[e.control.key].bgcolor=ft.colors.BLACK12
        page.controls[0].content.content.controls[1].controls[0].selected_index = e.control.key
        categories.open=False
        page.update()
        on_load_tab_content(e.control.key)
    
    def on_click_categories(e):
        data = myPyrebase.get_tabs()
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
                        value=data[category.tab_content.value], 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.colors.SECONDARY, 
                        size=18
                    )
                ),
            )
        page.overlay.clear()
        page.overlay.append(categories)
        categories.content.content.controls[page.client_storage.get('current_index_tab')].bgcolor=ft.colors.BLACK12
        categories.open = True
        page.update()
        
    def on_dismiss(e):
        page.overlay.clear()
        page.update()
        
    def on_load_tab_content(index):
        page.client_storage.set('current_index_tab', index)
        current_tab = all_tabs[index]
        full_name = myPyrebase.get_tabs()[current_tab.tab_content.value] #полное имя текущей, выбранной аббревиатуры
        
        if page.client_storage.get('bookmarks') == None:
            page.client_storage.set('bookmarks', [])
        
        if current_tab.content.data == 'shimmer':
            current_tab.content=TabDisplay(page=page, tab_name=full_name, myPyrebase=myPyrebase)
        
        page.overlay.clear()
        page.update()
        
    def build_tabs():
        all_tabs.clear()
        new = ft.Container(data='shimmer_load', border_radius=15, padding=5, height=220, width=3000,content=ft.Container(data='shimmer_load', border_radius=15, padding=30, content=ft.Column(spacing=15, alignment=ft.MainAxisAlignment.END, controls=[ft.Text(value='texttexttexttexttexttext', data='shimmer_load'), ft.Text(value='20-30-1203', data='shimmer_load')])))
        old = ft.Container(data='shimmer_load', border_radius=15, margin=ft.margin.only(right=15, left=15),padding=5, height=100, content=ft.Row(spacing=10,controls=[ft.Container(data='shimmer_load', border_radius=15, width=100, height=100),ft.Column(alignment=ft.MainAxisAlignment.CENTER, spacing=10, controls=[ft.Text(value='tettexttexttexttext', data='shimmer_load'), ft.Text(value='20-30-1203', data='shimmer_load') ])]))
        temp = [
            Shimmer(control=new, auto_generate=True),
            Shimmer(control=old, auto_generate=True),
            Shimmer(control=old, auto_generate=True),
            Shimmer(control=old, auto_generate=True),
            Shimmer(control=old, auto_generate=True),
            Shimmer(control=old, auto_generate=True),
        ]
        for abbreviature in page.client_storage.get("abbreviature"):
            all_tabs.append(
                    ft.Tab(
                        tab_content=ft.Text(
                            size=20, 
                            value=abbreviature, 
                            weight=ft.FontWeight.W_900, 
                        ),
                        content=ft.Container(
                            expand=True, 
                            data='shimmer', 
                            padding=ft.padding.only(left=15, right=15), 
                            content=ft.Column(
                                expand=True,
                                controls=temp,
                                
                            )
                        )
                    ),
                )
        page.update() 
        
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
                        value=myPyrebase.get_tabs()[category.tab_content.value], 
                        weight=ft.FontWeight.BOLD, 
                        color=ft.colors.SECONDARY, 
                        size=18
                    )
                ),
            )
        page.update()
        
        on_load_tab_content(tabs.selected_index)
        
    def preloader(activate):
        if activate:
            page.overlay.append(ft.Container(bgcolor='red',width=200, height=200, on_click=lambda _: print("dada")))
            page.update()
        else:
            page.overlay.clear()
            page.update()
   
    def clean_tabs():
        all_tabs.clear()
        page.update()

    logout_button = ft.TextButton('Выйти', on_click=handle_logout, style=ft.ButtonStyle(ft.colors.RED))
    all_tabs = []
    
    tabs = ft.Tabs(
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

    myPage = ft.Column(
        data='news',
        spacing=0,
        controls=[
            #ft.ProgressBar(value=None, bgcolor=ft.colors.ON_SECONDARY),
            TopBar(exit_button=ft.PopupMenuItem(icon=ft.icons.EXIT_TO_APP, text='выйти', on_click=handle_logout)),
            ft.Stack(
                expand=True,
                controls=[
                    tabs,
                    button_categories,
                ]
            )
        ],
    )
   
    
            
    return {
        'view': myPage,
        'load': on_page_load
    }

