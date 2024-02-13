import random
import flet as ft

from flet_contrib.shimmer import Shimmer

class CustomShimmer(ft.UserControl):
    def __init__(self, quantity = None, height = None, first_big=False, tabs=False):
        super().__init__()
        self.page_height = int(height)
        self.view_first = first_big
        self.view_tabs = tabs
            
    def build(self):
        if self.view_tabs:
            return self.on_load_page_shimmer()
        else:
            return self.tab_content_shimmer()
    
    def bookmarks_shimmer(self):
        pass
    def tab_content_shimmer(self):
        first = ft.Container(
            data='shimmer_load', 
            bgcolor=ft.colors.SECONDARY_CONTAINER,
            border_radius=15, 
            padding=30,
            height=220,
            alignment=ft.alignment.bottom_left,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.END, 
                spacing=10,
                controls=[
                    ft.Container(data='shimmer_load', height=12, width=200, border_radius=15,bgcolor=ft.colors.BACKGROUND), 
                    ft.Container(data='shimmer_load', height=12, width=90, border_radius=15, bgcolor=ft.colors.BACKGROUND), 
                ]
            )
        )
        usual = ft.Container(
            padding=5,
            border_radius=0, 
            content=ft.Row(
                controls=[
                    ft.Container(data='shimmer_load', opacity=1, bgcolor=ft.colors.SECONDARY_CONTAINER, border_radius=15, width=100, height=100),
                    ft.Column(alignment=ft.MainAxisAlignment.CENTER, spacing=10, controls=[
                            ft.Container(data='shimmer_load', opacity=1, bgcolor=ft.colors.SECONDARY_CONTAINER, height=12, width=170, border_radius=15), 
                            ft.Container(data='shimmer_load', opacity=1, bgcolor=ft.colors.SECONDARY_CONTAINER, height=12, width=90, border_radius=15), 
                        ]
                    )
                ]
            )
        )
        

        count = (((self.page_height - 220) // 100) if self.view_first else self.page_height // 100) - 4
        controls = [first if self.view_first and i == 0 else usual for i in range(count)]

        return ft.Container(
            opacity=0.3,
            data='shimmer_load',  
            content=ft.Column(
                spacing=10,
                controls=controls
            )
        )
        # return Shimmer(
        #     control=ft.Container(
        #         opacity=0.6,
        #         data='shimmer_load',  
        #         content=ft.Column(
        #             spacing=10,
        #             controls=controls
        #         )
        #     ),
            
        # )
    def on_load_page_shimmer(self):
        first = ft.Container(
            data='shimmer_load', 
            bgcolor=ft.colors.SECONDARY_CONTAINER,
            margin=ft.margin.only(bottom=10, left=15, right=15) if self.view_tabs else None,
            border_radius=15, 
            padding=30,
            height=220,
            alignment=ft.alignment.bottom_left,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.END, 
                spacing=10,
                controls=[
                    ft.Container(data='shimmer_load', height=12, width=200, border_radius=15,bgcolor=ft.colors.BACKGROUND), 
                    ft.Container(data='shimmer_load', height=12, width=90, border_radius=15, bgcolor=ft.colors.BACKGROUND), 
                ]
            )
        )
        usual = ft.Container(
            padding=5,
            margin=ft.margin.only(bottom=10, left=15, right=15) if self.view_tabs else None,
            border_radius=0, 
            content=ft.Row(
                controls=[
                    ft.Container(data='shimmer_load', opacity=1, bgcolor=ft.colors.SECONDARY_CONTAINER, border_radius=15, width=100, height=100),
                    ft.Column(alignment=ft.MainAxisAlignment.CENTER, spacing=10, controls=[
                            ft.Container(data='shimmer_load', opacity=1, bgcolor=ft.colors.SECONDARY_CONTAINER, height=12, width=170, border_radius=15), 
                            ft.Container(data='shimmer_load', opacity=1, bgcolor=ft.colors.SECONDARY_CONTAINER, height=12, width=90, border_radius=15), 
                        ]
                    )
                ]
            )
        )
        
        tabs = ft.Container(
            data='shimmer_load', 
            border_radius=0, 
            margin=ft.margin.only(bottom=5, left=15, top=15),
            
            alignment=ft.alignment.bottom_left,
            content=ft.Container(
                content=ft.Row(
                    expand=True,
                    controls=[ft.Container(data='shimmer_load', bgcolor="secondarycontainer", border_radius=15, width=random.randrange(70, 130, 10), height=35) for i in range(5)]
                )
            )
        )
        
        
        count = (((self.page_height - 220) // 100) if self.view_first else self.page_height // 100) - 4
        controls = [first if self.view_first and i == 0 else usual for i in range(count)]
        if self.view_tabs:
            controls.insert(0, tabs)

        return Shimmer(
            control=ft.Container(
                opacity=0.6,
                data='shimmer_load',  
                content=ft.Column(
                    spacing=10,
                    controls=controls
                )
            ),
            
        )
            
