# ЧГУ Новостное Приложение (ChGU News App)

<div style="text-align: center;">
  <img src="https://static.tildacdn.com/tild6230-3664-4432-b863-353833663132/__.png" width="200"/>
</div>

Добро пожаловать в репозиторий новостного приложения Чеченского Государственного Университета. Это приложение предоставляет последние новости, анонсы событий и другую полезную информацию для студентов, преподавателей и сотрудников университета.

## Оглавление
- [Описание](#описание)
- [Установка и Запуск](#установка-и-запуск)
- [Лицензия](#лицензия)

## Описание

Новостное приложение Чеченского Государственного Университета — это мобильное приложение, которое обеспечивает доступ к последним новостям университета, анонсам событий, учебному расписанию, контактам и другой полезной информации.

<div style="text-align: center;">
  <img src="image-2.png" width="280" style="display: inline-block;"/>
  <img src="image-3.png" width="280" style="display: inline-block;"/>
  <img src="image-1.png" width="280" style="display: inline-block;"/>
  <img src="image.png"   width="280" style="display: inline-block;"/>
</div>

## Установка и Запуск

Чтобы развернуть и запустить приложение, выполните следующие шаги:

1. Загрузите проект на ПК:
   ```git clone https://github.com/Klu1d/chesu-news-app```
2. Создайте виртуальное окружение:
  ```python -m venv .venv```
3. Скачайте все зависимости:
  ```pip install -r requirements.txt```
4. Получите ключи к проекту Firebase, пример того как они должны выглядеть:
    ```
    FIREBASE_KEYS = {
        "apiKey": "123321",
        "authDomain": "chesu-news.firebaseapp.com",
        "databaseURL": "https://chesu-neasdasdw45.fasidasrdaefsdfbgasd.com",
        "projectId": "chesu-news",
        "storageBucket": "cnews.apasdas4312pot.com",
        "messagingSenderId": "1232131",
        "appId": "1:403596570161asd32423:web:aslkdm3423rasd",
        "measurementId": "G-34qasdawsr23r"
    }
5. Создайте файл ```config.py``` и положите его рядом с файлом ```main.py```

6. Запустите приложение:
  ```flet run``` или ```flet run --ios```, ```flet run --android ```

