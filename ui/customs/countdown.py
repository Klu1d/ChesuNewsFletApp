import asyncio
import flet as ft
import copy

class Countdown(ft.TextButton):
    def __init__(self, seconds, on_click):
        super().__init__()
        self.seconds = seconds
        self.value = seconds
        self.on_click = on_click
        self.running = False
        self.disabled = True

    def did_mount(self):
        self.page.run_task(self.update_timer)

    def will_unmount(self):
        self.running = False

    async def update_timer(self):
        self.disabled = True
        while self.seconds and self.running:
            mins, secs = divmod(self.seconds, 60)
            self.text = "Отправить повторно {:02d}:{:02d}".format(mins, secs)
            self.update()
            await asyncio.sleep(1)
            self.seconds -= 1
        self.text = 'Отправить повторно'
        self.disabled = False
        self.update()



    
   
