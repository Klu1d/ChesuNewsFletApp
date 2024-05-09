import copy
import flet as ft
from collections import OrderedDict
from datetime import datetime, timedelta

from firebase.pyrebase import PyrebaseWrapper
from ui.customs.cards import AnnounceCard


class AnnouncementsLists(ft.Container):
    def __init__(self, page: ft.Page, firebase: PyrebaseWrapper, my_events: bool = True):
        super().__init__()
        self.firebase = firebase
        self.redactor_annouces = False
        self.my_events = my_events
        self.collection = OrderedDict()

    def build(self):
        self.expand = True
        self.no_data_icon = ft.Container(
            visible=False,
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
                    ft.Text(value='Тут тишина...', size=18)
                ]
            )
        )
        
        self.content = ft.Stack(
            controls=[
                self.no_data_icon,
                ft.ListView(
                    spacing=0, padding=ft.padding.only(bottom=60),
                    #controls=self.collection.values()
                )
            ]
        )

    def stream_handler(self, stream_data):
        self.firebase.streams[stream_data.get('stream_id')].close
        if stream_data['data'] != None:
            if stream_data['event'] == 'put':
                keys = stream_data['data'].keys()
                for key in keys:
                    if not(self.my_events) and stream_data['data'][key]['author_id'] == self.firebase.uuid:
                        pass
                    else:
                        self.collection[stream_data['path'] + key] = \
                        AnnounceCard(**stream_data['data'][key], firebase=self.firebase)
                    
            elif stream_data['event'] == 'patch':
                if stream_data['path'] in self.collection:
                    for key, value in stream_data['data'].items():
                        setattr(self.collection[stream_data['path']], key, value)
                    args_with_values = {arg_name: getattr(self.collection[stream_data['path']], arg_name) 
                                        for arg_name in AnnounceCard.__init__.__code__.co_varnames[1:]}
                    self.collection[stream_data['path']] = \
                    AnnounceCard(**args_with_values)
                else:
                    if not(self.my_events) and stream_data['data']['author_id'] == self.firebase.uuid:
                        pass
                    else:
                        self.collection[stream_data['path']] = \
                        AnnounceCard(**stream_data['data'], firebase=self.firebase)
        else:
            if stream_data['path'] in self.collection:
                del self.collection[stream_data['path']]
            else:
                self.collection.clear()
                self.no_data_icon.visible = True
        


            
        if stream_data['stream_id'] == 'chesu':
            self.create_time_mark()
        else:
            self.sort_cards_time()

        self.no_data_icon.visible = not(bool(self.collection))

    async def time_over(self, card):
        self.firebase.time_over_announcement(**card._data_args())

    def sort_cards_time(self):
        cards = list(self.collection.values())
        cards.sort(key=lambda card: datetime.strptime(card.datetime, '%d.%m.%Y %H:%M'))
        self.content.controls[1].controls = cards

    def create_time_mark(self):
        cards = list(self.collection.values())
        cards.sort(key=lambda card: datetime.strptime(card.datetime, '%d.%m.%Y %H:%M'), reverse=True)
        current_time = datetime.now()
        previous_text, a = None,  0
        #controls = []

        for i, card in enumerate(copy.copy(cards)):
            if datetime.strptime(card.datetime, '%d.%m.%Y %H:%M') < current_time:
                self.page.run_task(self.time_over, cards.pop(i))

        for i, card in enumerate(copy.copy(cards)):
            text = self.custom_time(card.datetime)
            if previous_text != text:
                cards.insert(i+a,
                    ft.Container(
                        expand=True,
                        padding=ft.padding.only(24,0,0,5), 
                        content=ft.Text(value=text, size=23)
                    )           
                )
                previous_text = text
                a += 1
            
        self.content.controls[1].controls = cards 
        self.update()
    # def create_time_mark(self):
    #     current_time = datetime.now()
    #     previous_text, positon = None, 0
    #     cards = sorted(
    #         self.collection.values(),
    #         key=lambda card: datetime.strptime(card.datetime, '%d.%m.%Y %H:%M'),
    #         reverse=True
    #     )

    #     for i, card in reversed(list(enumerate(cards))):
    #         card_datetime = datetime.strptime(card.datetime, '%d.%m.%Y %H:%M')
    #         if card_datetime < current_time:
    #             self.page.run_task(self.time_over, card)
    #             cards.pop(i)
    #         else:
    #             text = self.custom_time(card.datetime)
    #             if previous_text != text:
    #                 cards.insert(i + positon,
    #                     ft.Container(
    #                         expand=True,
    #                         padding=ft.padding.only(24, 0, 0, 5),
    #                         content=ft.Text(value=text, size=23)
    #                     )           
    #                 )
    #                 previous_text = text
    #                 positon += 1
                
    #     self.content.controls[1].controls = cards 
    #     self.update()


    def custom_time(self, date_time_str):
        current_date = datetime.now().date()
        current_week = current_date.isocalendar()[1]
        current_year = current_date.year
        date_only = datetime.strptime(date_time_str, '%d.%m.%Y %H:%M').date()

        formatted_date = ''
        months_translation = {
            'January': 'Январь',
            'February': 'Февраль',
            'March': 'Март',
            'April': 'Апрель',
            'May': 'Май',
            'June': 'Июнь',
            'July': 'Июль',
            'August': 'Август',
            'September': 'Сентябрь',
            'October': 'Октябрь',
            'November': 'Ноябрь',
            'December': 'Декабрь'
        }
                
        if date_only == current_date:
            formatted_date = 'Сегодня'
        elif date_only == current_date + timedelta(days=1):
            formatted_date = "Завтра"
        elif date_only.isocalendar()[1] == current_week:
            formatted_date = "На этой неделе"
        elif date_only.isocalendar()[1] == current_week + 1:
            formatted_date = "На следующей неделе"
        elif date_only.month == current_date.month:
            formatted_date = 'Этот месяц'
        elif date_only.year == current_year:
            formatted_date = months_translation[date_only.strftime('%B')]
        else:
            formatted_date = months_translation[date_only.strftime('%B')]
            formatted_date += " " + date_only.strftime('%Y')

        return formatted_date.title()
    
    def on_click_go_announce(self, e):
        e.control.visible = False
        e.page.go('/announce')
        e.page.update()
