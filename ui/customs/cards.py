import datetime
import flet as ft

from datetime import date, timedelta

from firebase.pyrebase import PyrebaseWrapper, Status
from ui.customs.news_article import NewsArticle

class NewCard(ft.GestureDetector):
    def __init__(self, 
            page: ft.Page, 
            firebase: PyrebaseWrapper,
            number: int,
            image: str,
            headline: str, 
            datetime: str,
        ):
        super().__init__()
        self.page = page
        self.firebase = firebase
        self.number = number
        self.image = image
        self.headline = headline
        self.datetime = datetime
        self.height=220
        self.alignment=ft.alignment.center_left
        self.animate_size=ft.animation.Animation(150)
        self.on_tap_up = self.on_click_card
        self.data = 'card'

    def did_mount(self):
        self.page.run_task(self.stack_build)

    async def stack_build(self):
        self.image_container = ft.ShaderMask(
            border_radius=15,
            content=ft.Image(
                src=self.image,
                fit=ft.ImageFit.COVER,
                width=2000,
                height=220,
            ),
            shader=ft.LinearGradient(
                stops=[0.2, 1],
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.WHITE, ft.colors.BLACK],
            ),
        )
        self.content=ft.Container(
            border_radius=15, ink=True,
            margin = ft.margin.only(left=15, top=0, right=15, bottom=10),
            padding=5,
            #bgcolor="secondarycontainer, 0.8",
            #border=ft.border.all(1, "onsecondarycontainer, 0.2"),
            bgcolor="secondarycontainer, 0.4",
            #border=ft.border.all(1, "onsecondarycontainer, 0.2"),
            content=ft.Stack(
                controls=[
                    self.image_container,
                    ft.Container(
                        alignment=ft.alignment.Alignment(-1, 0.6),
                        padding=20,
                        content=ft.Text(
                            value=self.headline,
                            text_align=ft.TextAlign.LEFT,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            weight=ft.FontWeight.BOLD,
                            font_family='Headline',
                            color='white', 
                            max_lines=3,
                            size=20,
                        ),
                    ),
                    ft.Container(
                        alignment=ft.alignment.bottom_left,
                        padding=20,
                        content=ft.Text(
                            value=self.time_display(self.datetime),
                            text_align=ft.TextAlign.LEFT,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            color='grey',
                            max_lines=3,
                            size=12, 
                        ),
                    )
                ]
            ),
        )
        self.update()
    
    def on_click_card(self, e: ft.ControlEvent):
        e.page.bottom_sheet = ft.BottomSheet(
            dismissible=True,
            enable_drag=True,
            use_safe_area=True,
            is_scroll_controlled=True,
            maintain_bottom_view_insets_padding=True,
            content=ft.Container(
                content=ft.ProgressRing(), 
                height=self.page.height - self.page.height * 16 / 100, 
                alignment=ft.alignment.center, 
            ),
            open=True,
        )
        e.page.update()
        e.page.bottom_sheet.content = NewsArticle(self.number, self.firebase)
        if self.page.client_storage.get('role'):
            if self.number in self.page.client_storage.get('bookmarks'):
                e.page.bottom_sheet.content.icon_bookmark_visible = True
            else:
                e.page.bottom_sheet.content.icon_bookmark_visible = False
        e.page.update()

    def time_display(self, input_date: str):
        today = date.today().strftime('%d-%m-%Y')
        yesterday = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
        
        if input_date.split(' ')[0] == today:
            return f"Сегодня в {input_date.split(' ')[1]}"
        elif input_date.split(' ')[0] == yesterday:
            return f"Вчера {input_date.split(' ')[1]}"
        else:
            return input_date

class OldCard(NewCard):
    def __init__(self, 
            page: ft.Page, 
            firebase: PyrebaseWrapper,
            number: int,
            image: str,
            headline: str, 
            datetime: str,
        ):
        super().__init__(page, firebase, number, image, headline, datetime,)
        self.page = page
        self.firebase = firebase
        self.number = number
        self.image = image
        self.headline = headline
        self.datetime = datetime
        self.height = 100

    def did_mount(self):
        self.page.run_task(self.stack_build)

    async def stack_build(self):
        self.content=ft.Container(
            padding=5, border_radius=15, ink=True,
            margin = ft.margin.only(left=15, top=0, right=15, bottom=10),
            bgcolor="secondarycontainer, 0.4",
            # bgcolor="secondarycontainer, 0.8",
            # border=ft.border.all(1, "onsecondarycontainer, 0.2"),
            content=ft.Row(
                controls=[
                    ft.Image(
                        border_radius=15,
                        fit=ft.ImageFit.COVER,
                        src=self.image,
                        height=100,
                        width=100,
                        expand=1,
                    ),
                    ft.Container(
                        margin=5,
                        expand=2,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=0,
                            controls=[
                                ft.Text(
                                    max_lines=3,
                                    weight=ft.FontWeight.W_600,
                                    text_align=ft.TextAlign.LEFT,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                    value=self.headline, 
                                ),
                                ft.Text(max_lines=1, value=self.time_display(self.datetime), color="grey"),
                            ]
                        )
                    )
                ]
            )
        )
        self.update()
    
class CreateAnnounceCard(ft.BottomSheet):
    def __init__(self, page, firebase):
        super().__init__()
        self.page = page
        self.firebase = firebase
        self.announce_id = None,
        self.headline = None
        self.text = None
        self.datetime = None
        self.place = None
        self.image = None
        self.role = None
        self.author = None 
        self.status = 'local'
        self.on_click_create = None
        self.is_scroll_controlled = True
        self.enable_drag = True
        self.faculties = ['АТИ', 'БХФ', 'ИМФИТ', 'ИСТФАК', 'ИЭФ', 'Мед Институт', 'ФГИГ', 'ФГУ', 'ФИЛФАК', 'ФИЯ', 'ЮРФАК']
        
        self.image_disabled = False
        self.place_disabled = False
        self.text_disabled = False
        self.headline_disabled = False
        self.datetime_disable = False
    
    def did_mount(self):
        self.open = True
        self.page.run_task(self.stack_build)

    def will_unmount(self):
        self.open = False

    async def stack_build(self):
        
        self.faculties_dropdown = ft.Dropdown(
            value=self.place,
            disabled=self.place_disabled,
            dense=True, 
            width=140,
            content_padding=5,
            border_width=2,
            on_change=self.on_change_place,
            options=[ft.dropdown.Option(faculty) for faculty in self.faculties]
        )
        
        self.clear_button = ft.TextButton(
            text='Очистить',
            on_click=self.on_click_clear,
        ) 
        self.datetime_button = ft.OutlinedButton(
            height=26,
            text=self.datetime,
            disabled=self.datetime_disable,
            style=ft.ButtonStyle(padding=5, color='onbackground', bgcolor='transparent',
                shape=ft.RoundedRectangleBorder(radius=5), side=ft.BorderSide(2, color='#879aa8')),
            on_click=self.on_click_datetime
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
            time_picker_entry_mode=ft.TimePickerEntryMode.INPUT,
            on_change=self.on_change_time_picker,
            on_dismiss=self.on_dismissed,
        )
        
        self.headline_field = ft.TextField(
            value=self.headline,
            disabled=self.headline_disabled,
            hint_text='Заголовок', 
            dense=True, 
            content_padding=5, 
            text_size=21,
            border_width=2,
            on_change=self.on_change_headline,
            capitalization=ft.TextCapitalization.SENTENCES,
            text_style=ft.TextStyle(font_family='Headline', size=20)
        )
        self.textline_field = ft.TextField(
            value=self.text,
            disabled=self.text_disabled,
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
            disabled=self.image_disabled,
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
        self.create_button = ft.TextButton(self.data, disabled=True, on_click=self.on_click_create)
        self.cancel_button = ft.TextButton('Отменить', on_click=self.on_click_cancel)
        
        self.content = ft.Container(
            expand=True,
            height=self.page.height - self.page.height * 15 / 100,
            bgcolor = "secondarycontainer, 0.8",
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
                                    margin=ft.margin.only(0,20,5,0),
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
       
        
        self.update()

    def on_click_cancel(self, e):
        self.open = False
        self.update()

    def on_click_create_announce_card(self, e):
        self.page.bottom_sheet.open = False
        self.page.update()
        
        self.firebase.create_announcement(
            announce_id=self.announce_id,
            headline=self.headline,
            text=self.text,
            place=self.place,
            datetime=self.datetime,
            role=self.role,
            username=self.author,
            image=self.image,
            status=self.status,
        )

    def empty_fields(self):
        self.create_button.disabled = False
        self.create_button.style=ft.ButtonStyle(color='onbackground', bgcolor=ft.colors.INVERSE_PRIMARY, shape=ft.RoundedRectangleBorder(radius=15))
        for value in [self.headline, self.text, self.place, self.datetime_button.text]:
            if value is None:
                self.create_button.disabled = True
                self.create_button.style=None
                break
            elif not value.split():
                self.create_button.disabled = True
                self.create_button.style=None
                break
        self.create_button.update()
    
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
        
        self.update() 
    
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

class AnnounceCard(ft.Container):
    def __init__(self,
            announce_id: str,
            status: str,
            headline: str, 
            text: str, 
            datetime: str, 
            place: str,  
            role: str,
            author: str,
            firebase: PyrebaseWrapper,
            author_id = None,
            subscribers = {},
            image: str = None,
            reason: str = None,
        ):
        super().__init__()
        self.firebase = firebase
        self.author = author
        self.author_id = author_id
        self.announce_id = announce_id
        self.status = status
        self.subscribers = subscribers if isinstance(subscribers, dict) else {}
        self.image = image
        self.headline = headline
        self.text = text
        self.role = role
        self.place = place
        self.datetime = datetime
        self.reason = reason

        self.count_subs = len(self.subscribers) 
        self.padding=ft.padding.only(10,0,10,10)
        self.bgcolor = "secondarycontainer, 0.4"
        self.border_radius = 15
        self.margin = ft.margin.only(left=15, top=0, right=15, bottom=10)
        #self.border=ft.border.all(1, "secondary, 0.1")
        self.offset=ft.transform.Offset(0, 0)
        self.animate_offset=ft.animation.Animation(500, ft.AnimationCurve.DECELERATE)
        self.animate_size = ft.animation.Animation(500, ft.AnimationCurve.DECELERATE)
        self.animate_opacity=ft.animation.Animation(500, ft.AnimationCurve.DECELERATE)
        self.status_label: ft.Control = None
        self.footer = ft.Container(height=0, padding=0)
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

    def _data_args(self):
        args_with_values = {arg_name: getattr(self, arg_name) \
        for arg_name in AnnounceCard.__init__.__code__.co_varnames[1:] \
        if arg_name != 'firebase'}

        return args_with_values
    
    def build(self):
        self.send_reason = ft.TextButton('Отправить', 
            height=40,
            disabled=True,
            on_click=self.on_click_rejected,
            style= ft.ButtonStyle(
                color={
                    ft.MaterialState.DEFAULT: 'onbackground',
                    ft.MaterialState.DISABLED: ft.colors.SECONDARY,
                }, 
                bgcolor={
                    ft.MaterialState.DEFAULT: ft.colors.INVERSE_PRIMARY,
                    ft.MaterialState.DISABLED: ft.colors.TRANSPARENT,
                },
                shape=ft.RoundedRectangleBorder(radius=10)
            )
        )
        self.choice_reason = ft.RadioGroup(
            on_change=self.on_change_choice_reason,
            content=ft.Column(
                controls=[
                    ft.Radio(value="Публикация карточки отклоняется из-за недостаточного объема данных или информации для адекватного представления.", label="Недостаточно информации"),
                    ft.Radio(value="Содержание карточки содержит неприемлемый или оскорбительный материал", label="Нецензурное содержимое"),
                    ft.Radio(value="Содержание карточки содержит рекламу или пропаганду, которая не соответствует правилам и политикам публикации", label="Неприемлемый рекламный материал"),
                    ft.Radio(value="Карточка отклоняется из-за указания неправильной даты публикации или проведения мероприятия в указанный день", label="Неправильная дата"),
                ]
            )
        )
        
        self.reason_input_field = ft.TextField( 
            content_padding=5, 
            text_size=16,
            border_width=2,
            border_radius=10,
            multiline=True,
            capitalization=ft.TextCapitalization.SENTENCES,
            on_change=self.on_change_reason_input,
            keyboard_type=ft.KeyboardType.TEXT,
        )
        self.reason_bottom_sheet = ft.BottomSheet(
            is_scroll_controlled=True,
            enable_drag=True,
            maintain_bottom_view_insets_padding=True,
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    scroll='hidden',
                    controls=[
                        ft.Text('Расскажите, в чем причина?', text_align=ft.TextAlign.START, weight=ft.FontWeight.BOLD, size=25),
                        self.reason_input_field,
                        ft.ResponsiveRow(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                self.choice_reason,
                                self.send_reason,
                            ]
                        )
                    ]
                )
            )
        )

        self.content = ft.Container(
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.ExpansionTile(
                        shape=ft.RoundedRectangleBorder(radius=1),
                        affinity=ft.TileAffinity.PLATFORM,
                        initially_expanded=True,
                        maintain_state=True,
                        controls_padding=0,
                        title=ft.Text(value=self.headline, font_family='Headline', size=22),
                        subtitle=ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Text(value=self.datetime, opacity=0.7), 
                                    ft.Container(
                                        padding=0,
                                        border_radius=10,
                                        content=self.status_label
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN), 
                            padding=0
                        ),
                        tile_padding=0,
                        controls=[
                            ft.Container(
                                padding=ft.padding.symmetric(0,5),
                                alignment=ft.alignment.center_left,
                                content=ft.Text(
                                    size=18,
                                    value=self.text, 
                                    style=ft.TextStyle(height=1), 
                                ), 
                            ),
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
                                            content=ft.Row(
                                                spacing=3,
                                                controls=[
                                                    ft.Icon(ft.icons.INFO_OUTLINE_ROUNDED, color='grey', size=15), 
                                                    ft.Text(value=self.place)
                                                ]
                                            ), 
                                        )
                                    ], 
                                ),
                                trailing=ft.Column([ft.Text(value=self.role+":", size=14), ft.Text(value=self.author)], spacing=0),
                            ),
                        ],
                    ),
                    self.buttons_control()
                ]
            )
        )

    def buttons_control(self):
        match self.status:
            case Status.PUBLISHED:
                return ft.Row(
                    spacing=0,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Container(
                            margin=ft.margin.only(0,0,0,0),
                            content=ft.Row(
                                spacing=2,
                                controls=[
                                    ft.Text(self.count_subs, color='grey'),
                                    ft.Icon('group', color='grey')
                                ]
                            )
                        ),
                        ft.TextButton('Отписаться', 
                            height=40,
                            on_click=self.on_click_leave,
                            style=ft.ButtonStyle(
                                color='onbackground', 
                                bgcolor=ft.colors.INVERSE_PRIMARY, 
                                shape=ft.RoundedRectangleBorder(radius=10)
                            )
                        )if self.subscribers.get(self.firebase.uuid, False) else ft.TextButton('Участвовать', 
                            height=40,
                            on_click=self.on_click_join,
                            style=ft.ButtonStyle(
                                color='onbackground', 
                                bgcolor=ft.colors.INVERSE_PRIMARY, 
                                shape=ft.RoundedRectangleBorder(radius=10)
                            )
                        )
                    ]
                )
            case Status.APPROVED:
                return ft.Row(
                    spacing=0,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            spacing=5,
                            controls=[
                                ft.IconButton(
                                    icon='group',
                                    on_click=self.on_click_attendees,
                                    style=ft.ButtonStyle(
                                        color='onbackground', 
                                        bgcolor=ft.colors.ON_INVERSE_SURFACE, 
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    )
                                ),
                                ft.IconButton(
                                    icon='edit',
                                    on_click=self.on_click_edit_time,
                                    style=ft.ButtonStyle(
                                        color='onbackground', 
                                        bgcolor=ft.colors.ON_INVERSE_SURFACE, 
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    )
                                ), 
                            ]
                        ),
                        ft.TextButton('Убрать из ленты', 
                            height=40,
                            on_click=self.on_click_unpublished_alert,
                            style=ft.ButtonStyle(
                                color='onbackground', 
                                bgcolor=ft.colors.INVERSE_PRIMARY, 
                                shape=ft.RoundedRectangleBorder(radius=10)
                            )
                        )
                    ]
                )
            case Status.MODERATION:
                return ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.TextButton('Отказать', 
                            height=40,
                            on_click=self.on_click_rejected_alert,
                            style=ft.ButtonStyle(
                                color='onbackground', 
                                bgcolor=ft.colors.ERROR_CONTAINER,
                                shape=ft.RoundedRectangleBorder(radius=10)
                            )
                        ),
                        ft.TextButton('Опубликовать', 
                            height=40,
                            on_click=self.on_click_published,
                            style=ft.ButtonStyle(
                                color='onbackground', 
                                bgcolor=ft.colors.INVERSE_PRIMARY, 
                                shape=ft.RoundedRectangleBorder(radius=10)
                            )
                        ),
                    ]
                )
            case Status.REJECTED:
                return ft.Row(
                    spacing=0,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            spacing=5,
                            controls=[
                                ft.IconButton(icon='delete',
                                    on_click=self.on_click_delete,
                                    style=ft.ButtonStyle(
                                        color=ft.colors.ERROR,
                                        bgcolor=ft.colors.ERROR_CONTAINER, 
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    )
                                ),
                                ft.IconButton(icon='edit', data=False,
                                    on_click=self.on_click_edit,
                                    style=ft.ButtonStyle(
                                        color='onbackground', 
                                        bgcolor=ft.colors.ON_INVERSE_SURFACE, 
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    )
                                ),
                                ft.Badge(
                                    text='Отклонено',
                                    alignment=ft.alignment.Alignment(-1.8, -2),
                                    label_visible=not(self.reason['read']),
                                    content=ft.IconButton(icon=ft.icons.MARKUNREAD_ROUNDED,
                                        on_click=self.on_click_read_reason,
                                        style=ft.ButtonStyle(
                                            color='onbackground', 
                                            bgcolor=ft.colors.ON_INVERSE_SURFACE, 
                                            shape=ft.RoundedRectangleBorder(radius=10)
                                        )
                                    )
                                )
                            ]
                        ),
                        ft.TextButton('Опубликовать', 
                            height=40,
                            on_click=self.on_click_review_alert,
                            style=ft.ButtonStyle(
                                color='onbackground', 
                                bgcolor=ft.colors.INVERSE_PRIMARY, 
                                shape=ft.RoundedRectangleBorder(radius=10)
                            )
                        )
                    ]
                )
            case Status.PENDING:
                return ft.Row(
                    spacing=0,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            opacity=0.5,
                            spacing=5,
                            controls=[
                                ft.IconButton(icon='delete',
                                    disabled=True,
                                    on_click=self.on_click_delete_alert,
                                    style=ft.ButtonStyle(
                                        color=ft.colors.ERROR,
                                        bgcolor=ft.colors.ERROR_CONTAINER, 
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    )
                                ),
                                ft.IconButton(icon='edit',
                                    disabled=True,
                                    on_click=self.on_click_edit,
                                    style=ft.ButtonStyle(
                                        color='onbackground', 
                                        bgcolor=ft.colors.ON_INVERSE_SURFACE, 
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    )
                                ), 
                            ]
                        ),
                        ft.TextButton('Отменить отправку', 
                            height=40,
                            on_click=lambda _: self.firebase.unreview_announcement(self.announce_id),
                            style=ft.ButtonStyle(
                                color='onbackground', 
                                bgcolor=ft.colors.INVERSE_PRIMARY, 
                                shape=ft.RoundedRectangleBorder(radius=10)
                            )
                        )
                    ]
                )
            case Status.LOCAL:
                return ft.Row(
                    spacing=0,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            spacing=5,
                            controls=[
                                ft.IconButton(icon='delete',
                                    on_click=self.on_click_delete,
                                    style=ft.ButtonStyle(
                                        color=ft.colors.ERROR,
                                        bgcolor=ft.colors.ERROR_CONTAINER, 
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    )
                                ),
                                ft.IconButton(icon='edit', data=False,
                                    on_click=self.on_click_edit,
                                    style=ft.ButtonStyle(
                                        color='onbackground', 
                                        bgcolor=ft.colors.ON_INVERSE_SURFACE, 
                                        shape=ft.RoundedRectangleBorder(radius=10)
                                    )
                                ), 
                            ]
                        ),
                        ft.TextButton('Опубликовать', 
                            height=40,
                            on_click=self.on_click_review_alert,
                            style=ft.ButtonStyle(
                                color='onbackground', 
                                bgcolor=ft.colors.INVERSE_PRIMARY, 
                                shape=ft.RoundedRectangleBorder(radius=10)
                            )
                        )
                    ]
                )
    
    def on_click_attendees(self, e):
        self.page.dialog = ft.Container(
            padding=ft.padding.only(10,10,10,0),
            border_radius=10,
            content=ft.Column(
                controls=[
                    ft.Text('Участники'),
                    ft.Column(
                        scroll='hidden',
                        controls=[ft.ListTile(title=ft.Text(username)) for username in self.subscribers]
                    )
                ]
            )
        )
        self.page.update()

    def on_change_choice_reason(self, e):
        self.reason_input_field.value = e.control.value
        self.send_reason.disabled = False
        self.reason_bottom_sheet.update()

    def on_change_reason_input(self, e):
        self.send_reason.disabled = not(bool(e.control.value))
        self.choice_reason.value = None
        self.reason_bottom_sheet.update()

    def on_click_read_reason(self, e):
        self.page.dialog = ft.AlertDialog(
            adaptive=True,
            open=True,
            title=ft.Text('Причина отклонения'),
            content=ft.Text(self.reason['text'], 
                text_align=ft.TextAlign.LEFT),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton('Понятно', data=False, on_click=lambda _: self.page.close_dialog()),  
            ]
        )
      
        self.page.update()

    def on_click_published(self, e):
        data_to_upload = self._data_args()
        self.firebase.published_announcement(**data_to_upload)

    def on_click_rejected_alert(self, e):
        self.page.show_bottom_sheet(self.reason_bottom_sheet)

    def on_click_rejected(self, e):
        self.page.close_bottom_sheet()
        self.reason = self.reason_input_field.value
        self.reason = {'text':self.reason_input_field.value, 'read':False}
        self.firebase.rejected_announcement(**self._data_args())
    
    def on_click_join(self, e):
        if e.page.client_storage.get('role'):
            self.count_subs = int(self.content.content.controls[1].controls[0].content.controls[0].value) + 1
            self.content.content.controls[1].controls[0].content.controls[0].value = self.count_subs
            e.control.text = 'Отписаться'
            e.control.on_click = self.on_click_leave
            self.update()

            self.firebase.subscribe_announcement(**self._data_args(), username=self.page.client_storage.get('username'))
        else:
            e.page.dialog = ft.AlertDialog(
                adaptive=True, content_padding=15, open=True,
                content=ft.Text('Для участия в событии требуется авторизация', text_align=ft.TextAlign.CENTER),
                actions=[
                    ft.TextButton('Понятно', on_click=lambda _: e.page.close_dialog()),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            e.page.update()

    def on_click_leave(self, e):
        self.count_subs = int(self.content.content.controls[1].controls[0].content.controls[0].value) - 1
        self.content.content.controls[1].controls[0].content.controls[0].value = self.count_subs
        e.control.text = 'Участвовать'
        e.control.on_click = self.on_click_join
        self.update()
        self.firebase.unsubscribe_announcement(**self._data_args())

    def on_click_unpublished_alert(self, e):
        self.page.dialog = ft.AlertDialog(
            open=True,
            adaptive=True,
            content=ft.Text('Вы уверены, что хотите удалить данное событие из ленты публикации?', 
                text_align=ft.TextAlign.CENTER),
            actions_alignment=ft.MainAxisAlignment.SPACE_AROUND,
            actions=[
                ft.TextButton('Снять с публикации', style=ft.ButtonStyle(color='error'), data=False, 
                              on_click=lambda _: (self.firebase.unpublished_announcement(**self._data_args()),
                                                  e.page.close_dialog())), 
                ft.TextButton('Снять и удалить', style=ft.ButtonStyle(color='error'), data=True, 
                              on_click=lambda _: (self.firebase.unpublished_announcement(**self._data_args()), 
                                                self.firebase.delete_announcement(self.announce_id),
                                                e.page.close_dialog())), 
                ft.TextButton('Отмена', data=True, on_click=lambda _: e.page.close_dialog()), 
            ]
        )
        self.page.update()

    def on_click_review_alert(self, e):
        self.page.dialog = ft.AlertDialog(
            adaptive=True,
            open=True,
            content=ft.Text('Перед тем, как ваше событие будет опубликовано, его проверят модераторы', 
                text_align=ft.TextAlign.CENTER),
            actions_alignment=ft.MainAxisAlignment.SPACE_AROUND,
            actions=[
                ft.TextButton('Отменить', data=False, on_click=lambda _: self.page.close_dialog()), 
                ft.TextButton('Отправить', data=True, on_click=lambda _: self.on_click_review(e)), 
            ]
        )
      
        self.page.update()
    
    def on_click_review(self, e):
        self.page.close_dialog()
        self.page.update()
        self.firebase.review_announcement(
            self.announce_id,
            self.headline,
            self.text,
            self.place,
            self.datetime,
            self.role,
            self.author,
            self.image
        )

    def on_click_delete_alert(self, e):
        warning_text = 'Вы уверены, что хотите удалить "'+self.headline+'"?'
        self.page.dialog = ft.AlertDialog(
            adaptive=True,
            content=ft.Text(warning_text, text_align=ft.TextAlign.CENTER),
            actions_alignment=ft.MainAxisAlignment.SPACE_AROUND,
            actions=[
                ft.TextButton('Отменить', on_click=lambda _: self.page.close_dialog()), 
                ft.TextButton('Удалить', on_click=self.on_click_delete, style=ft.ButtonStyle(color='error'))
            ],
        )
        self.page.dialog.open = True
        self.update()

    def on_click_delete(self, e):
        e.page.close_dialog()
        self.firebase.delete_announcement(self.announce_id)
    
    def on_click_edit_time(self, e):
        edit_card = CreateAnnounceCard(self.page, self.firebase)
        edit_card.announce_id = self.announce_id
        edit_card.image = self.image
        edit_card.headline = self.headline
        edit_card.text = self.text
        edit_card.place = self.place
        edit_card.datetime = self.datetime
        edit_card.role = self.role
        edit_card.author = self.author
        edit_card.data = 'Сохранить'

        edit_card.image_disabled = True
        edit_card.headline_disabled = True
        edit_card.text_disabled = True
        edit_card.place_disabled = True
        
        edit_card.on_click_create = \
        lambda e: (self.firebase.change_datetime_announcement(**self._data_args(), new_datetime=edit_card.datetime), e.page.close_bottom_sheet())
        #edit_card.on_click_create = on_click_create_announce_card if e.control.data == False else change_datetime_card
        
        self.page.bottom_sheet = edit_card
        self.page.bottom_sheet.open = True
        self.page.update()

    def on_click_edit(self, e):
        edit_card = CreateAnnounceCard(self.page, self.firebase)
        edit_card.announce_id = self.announce_id
        edit_card.image = self.image
        edit_card.headline = self.headline
        edit_card.text = self.text
        edit_card.place = self.place
        edit_card.datetime = self.datetime
        edit_card.role = self.role
        edit_card.author = self.author
    
        edit_card.data = 'Сохранить'
        
        edit_card.on_click_create = edit_card.on_click_create_announce_card

        
        #edit_card.on_click_create = on_click_create_announce_card if e.control.data == False else change_datetime_card
        
        self.page.bottom_sheet = edit_card
        self.page.bottom_sheet.open = True
        self.page.update()


        