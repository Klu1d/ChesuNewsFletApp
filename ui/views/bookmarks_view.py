import copy
import flet as ft

from ui.controller.board import Board
from ui.widgets.custom_shimmer import CustomShimmer


def BookmarksView(page, firebase):
    def on_load_bookmarks():
        try:
            preloader(True)
            
            storage = page.client_storage.get('bookmarks')
            display = [int(i.controls[0].key) for i in container_favorites.content.controls]
            difference = list(set(storage) ^ set(display))
            
            for number in difference:
                if len(storage) < len(display):
                    ind = display.index(number)
                    del container_favorites.content.controls[ind]
                    del display[ind]
                    if not container_favorites.content.controls:
                        bookmark_view.controls[0].actions[0].visible = False
                        empty_icon.visible = True
                else:
                    ind = storage.index(number)
                    news = firebase.get_news(number)[0]
                    board = Board(page, firebase).old(
                        checkbox=True,
                        opacity=False,
                        number=news['id'],
                        headline=news['headline'],
                        image=news['images'][0],
                        time=news['datetime'],
                    )
                    container_favorites.content.controls.insert(ind,
                        ft.Stack(
                            controls=[
                                board,
                                ft.Container(
                                    data=ind,
                                    visible=False,
                                    padding=5,
                                    height=100,
                                    width=page.width,
                                    margin=board.margin,
                                    border_radius=15,
                                    on_click=on_click_container_checkbox,
                                    alignment=ft.alignment.top_right,
                                    content=ft.CircleAvatar(
                                        radius=15,
                                        bgcolor=ft.colors.with_opacity(0.3, ft.colors.GREY), 
                                        content=ft.Checkbox(fill_color='#007aff', check_color='white', disabled=True, on_change=on_click_container_checkbox)
                                    ),
                                ),
                            ]
                        )
                    )
                    bookmark_view.controls[0].actions[0].visible = True
                    empty_icon.visible = False     
            page.update()
        except Exception as e:
            print('BookmarksView: ', e)
        finally:    
            preloader(False)
    
    def preloader(activate: bool):
        if activate:
            page.overlay.append(ft.Container(bgcolor='background, 0.5', expand=True, disabled=True,alignment=ft.alignment.center, content=ft.ProgressRing()))
        else:
            page.overlay.clear()
        page.update()
        
    def on_click_container_checkbox(e: ft.ControlEvent):
        e.control.content.content.value = not (e.control.content.content.value)
        e.control.bgcolor = 'black, 0.4' if e.control.content.content.value == True else None
        page.update()
        #если у всех элементов checkbox значение True, я возвращаю True
        chooced_all = all(checkbox.controls[1].content.content.value == True for checkbox in container_favorites.content.controls)
        no_chooced_all = all(checkbox.controls[1].content.content.value == False for checkbox in container_favorites.content.controls)
        
        if chooced_all:
            button_remove_favorites.disabled = True
            bookmark_view.controls[0].leading.text = 'Отменить'
            bookmark_view.controls[0].leading.on_click = on_click_cancel
        else:
            button_remove_favorites.disabled = False
            bookmark_view.controls[0].leading.text = 'Выбрать все'
            bookmark_view.controls[0].leading.on_click = on_click_chooce_all
            
        button_remove_favorites.disabled = False if not no_chooced_all else True
        page.update()    
    
    def on_click_chooce(e: ft.ControlEvent):
        e.control.text = 'Готово'
        e.control.on_click = on_click_finish
        for checkbox in container_favorites.content.controls:
            checkbox.controls[1].visible = True
            
        bookmark_view.controls[2].height = 67
        bookmark_view.controls[0].title.visible = False
        bookmark_view.controls[0].leading = ft.TextButton('Выбрать все', on_click=on_click_chooce_all)
        bookmark_view.controls[0].leading_width = 115
        page.update()
    
    def on_click_chooce_all(e: ft.ControlEvent):
        e.control.text = 'Отменить'
        e.control.on_click = on_click_cancel
        for checkbox in container_favorites.content.controls:
            checkbox.controls[1].bgcolor = 'black, 0.4'
            checkbox.controls[1].content.content.value = True

        button_remove_favorites.disabled = False
        bookmark_view.controls[0].leading_width = 115
        page.update()
        
    def on_click_cancel(e: ft.ControlEvent):
        e.control.text = 'Выбрать все'
        e.control.on_click = on_click_chooce_all
        for checkbox in container_favorites.content.controls:
            checkbox.controls[1].content.content.value = False
            checkbox.controls[1].bgcolor = None
            
        button_remove_favorites.disabled = True
        bookmark_view.controls[0].leading_width = 115
        page.update()
        
    def on_click_finish(e: ft.ControlEvent):
        e.control.text = 'Выбрать'
        e.control.on_click = on_click_chooce
        for checkbox in container_favorites.content.controls:
            checkbox.controls[1].bgcolor = None
            checkbox.controls[1].visible = False
            checkbox.controls[1].content.content.value = False
        
        button_remove_favorites.disabled = True
        bookmark_view.controls[2].height = 0
        bookmark_view.controls[0].title.visible = True
        bookmark_view.controls[0].leading = None
        bookmark_view.controls[0].leading_width = None
        page.update()
    
    def on_click_remove_favorites(e: ft.ControlEvent):
        bookmarks = page.client_storage.get('bookmarks')
            
        for checkbox in copy.copy(container_favorites.content.controls):
            if checkbox.controls[1].content.content.value == True:
                container_favorites.content.controls.remove(checkbox)
                bookmarks.remove(int(checkbox.controls[0].key))
                page.client_storage.set('bookmarks', bookmarks)
                firebase.set_bookmark(bookmarks)
        if bookmarks == []:
            bookmark_view.controls[0].actions[0] = ft.TextButton(
                text='Выбрать', 
                visible=False if container_favorites.content.controls == [] else True,
                on_click=on_click_chooce
            )
            bookmark_view.controls[0].title.visible = True
            bookmark_view.controls[0].leading = None
            bookmark_view.controls[0].leading_width = None
            bookmark_view.controls[2].height = 0
            empty_icon.visible = True
        e.control.disabled=True
        page.update()
    
    button_remove_favorites = ft.OutlinedButton(
        text='Удалить', 
        icon=ft.icons.DELETE, 
        disabled=True,
        on_click=on_click_remove_favorites
    )
     
    container_favorites = ft.Container(
        alignment=ft.alignment.top_center,
        content=ft.Column()
    )
    
    empty_icon = ft.Container(
        visible=True if container_favorites.content.controls == [] else False,
        data='empty_icon',
        height=page.height - 80,
        alignment=ft.alignment.center,
        content=ft.Column(
            scroll=None,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
            controls=[
                ft.CircleAvatar(
                    radius=45,
                    bgcolor=ft.colors.with_opacity(0.3, ft.colors.GREY), 
                    content=ft.Icon(ft.icons.BOOKMARK_BORDER_ROUNDED, size=40)
                ),
                ft.Text(value='Здесь пока пусто!', size=21)
            ]
        )
    )
    
    bookmark_view = ft.View(
        route='/bookmarks',
        scroll='hidden',
        vertical_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        padding=0,
        
        controls=[
            ft.AppBar(
                center_title=True,
                title=ft.Text('Избранное', size=16), 
                actions=[ft.TextButton('Выбрать', 
                    visible=False if container_favorites.content.controls == [] else True,
                    on_click=on_click_chooce)]),
            ft.Stack(
                controls=[
                    empty_icon,
                    container_favorites,
                ]
            ),
            ft.BottomAppBar(
                height=0,
                content=button_remove_favorites,
                animate_size=ft.animation.Animation(400, "decelerate"),
                
                
            )
        ] 
    )

    return {
        'view':bookmark_view,
        'load':on_load_bookmarks,
    }