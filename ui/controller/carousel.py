import random
import flet as ft

from typing import List


class Carousel(ft.UserControl):
    def __init__(self,
                 images: List[str],
                 shuffle: bool = False,
                 active_color: str = ft.colors.ON_SURFACE_VARIANT,
                 inactive_color: str = ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE_VARIANT)):
        super().__init__()
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.images = images
        self.carousel_image_ref = ft.Ref()
        self.carousel_btn_container_ref = ft.Ref()
        self.carousel_button_ref = ft.Ref()
        self.shuffle = shuffle
        if self.shuffle:
            self.images = random.sample(self.images, len(self.images))

    def swipe_handler(self, e: ft.DragEndEvent):
        current_image = self.carousel_image_ref.current.content.src
        current_index = self.images.index(current_image)
        images_len = len(self.images)
        next_index = current_index + 1

        try:
            next_image = self.images[next_index]
        except IndexError:
            next_image = self.images[0]
        prev_index = current_index - 1
        try:
            prev_image = self.images[prev_index]
        except IndexError:
            prev_image = self.images[images_len]

        if e.primary_velocity > 0:
            self.carousel_image_ref.current.content = ft.Image(
                src=prev_image,
                color_blend_mode=ft.BlendMode.COLOR_BURN,
            )
            for carousel_btn in self.carousel_btn_container_ref.current.controls:
                if carousel_btn.data != prev_image:
                    carousel_btn.bgcolor = self.inactive_color
                    carousel_btn.height = 5
                else:
                    carousel_btn.bgcolor = self.active_color
                    carousel_btn.height = 7
            self.update()
        if e.primary_velocity < 0:
            self.carousel_image_ref.current.content = ft.Image(
                src=next_image,
                color_blend_mode=ft.BlendMode.COLOR_BURN,
            )
            for carousel_btn in self.carousel_btn_container_ref.current.controls:
                if carousel_btn.data != next_image:
                    carousel_btn.bgcolor = self.inactive_color
                    carousel_btn.height = 5
                else:
                    carousel_btn.bgcolor = self.active_color
                    carousel_btn.height = 7
            self.update()

    # Register callbacks
    def carousel_click(self, e):
        self.carousel_image_ref.current.src = e.control.data
        e.control.bgcolor = self.active_color
        for carousel_btn in self.carousel_btn_container_ref.current.controls:
            if carousel_btn.data != e.control.data:
                carousel_btn.bgcolor = self.inactive_color
                carousel_btn.height = 10
        self.update()

    def build(self):
        return ft.GestureDetector(
            expand=True,
            on_horizontal_drag_end=self.swipe_handler,
            content=ft.Container(
                padding=ft.padding.only(top=0),
                height=220,
                bgcolor=ft.colors.SECONDARY_CONTAINER,
                alignment=ft.alignment.center,
                content=ft.Stack(
                    controls=[
                        ft.Container(
                            alignment = ft.alignment.center,
                            content=ft.AnimatedSwitcher(
                                content=ft.Image(
                                    src=[carousel_image for carousel_image in self.images][0],
                                    color_blend_mode=ft.BlendMode.COLOR_BURN,
                                    
                                ),
                                ref=self.carousel_image_ref,
                                transition=ft.AnimatedSwitcherTransition.FADE,
                                duration=500,
                                reverse_duration=1000,
                                switch_in_curve=ft.AnimationCurve.EASE_IN,
                                switch_out_curve=ft.AnimationCurve.EASE_IN_BACK,
                            ),
                        ),
                        ft.Container(
                            alignment=ft.alignment.bottom_center,
                            padding=ft.padding.only(bottom=-11),
                            visible=False if len(self.images) == 1 else True,
                            content=ft.Row(
                                ref=self.carousel_btn_container_ref,
                                controls=[
                                    ft.Container(
                                        data=img,
                                        opacity=1,
                                        bgcolor=self.inactive_color,
                                        height=5,
                                        width=(1 / len(self.images) * 300) - 10,
                                        ref=self.carousel_button_ref,
                                        border_radius=10,
                                        
                                        on_click=self.carousel_click,
                                    )if img != self.images[0] else ft.Container(
                                        data=img,
                                        bgcolor=self.active_color,
                                        height=7,
                                        width=(1 / len(self.images) * 300) - 10,
                                        opacity=1,
                                        border_radius=10,
                                        ref=self.carousel_button_ref,
                                        on_click=self.carousel_click,
                                    )
                                    for img in self.images
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=10,
                            )
                        )
                    ]
                )
            )
        )
    
