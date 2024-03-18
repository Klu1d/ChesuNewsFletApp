import flet as ft

class TopBar(ft.UserControl):
    def __init__(self, title='.news', exit_button=None):
        super().__init__()
        self.title = title
        self.exit_button = exit_button
        
    def build(self):
        self.popup_menu = ft.PopupMenuButton(
            content=ft.Container(ft.Icon(ft.icons.HOME_FILLED, color=ft.colors.ON_SECONDARY_CONTAINER), border_radius=15, margin=10),
            items=[
                ft.PopupMenuItem(content=ft.Row([ft.Icon(ft.icons.ACCOUNT_CIRCLE, color=ft.colors.ON_SECONDARY_CONTAINER), ft.Text('Учетная запись')]), on_click=self.on_click_account),
                ft.PopupMenuItem(content=ft.Row([ft.Icon(ft.icons.BOOKMARKS, color=ft.colors.ON_SECONDARY_CONTAINER), ft.Text('Избранное')]), on_click=self.on_click_bookmarks),
                ft.PopupMenuItem(content=ft.Row([ft.Icon(ft.icons.SETTINGS_ROUNDED, color=ft.colors.ON_SECONDARY_CONTAINER), ft.Text('Настройки')]), on_click=self.on_click_settings),
                ft.PopupMenuItem(content=ft.Row([ft.Icon(ft.icons.EXIT_TO_APP_ROUNDED, color=ft.colors.ON_SECONDARY_CONTAINER), ft.Text('Выйти')]), on_click=self.exit_button),
            ]
        )
        
        default_size_text = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
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
                    on_change=self.on_change_slider,
                ), 
                ft.Text('T', size=23)
            ]
        ) 
        
        self.settings = ft.BottomSheet(
            maintain_bottom_view_insets_padding=True,
            on_dismiss=self.on_dismiss_settings,
            is_scroll_controlled=True,
            enable_drag=True,
            use_safe_area=True,
            open=True,
            content=ft.Container(
                content=ft.ListView(
                    spacing=0,
                    controls=[
                        ft.ListTile(
                            trailing=ft.TextButton('Закрыть', on_click=self.on_click_close_settings),
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
                                adaptive=True,
                                value=False,
                                thumb_icon= {
                                    ft.MaterialState.SELECTED: ft.icons.CHECK,
                                    ft.MaterialState.DISABLED: ft.icons.CLOSE,
                                }
                            )
                        ),
                        ft.ListTile(
                            leading=ft.Text('Тема оформления', size=17),
                            trailing=ft.Switch(
                                adaptive=True,
                                on_change=self.on_change_theme, 
                                value=False,
                                thumb_icon= {
                                    ft.MaterialState.SELECTED: ft.icons.DARK_MODE,
                                    ft.MaterialState.DISABLED: ft.icons.LIGHT_MODE,
                                }
                                
                            ),     
                        ),
                        ft.ListTile(
                            leading = ft.Text('Размер текста по-умолчанию', size=17),
                            dense=True,
                        ),
                        ft.ListTile(dense=True, leading=default_size_text),
                        
                    ]
                )
            )
        )
        
        return ft.Container(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Container(
                        margin=ft.margin.only(left=15),
                        content=ft.Row(
                            spacing=0,
                            controls=[
                                ft.Image(src='./images/logo.png', height=40, width=40),
                                ft.Text(value=self.title, size=27, weight=ft.FontWeight.BOLD),
                            ]
                        ),
                    ),
                    ft.Container(
                        margin=ft.margin.only(right=10),
                        border_radius=15,
                        content=ft.Row(
                            spacing=2,
                            controls=[
                                ft.Badge(content=ft.IconButton(ft.icons.NOTIFICATIONS, icon_color=ft.colors.ON_SECONDARY_CONTAINER), text='23', alignment=ft.alignment.Alignment(0.4, -0.5)),
                                self.popup_menu,
                            ]
                        )
                    )
                ]
            )
        )

    def did_mount(self):
        self.settings.content.height = self.page.height - self.page.height * 16 / 100
        self.page.client_storage.set('slider_value', 32.5)
        self.page.update()

    def on_click_account(self, e):
        e.page.go('/account')
        e.page.update()
    
    def on_click_bookmarks(self, e):
        e.page.go('/bookmarks')
        e.page.update()     

    def on_click_settings(self, e):
        e.page.overlay.clear()
        e.page.overlay.append(self.settings)
        self.settings.open = True
        e.page.update()
        self.settings.update()

    def on_click_close_settings(self, e):
        e.page.overlay.clear()
        self.settings.open = False
        self.settings.update()

    def on_dismiss_settings(self, e):
        e.page.overlay.clear()
        e.page.update()

    def on_change_slider(self, e):
        e.page.client_storage.set('slider_value', e.control.value)
        e.page.update()

    def on_change_theme(self, e):
        if e.control.value == True:
            self.page.theme_mode = ft.ThemeMode.DARK
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT        
        self.page.update()
        