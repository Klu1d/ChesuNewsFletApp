import flet as ft

class Categories(ft.Container):
    def __init__(self):
        super().__init__()
        self.controls = []
        self.padding=ft.padding.only(top=3)
        self.bgcolor=ft.colors.BACKGROUND
        self.padding = ft.padding.only(left=5, top=2)
    def build(self):
        self.content=ft.IconButton(
            height=40, width=50, adaptive=False,
            on_click=self.open_categories,
            icon=ft.icons.DEHAZE_OUTLINED,
            style = ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=3),
                bgcolor=ft.colors.BACKGROUND,
                color=ft.colors.ON_SECONDARY_CONTAINER,
            )
        )

    def open_categories(self, e: ft.ControlEvent):
        e.page.bottom_sheet = ft.BottomSheet(
            enable_drag=True,
            show_drag_handle=True,
            maintain_bottom_view_insets_padding=True,
            content=ft.Column(
                self.controls,
                spacing=0,
                scroll='hidden',
            )
        )

        e.page.bottom_sheet.open = True
        e.page.update()
