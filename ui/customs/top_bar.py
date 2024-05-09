import flet as ft

class TopPanel(ft.AppBar):
    def __init__(self, button, button1):
        super().__init__()
        self.button = button
        self.button1 = button1
        self.adaptive = False
        
    
    def build(self):
        self.leading = ft.Container(
            margin=ft.margin.only(left=15),
            content=ft.Row(
                spacing=0,
                controls=[
                    #ft.Image(src='/home/mark/Development/copy_ches/assets/images/logo.png', height=40, width=40),
                    ft.Image(src='https://static.tildacdn.com/tild6230-3664-4432-b863-353833663132/__.png', height=40, width=40),
                    ft.Text(value='.news', size=27, weight=ft.FontWeight.BOLD),
                ]
            )
        )
        
        self.settings_button = ft.IconButton(
            icon=ft.icons.SETTINGS_ROUNDED,
            icon_color=ft.colors.INVERSE_SURFACE,
            selected_icon_color=ft.colors.BACKGROUND,
            on_click=self.on_click_settings
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
        
        self.settings_sheet = ft.BottomSheet(
            maintain_bottom_view_insets_padding=True,
            is_scroll_controlled=True,
            enable_drag=True, open=True,
            use_safe_area=True,
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
        
        self.actions = [
            self.button,
            self.button1,
            ft.IconButton(
                visible=bool(self.page.client_storage.get('role')),
                icon=ft.icons.ACCOUNT_CIRCLE_ROUNDED,
                icon_color=ft.colors.INVERSE_SURFACE,
                selected_icon_color=ft.colors.BACKGROUND,
                on_click=lambda _: self.page.go('/profile'),
                style = ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=3),
                    bgcolor=ft.colors.BACKGROUND,
                    color=ft.colors.INVERSE_SURFACE,
                )
            )
        ]

    def did_mount(self):
        self.settings_sheet.content.height = self.page.height - self.page.height * 16 / 100
        self.page.client_storage.set('slider_value', 32.5)
        self.page.update()

    def on_click_settings(self, e):
        e.page.dialog = self.settings_sheet
        e.page.dialog.open = True
        e.page.update()

    def on_click_close_settings(self, e):
        e.page.dialog.open = False
        e.page.update()

    def on_change_slider(self, e):
        e.page.client_storage.set('slider_value', e.control.value)
        e.page.update()

    def on_change_theme(self, e):
        if e.control.value == True:
            e.page.theme_mode = ft.ThemeMode.DARK
        else:
            e.page.theme_mode = ft.ThemeMode.LIGHT        
        e.page.update()
        