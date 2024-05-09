import flet as ft

from ui.customs.carousel import Carousel

class NewsArticle(ft.Container):
    def __init__(self, news_number: int, firebase):
        super().__init__()
        self.firebase = firebase
        self.news = self.firebase.get_news(news_number)[0]
        self.number_sheet = news_number
        self.icon_bookmark_visible = True

    
    def did_mount(self):
        self.on_change_slider(float(self.page.client_storage.get('slider_value')))

    def build(self):

        self.headline = ft.Container(
            padding=ft.padding.only(top=5, left=15, right=15, bottom=0),
            content=ft.Text(
                size=20,
                weight=ft.FontWeight.BOLD, 
                value=self.news.get('headline'), 
                selectable=True,
                font_family='Headline',
            )
        )
        self.text = ft.Container(
            content=ft.Text(self.news.get('text'),  selectable=True, size=16),
            padding=ft.padding.only(top=0, left=15, right=15, bottom=5),
        )

        self.datetime = ft.Container(
            margin=0,
            padding=ft.padding.only(top=0, left=15, right=15, bottom=0),
            content=ft.Text(value=self.news.get('datetime'),  selectable=True, size=14, color=ft.colors.SECONDARY)
        )
        
        self.text_size_format = ft.Container(
            height=0,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.ON_SECONDARY,
            animate=ft.animation.Animation(400, ft.AnimationCurve.DECELERATE),
            padding=ft.padding.only(left=35, right=35),
            border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15),
            content=ft.Row(
                spacing=0,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("T", size=16), 
                    ft.Slider(
                        expand=10,
                        min=10, 
                        max=100,
                        value=float(self.page.client_storage.get('slider_value')), 
                        divisions=4, 
                        label="{value}%",
                        on_change=lambda e: self.on_change_slider(e.control.value),
                        adaptive=True,
                    ), 
                    ft.Text("T", size=23)
                ]
            )
        )

        self.top_panel = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.IconButton(
                    selected=True,
                    icon=ft.icons.CLOSE_ROUNDED,
                    on_click=lambda _: self.page.close_bottom_sheet(), 
                ),
                ft.Text(value=self.news["headline"], expand=True, font_family='Headline', overflow=ft.TextOverflow.ELLIPSIS, weight=ft.FontWeight.BOLD),
                ft.Row(
                    spacing=1,
                    controls=[
                        ft.IconButton(
                            visible=True if self.page.views[-1].route != '/bookmarks' and self.page.client_storage.get('role') else False,
                            data=self.number_sheet,
                            icon_color=ft.colors.PRIMARY,
                            icon=ft.icons.BOOKMARK_BORDER,
                            selected_icon=ft.icons.BOOKMARK,
                            selected=self.icon_bookmark_visible,
                            on_click=self.on_click_icon_bookmark,
                        ),
                        ft.IconButton(
                            icon_color=ft.colors.PRIMARY,
                            icon=ft.icons.FORMAT_SIZE,
                            on_click=self.on_click_icon_format,
                        ),
                        ft.IconButton(
                            icon_color=ft.colors.PRIMARY,
                            icon=ft.icons.SHARE,
                            on_click=lambda _: print("share"),
                        )    
                    ]
                )
            ]
        )
        
        self.content = ft.Container(
            border_radius=ft.border_radius.only(top_left=15, top_right=15),
            height=self.page.height - self.page.height * 16 / 100,
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Container(
                        bgcolor=ft.colors.ON_SECONDARY,
                        content=self.top_panel,
                    ),
                    self.text_size_format,
                    ft.Column(
                        expand=True,
                        scroll='hidden',
                        controls=[
                            self.headline,
                            self.datetime,
                            Carousel(images=[linq for linq in self.news.get('images')]),
                            self.text
                        ]
                    )
                ]
            )
        )


    def on_click_icon_bookmark(self, e):
        e.control.selected = not e.control.selected
        self.update()
        bookmarks = self.page.client_storage.get("bookmarks")
        if e.control.data in bookmarks:
            bookmarks.remove(e.control.data)
            self.firebase.set_bookmark(bookmarks)
            self.page.client_storage.set("bookmarks", bookmarks)
        else:
            bookmarks.insert(0, e.control.data)
            self.firebase.set_bookmark(bookmarks)
            self.page.client_storage.set("bookmarks", bookmarks) 

    def on_click_icon_format(self, e):
        self.text_size_format.height = 50 if self.text_size_format.height != 50 else 0
        self.update() 

    def on_change_slider(self, value):
        match value:
            case 100:
                self.headline.content.size = 35
                self.datetime.content.size = 29
                self.text.content.size = 31
            case 77.5:
                self.headline.content.size = 30
                self.datetime.content.size = 24
                self.text.content.size = 26
            case 55.0:
                self.headline.content.size = 26
                self.datetime.content.size = 20
                self.text.content.size = 22
            case 32.5:
                self.headline.content.size = 20
                self.datetime.content.size = 14
                self.text.content.size = 16
            case 10:
                self.headline.content.size = 15
                self.datetime.content.size = 9
                self.text.content.size = 11
        self.update()
