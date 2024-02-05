import flet as ft
from ui.controller.board import Board 
from ui.widgets.custom_bottom_sheet import CustomBottomSheet


class TabDisplay(ft.UserControl):
    def __init__(self, page, tab_name, firebase=None):
        super().__init__()
        self.page = page
        self.tab_name = tab_name
        self.firebase = firebase
        self.news_sheet = CustomBottomSheet(pyrebase=self.firebase)

    def build(self):
        self.empty = ft.Container(
            data='empty',
            alignment=ft.alignment.center,
            content=ft.Column(
                scroll=None,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                controls=[
                    ft.CircleAvatar(
                        radius=52.5,
                        bgcolor=ft.colors.with_opacity(0.3, ft.colors.GREY), 
                        content=ft.Icon(ft.icons.SPEAKER_NOTES_OFF_OUTLINED, size=50)
                    ),
                    ft.Text(value='В разделе пока тишина.', size=18)
                ]
            )
        )
        
        
        news = self.firebase.get_news(self.tab_name) if self.tab_name != 'Новости' else self.firebase.get_news()
        tab_content = ft.ListView(expand=True, controls=self.full_up_controls(news), spacing=10)
        return tab_content if tab_content.controls != [] else self.empty

        

    def full_up_controls(self, news_data):
        try:
            container = Board(self.page, self.firebase)
            
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
            print('tab_display: ', e)
            list_finish_bords = []
        finally:
            return list_finish_bords
    def time_sort(self, e):
        pass
                
