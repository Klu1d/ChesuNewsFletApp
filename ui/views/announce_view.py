import datetime
import flet as ft

def AnnounceView(page, firebase):
    def on_load_announce():
        pass
    
    def dismissed(e):
        datetime_button.icon=ft.icons.EDIT_CALENDAR
        datetime_button.text=None
        page.update()
        
        
    def change_time(e):
        datetime_button.text += e.control.value.strftime(' %H:%M')
        page.update()
        
        
    def change_date(e):
        datetime_button.text = datetime.datetime.strftime(e.control.value, '%d.%m.%Y')
        datetime_button.icon = None
        on_click_time_button(e)

        
    def on_click_time_button(e):
        page.overlay.append(time_picker)
        page.update()
        time_picker.pick_time()

    def on_click_date_button(e):
        page.overlay.clear()
        page.overlay.append(date_picker)
        page.update()
        date_picker.pick_date()
        
    avatar = ft.CircleAvatar(
        content=ft.Image(src='./assets/logo/logo.png'),
        radius=25,
    )
    dropdown_faculties = ft.Dropdown(
        label='Факультет/Институт',
        border=ft.InputBorder.NONE,
        options=[ft.dropdown.Option(faculti) for faculti in  page.client_storage.get('tabs').keys() if faculti not in ['Новости', 'Анонсы']],
    )
    headline = ft.TextField(
        label='Заголовок',
        border=ft.InputBorder.NONE,
    )
    text = ft.TextField(
        label='Текст',
        multiline=True,
        border=ft.InputBorder.NONE,
    )
    send_button = ft.ElevatedButton(
        'Отправить на проверку',
    )

    date_picker = ft.DatePicker(
        confirm_text="Выбрать",
        cancel_text='Отменить',
        error_format_text='Неправильный формат даты',
        error_invalid_text=" ",
        help_text='Укажите дату',
        on_change=change_date,
        on_dismiss=dismissed,
        first_date=datetime.datetime(2023, 10, 1),
        last_date=datetime.datetime(2024, 10, 1),
    )
    
    time_picker = ft.TimePicker(
        confirm_text="Выбрать",
        cancel_text='Отменить',
        error_invalid_text=" ",
        help_text="Выберите время",
        hour_label_text='Часы',
        minute_label_text='Минуты',
        on_change=change_time,
        on_dismiss=dismissed,
    )
    
    datetime_button = ft.TextButton(
        icon=ft.icons.EDIT_CALENDAR,
        on_click=on_click_date_button,
    )
    
    datetime_text = ft.Text(value='Дата проведения:')
    announce_view = ft.View(
        route='/announce',
        scroll='hidden',
        controls=[
            ft.AppBar(
                center_title=True,
                title=ft.Text('Создать мероприятие', size=16), 
            ),
            ft.Row([avatar, dropdown_faculties]),
            ft.Row([datetime_text, datetime_button], spacing=0),
            headline,
            text,
            send_button,
        ] 
    )
    return {
        'view':announce_view,
        'load':on_load_announce,
    }