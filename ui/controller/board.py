import flet as ft

from datetime import date, timedelta
from ui.controller.carousel import Carousel
        
class Board(ft.UserControl):
    def __init__(self, page, firebase):
        super().__init__()
        self.firebase = firebase
        self.page = page    
    
    def old(self, number, image, headline, time, vision=True, opacity=True, checkbox=False):
        return ft.Container(
            key=str(number),
            data=time,
            visible=vision,
            ink=opacity,
            height=100,
            opacity=1,
            margin=ft.margin.only(right=15, left=15, bottom=0, top=0),
            animate_size=ft.animation.Animation(150),
            border_radius=15,
            on_click=lambda e: self.on_click_board_container(e, number, checkbox),
            content=ft.Container(
                bgcolor="secondarycontainer, 0.8",
                padding=ft.padding.only(left=5, right=5, top=5, bottom=5),
                border_radius=15,
                border=ft.border.all(1, "onsecondarycontainer, 0.2"),
                content=ft.Row(
                    controls=[
                        ft.Image(
                            border_radius=15,
                            fit=ft.ImageFit.COVER,
                            src=image,
                            height=100,
                            width=100,
                            expand=1,
                        ),
                        ft.Container(
                            margin=5,
                            expand=2,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=0,
                                controls=[
                                    ft.Text(
                                        max_lines=3,
                                        weight=ft.FontWeight.W_600,
                                        text_align=ft.TextAlign.LEFT,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                        value=headline,   
                                    ),
                                    ft.Text(max_lines=1, value=self.time_display(time), color="grey"),
                                ],
                            ),
                        ),
                    ],
                )
            )
        )
        
    def new(self, number, image, headline, time):
        return ft.Container(
            height=220,
            ink=True,
            opacity=1,
            data=time,
            key=number,
            border_radius=15,
            alignment=ft.alignment.center_left,
            animate_size=ft.animation.Animation(150),
            margin=ft.margin.only(right=15, left=15, bottom=3, top=0),
            on_click=lambda e: self.on_click_board_container(e, number),
            content=ft.Container(
                border_radius=15,
                padding=ft.padding.only(left=5,top=5,right=5,bottom=5),
                bgcolor="secondarycontainer, 0.8",
                border=ft.border.all(1, "onsecondarycontainer, 0.2"),
                content=ft.Stack(
                    controls=[
                        ft.ShaderMask(
                            border_radius=15,
                            content=ft.Image(
                                src=image,
                                fit=ft.ImageFit.COVER,
                                width=2000,
                                height=220,
                            ),
                            shader=ft.LinearGradient(
                                stops=[0.2, 1],
                                begin=ft.alignment.top_center,
                                end=ft.alignment.bottom_center,
                                colors=[ft.colors.WHITE, ft.colors.BLACK],
                            ),
                        ),
                        ft.Container(
                            alignment=ft.alignment.Alignment(-1, 0.6),
                            padding=20,
                            content=ft.Text(
                                value=headline,
                                text_align=ft.TextAlign.LEFT,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                weight=ft.FontWeight.BOLD,
                                color='white', 
                                max_lines=3,
                                size=20, 
                            ),
                        ),
                        ft.Container(
                            alignment=ft.alignment.bottom_left,
                            padding=20,
                            content=ft.Text(
                                value=self.time_display(time),
                                text_align=ft.TextAlign.LEFT,
                                overflow=ft.TextOverflow.ELLIPSIS,
                                color='grey',
                                max_lines=3,
                                size=12, 
                            ),
                        )
                    ]
                ),
            )
        )
    
    def announce(self, number):
        announceContainer = ft.Column(
                spacing=0,
                controls=[
                    ft.Text("Завтра", size=25),
                    ft.Container(
                        border_radius=15,
                        margin=ft.margin.only(left=10),
                        content=ft.Column(
                            controls=[
                                ft.ExpansionPanelList(
                                    spacing=0,
                                    controls=[
                                        ft.ExpansionPanel(
                                            bgcolor="secondarycontainer, 0.6",
                                            header=ft.ListTile(title=ft.Text(f"ЮРФАК", size=20)),
                                            expanded=True,
                                            content=ft.Container(
                                                bgcolor='green', 
                                                border_radius=15,
                                                height=100
                                            ),
                                        ),
                                        ft.ExpansionPanel(
                                            bgcolor="secondarycontainer, 0.6",
                                            header=ft.ListTile(title=ft.Text(f"ЮРФАК", size=20)),
                                            expanded=True,
                                            content=ft.Container(
                                                bgcolor='blue', 
                                                border_radius=15,  
                                                height=100
                                            ),
                                            
                                        )
                                    ]
                                ),
                            ]
                        )
                    )
                ] 
            )
 
    def show_news_sheet(self, news_number, icon_bookmark):
        self.news_sheet = ft.BottomSheet(
            use_safe_area=True,
            dismissible=True,
            on_dismiss=self.on_dismiss_news_sheet,
            enable_drag=True,
            is_scroll_controlled=True,
            maintain_bottom_view_insets_padding=True,
            content=ft.Container(
                height=self.page.height - self.page.height * 16 / 100,
                padding=0,
                expand=True,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    spacing=0,
                    controls=[
                        ft.Container(
                            padding=ft.padding.only(top=5, bottom=5, left=5, right=5),
                            border_radius=ft.border_radius.only(top_left=15,top_right=15),
                            bgcolor=ft.colors.ON_SECONDARY,
                            animate=ft.animation.Animation(200, ft.AnimationCurve.DECELERATE),
                            height=55,
                            content=ft.Column(
                                spacing=0,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.IconButton(
                                                selected=True,
                                                icon=ft.icons.CLOSE_ROUNDED,
                                                on_click=self.on_click_close 
                                            ),
                                            ft.Text(expand=True, overflow=ft.TextOverflow.ELLIPSIS, weight=ft.FontWeight.BOLD),
                                            ft.Row(
                                                spacing=1,
                                                controls=[
                                                    ft.IconButton(
                                                        visible=icon_bookmark,
                                                        data=news_number,
                                                        icon_color=ft.colors.PRIMARY,
                                                        icon=ft.icons.BOOKMARK_BORDER,
                                                        selected_icon=ft.icons.BOOKMARK,
                                                        selected=self.page.client_storage.get("bookmarks").__contains__(news_number),
                                                        on_click=self.on_click_bookmark,
                                                    ),
                                                    ft.IconButton(
                                                        icon_color=ft.colors.PRIMARY,
                                                        icon=ft.icons.FORMAT_SIZE,
                                                        on_click=self.on_click_text_size,
                                                    ),
                                                    ft.IconButton(
                                                        icon_color=ft.colors.PRIMARY,
                                                        icon=ft.icons.SHARE,
                                                        on_click=lambda _: print("share"),
                                                    )    
                                                ]
                                            )
                                        ]
                                    ),
                                ]
                            )
                        ),
                        ft.Container(
                            expand=True,
                            padding=ft.padding.only(left=0, right=0),
                            content=ft.Column(
                                scroll="hidden"
                            )
                        )
                    ]
                ),
            )
        )
        return self.news_sheet
    
    def on_load_news(self, news_number):
        news = self.firebase.get_news(news_number)[0]
        self.news_sheet.content.content.controls[0].content.controls[0].controls[1].value = news["headline"]
        self.news_sheet.content.content.controls[1].content.controls = [
            ft.Container(
                padding=ft.padding.only(top=5, left=15, right=15, bottom=0),
                content=ft.SelectionArea(
                    content=ft.Text(
                        size=20,
                        weight=ft.FontWeight.BOLD, 
                        value=news["headline"], 
                    )
                )
            ),
            ft.Container(
                margin=0,
                padding=ft.padding.only(top=0, left=15, right=15, bottom=0),
                content=ft.Text(value=news["datetime"], size=14, color=ft.colors.SECONDARY)
            ),
            Carousel(images=[linq for linq in news["images"]]),
            ft.Container(
                content=ft.SelectionArea(ft.Text(news["text"], size=16)),
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
        
        self.on_change_slider(self.slider_value)
           
    def on_click_bookmark(self, e):
        e.control.selected = not e.control.selected
        self.page.update()
        
        bookmarks = self.page.client_storage.get("bookmarks")
        if e.control.data in bookmarks:
            bookmarks.remove(e.control.data)
            self.firebase.set_bookmark(bookmarks)
            self.page.client_storage.set("bookmarks", bookmarks)
        else:
            bookmarks.insert(0, e.control.data)
            self.firebase.set_bookmark(bookmarks)
            self.page.client_storage.set("bookmarks", bookmarks)     

    def on_click_text_size(self, e):
        
        checkif = self.news_sheet.content.content.controls[0].height
        self.news_sheet.content.content.controls[0].height = 100 if checkif == 55 else 55
        self.news_sheet.content.content.controls[0].border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15, top_left=15, top_right=15) if checkif == 55 else ft.border_radius.only(bottom_left=0, bottom_right=0, top_left=15, top_right=15)
    
        text_size_slider = ft.Container(
            padding=ft.padding.only(left=35, right=35),
            alignment=ft.alignment.center,
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
                        value=self.slider_value, 
                        divisions=4, 
                        label="{value}%",
                        on_change=self.on_change_slider,
                        adaptive=True,
                    ), 
                    ft.Text("T", size=23)
                ],
                
            )
        )
        if checkif == 55:
            self.news_sheet.content.content.controls[0].content.controls.insert(1, text_size_slider) 
        else:
            self.news_sheet.content.content.controls[0].content.controls.pop()
        self.news_sheet.update()
        
    def on_change_slider(self, e):
        value = 32.5
        if type(e) == float:
            value = e
        else:
            value = e.control.value
        match value:
            case 100:
                
                self.news_sheet.content.content.controls[1].content.controls[0].content.content.size = 35
                self.news_sheet.content.content.controls[1].content.controls[1].content.size = 29
                self.news_sheet.content.content.controls[1].content.controls[3].content.size = 31
            case 77.5:
                self.news_sheet.content.content.controls[1].content.controls[0].content.content.size = 30
                self.news_sheet.content.content.controls[1].content.controls[1].content.size = 24
                self.news_sheet.content.content.controls[1].content.controls[3].content.size = 26
            case 55.0:
                self.news_sheet.content.content.controls[1].content.controls[0].content.content.size = 26
                self.news_sheet.content.content.controls[1].content.controls[1].content.size = 20
                self.news_sheet.content.content.controls[1].content.controls[3].content.size = 22
            case 32.5:
                self.news_sheet.content.content.controls[1].content.controls[0].content.content.size = 20
                self.news_sheet.content.content.controls[1].content.controls[1].content.size = 14
                self.news_sheet.content.content.controls[1].content.controls[3].content.size = 16
            case 10:
                self.news_sheet.content.content.controls[1].content.controls[0].content.content.size = 15
                self.news_sheet.content.content.controls[1].content.controls[1].content.size = 9
                self.news_sheet.content.content.controls[1].content.controls[3].content.size = 11
                
        self.news_sheet.update()
    
    def on_dismiss_news_sheet(self, e):
        self.page.overlay.clear()
    
    def on_click_close(self, e):
        self.news_sheet.open = False
        self.page.update()
        self.page.overlay.clear()

    def on_click_board_container(self, event: ft.TapEvent, number: int, checkbox: bool = False):

        self.slider_value = self.page.client_storage.get("slider_value")
        self.page.overlay.clear()
        news_paper = self.show_news_sheet(number, False if len(self.page.views) == 2 else True)
        
        self.page.overlay.clear()
        self.page.overlay.append(news_paper)
        news_paper.open = True
        self.page.update()
        
        self.on_load_news(number)            
        self.page.update()
            
        event.control.opacity = 0.6 if event.control.ink != False else 1
        event.control.update()
            
    def time_display(self, input_date: str):
        today = date.today().strftime('%d-%m-%Y')
        yesterday = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
        
        if input_date.split(' ')[0] == today:
            return f"Сегодня в {input_date.split(' ')[1]}"
        elif input_date.split(' ')[0] == yesterday:
            return f"Вчера в {input_date.split(' ')[1]}"
        else:
            return input_date
    

