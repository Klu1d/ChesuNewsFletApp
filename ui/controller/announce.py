import copy
import uuid
import datetime
import flet as ft
from collections import OrderedDict
from typing import Any, List, Optional, Tuple



class CreateAnnounceCard(ft.UserControl):
    def __init__(self, create_button, cancel_button):
        super().__init__()
        self.headline = None
        self.text = None
        self.datetime = None
        self.place = None
        self.image = None
        self.role = None
        self.username = None 
        self.status = 'local'
        
        self.create_button = create_button
        self.cancel_button = cancel_button
        self.datetime_button = ft.OutlinedButton(
            height=26,
            text=self.datetime,
            style=ft.ButtonStyle(padding=5, color='onbackground', bgcolor='transparent',
                shape=ft.RoundedRectangleBorder(radius=5), side=ft.BorderSide(2, color='#879aa8')),
            on_click=self.on_click_datetime
        )
        self.faculties = ['АТИ', 'БХФ', 'ИМФИТ', 'ИСТФАК', 'ИЭФ', 'Мед Институт', 'ФГИГ', 'ФГУ', 'ФИЛФАК', 'ФИЯ', 'ЮРФАК']
        
    def on_change_headline(self, e):
        self.headline = e.control.value
        self.empty_fields()
        
    def on_change_text(self, e):
        self.text = e.control.value
        self.empty_fields()
        
    def on_change_place(self, e):
        self.place = e.control.value
        self.empty_fields()
        
    def on_change_image(self, e):
        self.image = e.control.value
        self.empty_fields()
        
    def build(self):
        self.faculties_dropdown = ft.Dropdown(
            value=self.place,
            dense=True, 
            width=140,
            content_padding=5,
            border_width=2,
            on_change=self.on_change_place,
            options=[ft.dropdown.Option(faculty) for faculty in self.faculties]
        )
        
        self.clear_button = ft.IconButton(
            height=35,
            width=45,
            on_click=self.on_click_clear,
            icon=ft.icons.CLEAR,
            icon_color='onbackground',
            style=ft.ButtonStyle(color='onbackground', padding=0, bgcolor=ft.colors.INVERSE_PRIMARY, shape=ft.RoundedRectangleBorder(radius=15)),
        ) 

        self.file_picker = ft.FilePicker()
        self.date_picker = ft.DatePicker(
            confirm_text='Выбрать',
            cancel_text='Отменить',
            error_format_text='Неправильный формат даты',
            error_invalid_text=' ',
            help_text='Укажите дату',
            on_change=self.on_change_date_picker,
            on_dismiss=self.on_dismissed,
            first_date=datetime.datetime.now(),
            last_date=datetime.datetime(2024, 12, 1),
        )
        self.time_picker = ft.TimePicker(
            confirm_text='Выбрать',
            cancel_text='Отменить',
            error_invalid_text=' ',
            help_text='Выберите время',
            hour_label_text='Часы',
            minute_label_text='Минуты',
            on_change=self.on_change_time_picker,
            on_dismiss=self.on_dismissed,
        )
        
        self.headline_field = ft.TextField(
            value=self.headline,
            hint_text='Заголовок', 
            dense=True, 
            content_padding=5, 
            text_size=21,
            border_width=2,
            on_change=self.on_change_headline,
            capitalization=ft.TextCapitalization.SENTENCES,
            text_style=ft.TextStyle(font_family='Spaceland', size=20)
        )
        self.textline_field = ft.TextField(
            value=self.text,
            hint_text='Основной текст', 
            content_padding=ft.padding.symmetric(8,10),
            multiline=True,
            expand=True,
            min_lines=50,
            max_lines=50,
            border_width=2,
            text_size=18,
            capitalization=ft.TextCapitalization.SENTENCES,
            on_change=self.on_change_text
        )
        self.image_field = ft.Container(
            padding=0, margin=0,
            height=100, border=ft.border.all(5, 'grey'),
            border_radius=ft.border_radius.only(15,15,0,0), 
            alignment=ft.alignment.center,
            on_click=self.on_click_add_photo,
            content=ft.CircleAvatar(
                data='notimage',
                radius=36.5,
                bgcolor=ft.colors.with_opacity(0.3, 'grey'), 
                content=ft.Icon(ft.icons.ADD_PHOTO_ALTERNATE_OUTLINED, size=25, color='grey')
            )
        )
        
        self.create_announce_card = ft.Container(
            bgcolor=ft.colors.TERTIARY_CONTAINER, 
            border_radius=ft.border_radius.only(15,15,15,15), 
            alignment=ft.alignment.top_left,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    self.image_field,
                    ft.Container(
                        expand=True,
                        padding=ft.padding.only(10,10,10,5),
                        border_radius=ft.border_radius.only(0,0,15,15), 
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                self.headline_field,
                                self.textline_field,
                                ft.ListTile(dense=True,
                                    content_padding=0,
                                    leading=ft.Column([ft.Text('Место:', size=16), self.faculties_dropdown], spacing=0),
                                    trailing=ft.Column([ft.Text('Дата:', size=16), self.datetime_button], spacing=0),
                                ),
                                ft.Container(
                                    padding=ft.padding.only(0,10,0,0),
                                    margin=ft.margin.only(0,5,0,0),
                                    content=ft.Row(spacing=0, alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Row([self.clear_button], spacing=5), 
                                            ft.Row(
                                                spacing=5,
                                                controls=[
                                                    self.cancel_button,
                                                    self.create_button,
                                                ]
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )
        self.finish = ft.Container(content=self.create_announce_card, expand=True, height=600)
        return self.finish
    
    def empty_fields(self):
        self.create_button.disabled = False
        for value in [self.headline, self.text, self.place, self.datetime_button.text]:
            if value is None:
                self.create_button.disabled = True
                break
            elif not value.split():
                self.create_button.disabled = True
                break
        self.create_button.update()
        
    """Кнопки для редактирования"""
    def on_click_add_photo(self, e: ft.ControlEvent):
        print('выбери фото')
    
    def on_click_clear(self, e: ft.ControlEvent):
        self.headline_field.value = None
        self.textline_field.value = None
        self.faculties_dropdown.value = None
        self.datetime_button.text = None
        self.image_field
        self.create_button.disabled = True
        
        self.finish.update() 
    
    """Управление временем"""
    def on_dismissed(self, e: ft.ControlEvent):
        self.datetime_button.text = self.datetime
    
    def on_click_datetime(self, e: ft.ControlEvent):
        e.page.overlay.clear()
        e.page.overlay.append(self.date_picker)
        e.page.update()
        self.date_picker.pick_date()
        
    def on_change_date_picker(self, e: ft.ControlEvent):
        self.dismiss = self.datetime_button.text
        self.datetime_button.text = datetime.datetime.strftime(e.control.value, '%d.%m.%Y')
        e.page.overlay.append(self.time_picker)
        e.page.update()
        self.time_picker.pick_time()
        
    def on_change_time_picker(self, e: ft.ControlEvent):
        self.datetime_button.text += e.control.value.strftime(' %H:%M')
        self.datetime = self.datetime_button.text
        self.empty_fields()
        self.datetime_button.update()

class AnnounceCard(ft.UserControl):
    def __init__(self,
            id: str,
            status: str,
            headline: str, 
            text: str, 
            datetime: str, 
            place: str,  
            role: str,
            username: str,
            image: str = None,
            bgcolor: str = ft.colors.TERTIARY_CONTAINER,
            margin: int = None,
            options_visible: bool = True,
            maintain_state: bool = False,
            status_label: ft.Control = None,
            leading_button: ft.Control = None,
            trailing_button: ft.Control = None,
            title_button: ft.Control = None,
            on_click_change: Any = None,
            on_click_delete: Any = None,
            
        ):
        super().__init__()
        self.id = id
        self.status = status
        self.image = image
        self.headline = headline
        self.text = text
        self.role = role
        self.username = username
        self.place = place
        self.datetime = datetime
        self.options_visible = options_visible
        self.maintain_state = maintain_state
        self.status_label = status_label
        self.bgcolor = bgcolor
        self.margin = margin
        self.trailing_button = trailing_button
        self.title_button = title_button
        self.leading_button = leading_button 
        self.on_click_change = on_click_change
        self.on_click_delete = on_click_delete
       
        self.faculties = ['АТИ', 'БХФ', 'ИМФИТ', 'ИСТФАК', 'ИЭФ', 'Мед Институт', 'ФГИГ', 'ФГУ', 'ФИЛФАК', 'ФИЯ', 'ЮРФАК']
        self.faculties_more = [
            'Агротехнологический институт', 
            'Биолого-химический факультет', 
            'Институт математики, физики и информационных технологий', 
            'Исторический факультет', 
            'Институт экономики и финансов', 
            'Медицинский институт', 
            'Факультет географии и геоэкологии', 
            'Факультет государственного управления', 
            'Филологический факультет', 
            'Факультет иностранных языков', 
            'Юридический факультет'
        ]

    def build(self):
        self.card_menu = ''
        self.card_text_container = ft.Container(
            padding=ft.padding.symmetric(0,5),
            alignment=ft.alignment.center_left,
            content=ft.Text(
                size=18,
                value=self.text, 
                style=ft.TextStyle(height=1), 
            ), 
        )
        self.card_footer = ft.ListTile(
            content_padding=0,
            dense=True,
            visible=True,#False if all(value == None for value in [self.leading_button, self.title_button, self.trailing_button]) else 
            leading=self.leading_button,
            title=self.title_button,
            trailing=self.trailing_button,
        )

        
        self.card_expansion_tile =  ft.ExpansionTile(
            shape=ft.RoundedRectangleBorder(radius=1),
            affinity=ft.TileAffinity.PLATFORM,
            maintain_state=self.maintain_state,
            initially_expanded=True,
            controls_padding=0,
            title=ft.Text(value=self.headline, font_family='Spaceland', size=22),
            subtitle=ft.Container(
                ft.Row(
                    controls=[
                        ft.Text(value=self.datetime, opacity=0.7), 
                        ft.Container(
                            padding=0,
                            border_radius=10,
                            content = self.status_label
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN), 
                padding=0
            ),
            tile_padding=0,
            controls=[
                self.card_text_container,
                ft.ListTile(
                    dense=True, 
                    content_padding=5,
                    leading=ft.Column(
                        spacing=0,
                        controls=[
                            ft.Text('Место:', size=14), 
                            ft.Container(
                                padding=0,
                                width=100,
                                on_click=self.on_click_more_info,
                                content=ft.Row(
                                    spacing=3,
                                    controls=[
                                        ft.Icon(ft.icons.INFO_OUTLINE_ROUNDED, color='grey', size=15), 
                                        ft.Text(value=self.place, tooltip=self.faculties_more[5])
                                    ]
                                ), 
                            )
                        ], 
                    ),
                    trailing=ft.Column([ft.Text(value=self.role+":", size=14), ft.Text(value=self.username)], spacing=0),
                ),          
            ],
        )
        

        
        self.options = ft.PopupMenuButton(
            data=self.id,
            icon=ft.icons.MORE_HORIZ_OUTLINED,
            visible=self.options_visible,
			items=[
				ft.PopupMenuItem(text="Изменить", on_click=self.on_click_change, data=self.id ),
				ft.PopupMenuItem(text="Удалить", data=self.id, on_click=self.on_click_delete),
			]
    	)
        
        
        self.card = ft.Container(
            border_radius=15,
            bgcolor=self.bgcolor,
            margin=self.margin,
            border=ft.border.all(1, "secondary, 0.2"),
            content=ft.Stack(
				controls=[
					ft.Container(
                        margin=0,
						padding=ft.padding.symmetric(0,10),
						content=ft.Column(
							spacing=0,
							controls=[
								ft.SelectionArea(self.card_expansion_tile),
								self.card_footer
							]
						),
					),
					ft.Row([self.options], alignment=ft.MainAxisAlignment.END)
				]
			)
        )
        
        return self.card

    def on_click_more_info(self, e):
        self.page.overlay.append(
            ft.AlertDialog(
                open=True,
                content=ft.Text(self.faculties_more[5])
            )
        )
