import flet as ft
from ui.controller.board import Board 
from ui.widgets.custom_bottom_sheet import CustomBottomSheet


class TabDisplay(ft.UserControl):
    def __init__(self, page, tab_name, myPyrebase=None):
        super().__init__()
        self.page = page
        self.tab_name = tab_name
        self.myPyrebase = myPyrebase
        self.news_sheet = CustomBottomSheet(pyrebase=self.myPyrebase)

    def build(self):
        self.empty = ft.Container(
            data="empty",
            height=400,
            opacity=0.6,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        bgcolor=ft.colors.SECONDARY_CONTAINER,
                        border_radius=15,
                        height=100,
                        padding=10,
                        alignment=ft.alignment.center,
                        content=ft.Row(
                            controls=[
                                ft.Icon(opacity=0.9, name=ft.icons.SPEAKER_NOTES_OFF_ROUNDED, size=80),
                                ft.Text(opacity=0.9, value="Новостей пока нет", size=20, weight=ft.FontWeight.W_600 ),
                            ]
                        )
                    )
                ]
            )
        )
        
        news = self.myPyrebase.get_news(self.tab_name) if self.tab_name != "Новости" else self.myPyrebase.get_news()
        return ft.ListView(expand=True, controls=self.full_up_controls(news), spacing=10)


        

    def full_up_controls(self, news_data):
        try:
            container = Board(self.page, pyrebase=self.myPyrebase)
            
            list_finish_bords = []
            for i in range(len(news_data)):
                if i == 0:
                    list_finish_bords.append(
                        container.new(
                            number=news_data[i]['id'],
                            headline=news_data[i]['headline'],
                            image=news_data[i]['images'][0],
                            time=news_data[i]['datetime'], #22.11.2023 12:00
                        ),
                    )
                else:
                    list_finish_bords.append(
                        container.old(
                            number=news_data[i]['id'],
                            headline=news_data[i]['headline'],
                            image=news_data[i]['images'][0],
                            time=news_data[i]['datetime'], #22.11.2023 12:00
                        )
                    )
        except Exception as e:
            print(e)
            list_finish_bords = [self.empty]
        finally:
            return list_finish_bords
    def time_sort(self, e):
        pass
                
