import flet as ft

class TopBar(ft.UserControl):
    def __init__(self, name='Chesu.news', exit_button=''):
        super().__init__()
        self.name = name
        self.exit_button = exit_button
        
    def build(self):
        self.navig = ft.NavigationDrawer(
            controls=[
                ft.FilledButton('Аккаунт', icon=ft.icons.ACCOUNT_BOX, on_click=self.show_settings),
            ],
        )
        
        self.popup_menu = ft.PopupMenuButton(
            icon=ft.icons.PERSON_ROUNDED,
            items=[
                ft.PopupMenuItem(icon=ft.icons.EDIT_ROUNDED, text='Учетная запись'),
                ft.PopupMenuItem(icon=ft.icons.BOOKMARKS, text='Архив', on_click=self.open_bookmarks_page),
                ft.PopupMenuItem(icon=ft.icons.SETTINGS_OUTLINED,  text='Настройки', on_click=self.show_settings), 
                self.exit_button             ]
        )
        
        default_size_text = ft.Row(
            alignment=ft.MainAxisAlignment.START,
            spacing=0,
            controls=[
                ft.Text('T', size=16), 
                ft.Slider(
                    min=10, 
                    max=100,
                    value=32.5,
                    divisions=4, 
                    width=250, 
                    height=100, 
                    adaptive=True,
                    label='{value}%',
                    on_change=self.slider_changed,
                ), 
                ft.Text('T', size=23)
            ]
        ) 
        self.settings = ft.BottomSheet(
            maintain_bottom_view_insets_padding=True,
            on_dismiss=self.settings_dismissed,
            is_scroll_controlled=True,
            enable_drag=True,
            use_safe_area=True,
            open=True,
            content=ft.Container(
                content=ft.ListView(
                    spacing=0,
                    controls=[
                        ft.ListTile(
                            trailing=ft.TextButton('Закрыть', on_click=self.close_settings),
                            content_padding=ft.padding.only(right=10)
                        ),
                        ft.ListTile(
                            leading=ft.Text('Настройки', weight=ft.FontWeight.W_700, size=30),
                        ),
                        ft.ListTile(
                            leading=ft.Text('Рубрики новостей', size=17),
                            trailing=ft.Icon(ft.icons.ARROW_FORWARD_IOS_ROUNDED, size=15),
                            
                        ),
                        ft.ListTile(
                            leading=ft.Text('Уведомления', size=17),
                            trailing=ft.Switch(
                                value=False,
                                thumb_icon= {
                                    ft.MaterialState.SELECTED: ft.icons.CHECK,
                                    ft.MaterialState.DISABLED: ft.icons.CLOSE,
                                }
                            )
                        ),
                        ft.ListTile(
                            leading=ft.Text('Тема оформления:', size=17),
                            trailing=ft.Switch(
                                
                                on_change=self.theme_changed, 
                                value=False,
                                thumb_icon= {
                                    ft.MaterialState.SELECTED: ft.icons.DARK_MODE,
                                    ft.MaterialState.DISABLED: ft.icons.LIGHT_MODE,
                                }
                                
                            ),     
                        ),
                        ft.ListTile(
                            leading = ft.Text('Размер текста по-умолчанию:', size=17),
                            dense=True,
                        ),
                        ft.ListTile(leading = default_size_text),
                        
                    ]
                )
            )
        )
        
        return ft.Stack(
            controls=[
                ft.Container(
                    padding=5,
                    
                    bgcolor=ft.colors.SECONDARY_CONTAINER,
                    border_radius=ft.border_radius.only(top_left=30, bottom_left=30, top_right=0, bottom_right=0),
                    margin=ft.margin.only(right=0, left=7, bottom=0, top=0),
                    content=ft.Row(
                        spacing=0,
                        controls=[
                            ft.Container(
                                margin=0,
                                padding=0,
                                expand=1,
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.START,
                                    controls=[
                                        
                                        ft.Container(
                                            margin=0,
                                            padding=0,
                                            border_radius=360,
                                            height=60,
                                            width=60
                                           
                                        ),
                                        ft.Text(value=self.name, size=20, weight=ft.FontWeight.BOLD)
                                    ],
                                ),
                            ),
                            ft.Badge(content=ft.IconButton(ft.icons.NOTIFICATIONS), text='23', alignment=ft.alignment.Alignment(0.4, -0.5)),
                            self.popup_menu,
                        ]
                    ),
                ),
                ft.Container(
                    margin=0,
                    padding=0,
                    content=ft.Image(
                        src='./assets/logo/logo.png',
                        height=70,
                        width=70,
                        
                    ),
                ),
            ]
        )

    def did_mount(self):
        self.settings.content.height = self.page.height - self.page.height * 16 / 100
        self.page.client_storage.set('slider_value', 32.5)
        self.page.update()

    def slider_changed(self, e):
        e.page.client_storage.set('slider_value', e.control.value)
        e.page.update()

    def show_drawer(self, e):
        self.page.end_drawer.open = True
        self.page.update()
        
    def open_bookmarks_page(self, e):
        e.page.go('/bookmarks')
        e.page.update()

    def settings_dismissed(self, e):
        e.page.overlay.clear()
        e.page.update()

    def show_settings(self, e:ft.TapEvent):
        e.page.overlay.clear()
        e.page.overlay.append(self.settings)
        
        self.settings.open = True
    
        
        e.page.update()
        self.settings.update()

    def close_settings(self, e):
        e.page.overlay.clear()
        self.settings.open = False
        self.settings.update()


    def theme_changed(self, e):
        if self.page.theme_mode == ft.ThemeMode.LIGHT:
            self.page.theme_mode = ft.ThemeMode.DARK
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT        
        self.page.update()
        