import locale
import flet as ft
from datetime import datetime

from ui.controller.board import Board 
from ui.widgets.custom_bottom_sheet import CustomBottomSheet


class TabDisplay(ft.UserControl):
    def __init__(self, page, tab_name, firebase=None):
        super().__init__()
        self.page = page
        self.tab_name = tab_name
        self.firebase = firebase
        self.tab_content = ft.ListView(expand=True, padding=ft.padding.only(bottom=10), spacing=10)
        self.empty_icon_visible = True
        self.news_sheet = CustomBottomSheet(self.firebase)
        

    def build(self):
        self.show_more = ft.Container(
            data='show_more',
            padding=ft.padding.symmetric(horizontal=15),
            margin=ft.margin.only(top=10),
            content=ft.FilledButton(
                'Показать еще',
                height=40,
                on_click=self.on_click_show_more,
                style=ft.ButtonStyle(
                    color=ft.colors.SECONDARY_CONTAINER,
                    shape=ft.RoundedRectangleBorder(radius=10),
                    overlay_color=ft.colors.SECONDARY,
                ),
            )
        )
        self.empty = ft.Container(
            visible=self.empty_icon_visible,
            alignment=ft.alignment.center,
            content=ft.Column(
                scroll=None,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                controls=[
                    ft.CircleAvatar(
                        radius=47.5,
                        bgcolor=ft.colors.with_opacity(0.3, ft.colors.GREY), 
                        content=ft.Icon(ft.icons.SPEAKER_NOTES_OFF_OUTLINED, size=45)
                    ),
                    ft.Text(value='В разделе пока тишина.', size=18)
                ]
            )
        )     
        
        news = self.firebase.get_news(self.tab_name) if self.tab_name != 'Новости' else self.firebase.get_news() 
        self.list_news = self.create_board_news(news)
        self.part_list = ''
        
        if self.list_news != None and len(self.list_news) > 25:
            self.part_list = self.list_news[:25] if self.list_news != None else []
            self.part_list.append(self.show_more)
        else:
            self.part_list = self.list_news if self.list_news != None else []
        
        self.tab_content.controls=self.part_list
        return self.tab_content if self.tab_content.controls != [] else self.empty

    def on_click_show_more(self, e):
        count = len(self.tab_content.controls)
        for i, item in enumerate(self.tab_content.controls):
            if item.data == 'show_more':
                del self.tab_content.controls[i]
                break
        
        more_news = self.list_news[count:][:25]

        self.tab_content.controls.extend(more_news)
        self.tab_content.scroll_to(key=more_news[0].key, duration=650)
        if len(self.tab_content.controls) != len(self.list_news)-1:
            self.tab_content.controls.append(self.show_more)
        
        self.tab_content.update()

    def create_board_news(self, news_data):
        try:
            container = Board(self.page, self.firebase)
            list_controls = [container.new(
                    number=news_data[0]['id'],
                    headline=news_data[0]['headline'],
                    image=news_data[0]['images'][0],
                    time=news_data[0]['datetime'],
                )
            ]
            for i in range(1, len(news_data)):
                list_controls.append(
                    container.old(

                        number=news_data[i]['id'],
                        headline=news_data[i]['headline'],
                        image=news_data[i]['images'][0],
                        time=news_data[i]['datetime'], #22.11.2023 12:00
                    )
                )
          
            list_controls.sort(key=lambda x: datetime.strptime(x.data, '%d.%m.%Y %H:%M'), reverse=True)
            return self.create_time_mark(list_controls)
        except Exception as e:
            print(e)
 
    def create_time_mark(self, list_controls):
        prev_month = None 
        for i, container in enumerate(list_controls):
            current_month = datetime.strptime(container.data, '%d.%m.%Y %H:%M').month
            if prev_month is not None and current_month != prev_month:
                list_controls.insert(i,
                    ft.Container(
                        data='datetime',
                        expand=True, 
                        margin=ft.margin.only(top=0),
                        padding=ft.padding.only(left=24), height=28, 
                        content=ft.Text(self.custom_time(list_controls[i].data), size=22)
                    )
                )
            prev_month = current_month
        
        return list_controls 
        
    def custom_time(self, time):
        current_locale = locale.getlocale()
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

        date_string = time.split()[0]
        date_object = datetime.strptime(date_string, '%d.%m.%Y')

        current_date = datetime.now()
        
        formatted_date = ''
        if current_date.month == date_object.month:
            formatted_date = 'За этот месяц'
        elif current_date.year == date_object.year:
            formatted_date = date_object.strftime('%B') 
        else:
            formatted_date = date_object.strftime('%B %Y') 
            
        formatted_date = formatted_date.replace(date_object.strftime('%B'), date_object.strftime('%B')[:-1] + 'ь')
        locale.setlocale(locale.LC_TIME, current_locale)
        
        return formatted_date.title()
