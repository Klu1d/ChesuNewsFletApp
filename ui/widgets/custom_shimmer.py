import flet as ft
from flet_contrib.shimmer import Shimmer

class CustomShimmer(ft.UserControl):
    def __init__(self, quantity = None, height = None, first_big=False):
        super().__init__()
        self.big_first = first_big
        self.page_height = int(height)
            
    def build(self):
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
        
        
        count = (((self.page_height - 220) // 100) if self.big_first else self.page_height // 100) - 4
        controls = [first if self.big_first and i == 0 else usual for i in range(count)]
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
            
            
  
