import copy
import flet as ft
from datetime import datetime, timedelta

from firebase.pyrebase import PyrebaseWrapper
from ui.customs.cards import OldCard, NewCard
from ui.customs.announcements_lists import AnnouncementsLists


class NewsLists(AnnouncementsLists):
    def __init__(self, page: ft.Page, firebase: PyrebaseWrapper, tab_name: str, stream_data = None):
        super().__init__(firebase, stream_data)
        self.page = page
        self.stream_data = stream_data
        self.firebase = firebase
        self.news_data = firebase.get_news() if tab_name == 'Новости' else firebase.get_news(tab_name)
        self.tab_name = tab_name

    def did_mount(self):
        self.running = True
        self.page.run_thread(self.news_build)
        #self.page.run_task(self.news_build)

    def will_unmount(self):
        self.running = False

    def news_build(self):
        self.data = 'news'
        self.news_data.sort(key=lambda x: datetime.strptime(x.get('datetime', '01.01.1900 00:00'), '%d.%m.%Y %H:%M'), reverse=True)
        self.show_more = ft.Container(
            data='show_more',
            height=40, key=0,
            border_radius=10,
            margin=ft.margin.only(top=5, bottom=10, left=15, right=15),
            on_click=self.on_click_show_more,
            alignment=ft.alignment.center,
            content=ft.Text('Показать еще', size=16),
            gradient=ft.SweepGradient(
                center=ft.alignment.bottom_right,
                colors=[ft.colors.ON_SECONDARY, ft.colors.SECONDARY]
            )
        )
        self.news_lists = [
            NewCard(
                page=self.page,
                firebase=self.firebase,
                number=self.news_data[i]['id'],
                headline=self.news_data[i]['headline'],
                image=self.news_data[i]['images'][0],
                datetime=self.news_data[i]['datetime'],
            ) if i == 0 else  OldCard(
                page=self.page,
                firebase=self.firebase,
                number=self.news_data[i]['id'],
                headline=self.news_data[i]['headline'],
                image=self.news_data[i]['images'][0],
                datetime=self.news_data[i]['datetime'], #22.11.2023 12:00
            )
            for i in range(len(self.news_data))
        ]
        
        self.news_lists = self.create_time_mark_news(self.news_lists) 
        self.chunks_dict = {
            i // 16: self.news_lists[i:i + 16] \
            for i in range(0, len(self.news_lists), 16)
        }
        if len(self.chunks_dict) > 1:
            self.chunks_dict[0].append(self.show_more)
        self.content = ft.Container(
            content=ft.ListView(self.chunks_dict[0], spacing=0, padding=ft.padding.only(bottom=60)))

        self.update()
    
    def on_click_show_more(self, e):
        del self.content.content.controls[-1]
        e.control.key = e.control.key + 1 
        if e.control.key in self.chunks_dict:
            self.content.content.controls.extend(self.chunks_dict[e.control.key])
            self.content.content.controls.append(self.show_more)
        
        self.update()

    def create_time_mark_news(self, list_controls):
        prev_month = None 
        for i, container in enumerate(list_controls):
            if container.data == 'card':
                current_month = datetime.strptime(container.datetime, '%d.%m.%Y %H:%M').month
                if current_month != prev_month:
                    list_controls.insert(i,
                        ft.Container(
                            expand=True, data='time_mark',
                            padding=ft.padding.only(24,0,0,5),  
                            content=ft.Text(self.custom_time(list_controls[i].datetime), size=23)
                        )
                    )
                prev_month = current_month
        return list_controls