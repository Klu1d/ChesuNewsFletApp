import flet as ft

from ui.controller.carousel import Carousel

class CustomBottomSheet(ft.BottomSheet):
    def __init__(self, pyrebase):
        super().__init__()
        self.pyrebase = pyrebase
        
    def build(self):
        self.news_sheet = ft.BottomSheet(
            enable_drag=True,
            dismissible=True,
            is_scroll_controlled=True,
            maintain_bottom_view_insets_padding=True,
            content=ft.Container(
                padding=0,
                expand=True,
                content=ft.Column(
                    spacing=0,
                    controls=[
                        ft.Container(
                            border_radius=ft.border_radius.only(top_left=15,top_right=15),
                            bgcolor=ft.colors.ON_SECONDARY,
                            padding=ft.padding.only(left=20, right=20),
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.IconButton(
                                        selected=True,
                                        icon=ft.icons.ARROW_BACK,
                                        
                                    ),
                                    ft.Text(expand=True, overflow=ft.TextOverflow.ELLIPSIS, weight=ft.FontWeight.BOLD),
                                    ft.Row(
                                        spacing=1,
                                        controls=[
                                            ft.IconButton(
                                                selected=True,
                                                icon=ft.icons.BOOKMARK_BORDER,
                                                
                                            ),
                                            ft.IconButton(
                                                selected=True,
                                                icon=ft.icons.FORMAT_SIZE,
                                                on_click=lambda _: print("text size"),
                                            ),
                                            ft.IconButton(
                                                selected=True,
                                                icon=ft.icons.SHARE,
                                                on_click=lambda _: print("share"),
                                            )
                                            
                                        ]
                                    )
                                ]
                            ),
                        ),
                        ft.Container(
                            expand=True,
                            padding=ft.padding.only(left=20, right=20),
                            content=ft.Column(
                                scroll="hidden"
                            )
                        )
                    ]
                ),
            )
        )
        return self.news_sheet
        
    def on_load(self, news_number):
        news = self.pyrebase.get_news(news_number)
        self.news_sheet.content.content.controls[0].content.controls[1].value = news["headline"]
        self.news_sheet.content.content.controls[1].content.controls = [
            ft.Container(
                padding=ft.padding.only(top=5, left=15, right=15, bottom=0),
                content=ft.Text(
                    size=20,
                    weight=ft.FontWeight.BOLD, 
                    value=news["headline"], 
                )
            ),
            ft.Container(
                margin=0,
                padding=ft.padding.only(top=0, left=15, right=15, bottom=0),
                content=ft.Text(value=news["datetime"], size=14, color=ft.colors.SECONDARY)
            ),
            Carousel(images=[linq for linq in news["images"]]),
            ft.Container(
                content=ft.Text(news["text"], size=16),
                padding=ft.padding.only(top=0, left=15, right=15, bottom=5),
            ),
            ft.Divider(height=3, color=ft.colors.SECONDARY_CONTAINER),
            ft.Container(
                padding=5,
                content=ft.Row(
                    wrap=True,
                    controls=[ft.OutlinedButton(
                        tag,
                        style = ft.ButtonStyle(
                            
                            color=ft.colors.ON_SECONDARY_CONTAINER,
                            shape=ft.RoundedRectangleBorder(radius=3),
                            bgcolor=ft.colors.BACKGROUND,
                            overlay_color=ft.colors.SECONDARY,
                        ),
                    ) for tag in news["tags"]]
                )
            ),
        ]
        
    def close_sheet(self):
        self.news_sheet.open = False
        
   