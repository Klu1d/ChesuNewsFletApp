import pyrebase
import json
from multipledispatch import dispatch
from flet.security import encrypt, decrypt
from config import FIREBASE_KEYS

secret_key = 'sample'

class Status():
    LOCAL = 'local'
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    PUBLISHED = 'published'
    MODERATION = 'moderation'
    OLD_EVENT = 'old_event'

class PyrebaseWrapper:
    def __init__(self, page):
        self.page = page
        self.firebase = pyrebase.initialize_app(FIREBASE_KEYS)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        #Переменные, где мы храним временный токен и
        # постоянный идентификатор пользователя во время работы приложения
        self.idToken = None
        self.uuid = None
        self.user = None
        #Если приложение было недавно запущено, 
        # мы можем получить токен с устройства пользователя.
        

        self.streams = {}

    def save_tokens(self, token, uuid, page):
        encrypted_token = encrypt(token, secret_key)
        page.client_storage.set('firebase_token', encrypted_token)
        page.client_storage.set('firebase_id', uuid)
        self.idToken = token
        self.uuid=uuid
        
    
    def erase_token(self):
        if not(self.account_info().get('role')):
            print("Анонимный пользователь удален")
            self.auth.delete_user_account(self.idToken)
        self.page.client_storage.remove('firebase_token')
        self.page.client_storage.remove('firebase_id')

    def register_user(self, name, lastname, role, email, password, faculty, bookmarks=None, tabs=None):
        data={
            'firstname': name, 
            'lastname': lastname, 
            'role': role, 
            'bookmarks': bookmarks, 
            'tabs': tabs, 
            'email': email,
            'faculty':faculty,
        }
        self.auth.create_user_with_email_and_password(email, password)
        self.sign_in(email, password)
        self.db.child('users').child(self.uuid).update(data=data, token=self.idToken)
        #self.auth.verify_password_reset_code
    
    def sign_in(self, email, password):
        self.user = self.auth.sign_in_with_email_and_password(email, password)
        if self.user:
            token = self.user['idToken']
            self.uuid = self.user['localId']
            self.save_tokens(token, self.uuid, self.page)
        
    def sign_out(self):
        self.erase_token()

    
    def login_in_anonymous(self):
        user_credential = self.firebase.auth().sign_in_anonymous()
        if user_credential:
            token = user_credential['idToken']
            uuid = user_credential['localId']
            self.save_tokens(token, uuid, self.page)

    def refresh_user_token(self, refresh_token):
        try:
            refreshed_user = self.auth.refresh(refresh_token)
            if refreshed_user and 'idToken' in refreshed_user:
                new_token = refreshed_user['idToken']
                return new_token
            else:
                print("Ошибка при обновлении токена: неверный формат данных.")
                return None
        except pyrebase.pyrebase.HTTPError as e:
            print("Ошибка при обновлении токена:", e.errno
            )
            return None

    def retry_authentication(self, email, password):
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            if 'idToken' in user:
                print("Аутентификация успешна.")
                return user['idToken']
            else:
                print("Ошибка при повторной аутентификации: неверный формат данных.")
                return None
        except pyrebase.pyrebase.HTTPError as e:
            print("Ошибка при повторной аутентификации:", e)
            return None

    def check_token(self):
        try:
            encrypted_token = self.page.client_storage.get('firebase_token')
            uuid = self.page.client_storage.get('firebase_id')
            if encrypted_token:
                decrypted_token = decrypt(encrypted_token, secret_key)
                self.idToken = decrypted_token
                self.uuid = uuid
                try:
                    self.auth.get_account_info(self.idToken)
                    return 'Success'
                except:
                    print('Токен устарел, идет процесс обновления')
                    self.page.update()
                    # new_token = self.refresh_user_token(self.idToken)
                    # if new_token:
                    #     print('Токен обновлен')
                    #     self.idToken = new_token
                    #     self.save_tokens(new_token, self.uuid, self.page)
                    #     return 'Success'
                    # else:
                    print('Токен недействителен, требуется аутентификация')
                        # new_token = self.retry_authentication(email, password)
                        # if new_token:
                        #     print('Токен создан после повторной аутентификации')
                        #     self.idToken = new_token
                        #     self.save_tokens(new_token, self.uuid, self.page)
                        #     return 'Success'
                        # else:
                        #     print('Не удалось создать токен после повторной аутентификации')
                        #     
                    return None
            return None
        except TimeoutError as e:
            print('Pyrebase check token: ', e)
            return None

    

    def set_news(self, id: int, datetime: str, headline: str, text: str, images: list, tags: list):
        data_to_upload = {
            'id':id,
            'datetime': datetime,
            'headline': headline,
            'text': text,
            'images': images,
            'tags': tags,
        }
        self.db.child('chesu').child('news').child(str(id)).set(data=data_to_upload, token=self.idToken)

    def get_latest_news_key(self):
        news = self.db.child("chesu").child("news").get()
        if news.each() is not None:
            keys = [item.key() for item in news.each()]
            latest_key = max(keys, key=int)
            return int(latest_key)
        return None

    def get_users_tabs(self):
        tabs = self.db.child('users').child(self.uuid).child('tabs').get(token=self.idToken).val()
        if tabs:
            tabs = dict(tabs)
            return tabs
        else:
            tabs = dict(self.get_tabs())
            return tabs
    
    def get_tabs(self):
        return self.db.child('chesu').child('tabs').get().val()

    @dispatch()  
    def get_news(self):
        return list(self.db.child('chesu').child('news').get().val().values())[::-1]
    
    @dispatch(int)
    def get_news(self, id: int):
        list_items = []
        for item in self.get_news():
            if item['id'] == id:
                list_items.insert(0, item)
            else:
                continue
        return list_items[::-1] if list_items != [] else None
    
    @dispatch(str)
    def get_news(self, tag: str):
        list_items = []
        for item in self.get_news():
            if 'tags' in item:
                if tag in item['tags']:
                    list_items.insert(0, item)
            else:
                continue
        
        return list_items[::-1] if list_items != [] else None
    
    """Работа с AnnounceView"""
    def create_announcement(
        self, announce_id, 
        headline, text, 
        place, datetime, 
        role, username, 
        image, 
        status='local'
    ):
        
        data_to_upload = {
            'status': status,
            'announce_id': announce_id,
            'headline': headline,
            'datetime': datetime,
            'author': username,
            'image': image,
            'place': place,
            'text': text,
            'role': role,
        }
        self.db.child('users').child(self.uuid).child('announcements').child(announce_id).update(data_to_upload, token=self.idToken)
    
    def send_announcement(
        self, announce_id, 
        headline, text, 
        place, datetime, 
        role, username, 
        image=None, 
        status=Status.PENDING
    ):
        data_to_upload = {
            'content':{
                'announce_id': announce_id,
                'headline': headline,
                'datetime': datetime,
                'author': username,
                'image': image,
                'place': place,
                'text': text,
                'role': role,
            },
            'status':status,
        }
        self.db.child('moderations').child(self.uuid).child(announce_id).set(data_to_upload, token=self.idToken)
        self.db.child('users').child(self.uuid).child('announcements').child(announce_id).update({'status': Status.PENDING}, token=self.idToken)
    
    def change_datetime_announcement(self, new_datetime, **data):
        data['datetime'] = new_datetime
        self.db.child('users').child(self.uuid).child('announcements') \
        .child(data.get('announce_id')).update(data, token=self.idToken)

        data['status'] = Status.PUBLISHED
        self.db.child('chesu').child('announcements').child(data.get('announce_id')).update(data, token=self.idToken)
    
    def rejected_announcement(self, **data):
        data['status'] = Status.REJECTED
        self.db.child('users').child(data.get('author_id')).child('announcements').child(data.get('announce_id')).update(data, token=self.idToken)
        self.db.child('moderations').child(data.get('announce_id')).remove(self.idToken)

    def published_announcement(self, **data_to_upload):
        data_to_upload['status'] = Status.PUBLISHED
        self.db.child('chesu').child('announcements').child(data_to_upload.get('announce_id')).update(data_to_upload, token=self.idToken)
        
        data_to_upload['status'] = Status.APPROVED
        self.db.child('users').child(data_to_upload.get('author_id')).child('announcements').child(data_to_upload.get('announce_id')).update(data_to_upload, token=self.idToken)
        self.db.child('moderations').child(data_to_upload.get('announce_id')).remove(self.idToken)
    
    def unpublished_announcement(self, **data):
        data['status'] = Status.LOCAL
        self.db.child('chesu').child('announcements').child(data.get('announce_id')).remove(self.idToken)
        self.db.child('users').child(self.uuid).child('announcements').child(data.get('announce_id')).update(data, token=self.idToken)

    def delete_announcement(self, announce_id):
        self.db.child('users').child(self.uuid).child('announcements').child(announce_id).remove(self.idToken)

    def time_over_announcement(self, **data):
        data['status'] = Status.OLD_EVENT
        self.db.child('chesu').child('announcements').child(data['announce_id']).remove(self.idToken)
        self.db.child('users').child(data['author_id']).child('old_events').child(data['announce_id']).update(data, self.idToken)
        self.db.child('users').child(data['author_id']).child('announcements').child(data['announce_id']).remove(self.idToken)

    def subscribe_announcement(self, username, **data):

        data['subscribers'][self.uuid] = username
        self.db.child('chesu') \
        .child('announcements').child(data.get('announce_id')).update(data, token=self.idToken)

    def unsubscribe_announcement(self, **data):
        self.db.child('chesu') \
        .child('announcements').child(data.get('announce_id')).update(data, token=self.idToken)

    def review_announcement(
        self, announce_id, 
        headline, text, 
        place, datetime, 
        role, username,
        image,
    ):
        data_to_upload = {
            'author_id': self.uuid,
            'announce_id': announce_id,
            'headline': headline,
            'datetime': datetime,
            'author': username,
            'image': image,
            'place': place,
            'text': text,
            'role': role,
        }
        data_to_upload['status'] = Status.PENDING
        self.db.child('users').child(self.uuid).child('announcements').child(announce_id).update(data_to_upload, token=self.idToken)
        data_to_upload['status'] = Status.MODERATION
        self.db.child('moderations').child(announce_id).update(data_to_upload, token=self.idToken)
    
    def unreview_announcement(self, announce_id):
        data_to_upload = self.db.child('users').child(self.uuid).child('announcements').child(announce_id).get(self.idToken).val()
        data_to_upload['status'] = Status.LOCAL
        self.db.child('users').child(self.uuid).child('announcements').child(announce_id).update(data_to_upload, token=self.idToken)
        self.db.child('moderations').child(announce_id).remove(self.idToken)

    def stream_public_announcements(self, stream_handler):
        stream = self.db.child('chesu') \
            .child('announcements') \
            .stream(stream_handler=stream_handler, stream_id='chesu', token=self.idToken)
        
        self.streams['chesu'] = stream

    def stream_user_account(self, stream_handler):
        stream = self.db.child('users') \
            .child(self.uuid) \
            .stream(stream_handler=stream_handler, stream_id='users', token=self.idToken)

        self.streams['users'] = stream
        
    def stream_moderation_decisions(self, stream_handler):
        status = self.db.child("moderations") \
        .stream(stream_handler=stream_handler, stream_id='moderations',token=self.idToken)

        self.streams['moderations'] = status

    # def stream_moderation_decisions(self, stream_handler):
    #     status = self.db.child("users").child(self.uuid) \
    #     .stream(stream_handler=stream_handler, stream_id='moderator',token=self.idToken)

    #     self.streams['moderator'] = status


    """Работа с BookmarksView"""
    def get_bookmarks(self):
        bookmarks = self.db.child('users').child(self.uuid).child('bookmarks').get(token=self.idToken).val()
        if bookmarks:
            return list(bookmarks)
        else:
            return []

    def check_bookmark(self, bookmarks):
        return self.db.child('users').child(self.uuid).child('bookmarks').get(token=self.idToken).val()

    def set_bookmark(self, bookmarks: list):
        self.db.child('users').child(self.uuid).child('bookmarks').child().set(token=self.idToken, data=bookmarks)

    def del_bookmark(self, id_news):
        self.db.child('users').child(self.uuid).child('bookmarks').child(id_news).remove(self.idToken)
        



    def account_info(self):
        user = self.auth.get_account_info(self.idToken)['users'][0]
        user['firstname'] = self.db.child('users').child(self.uuid).child('firstname').get(token=self.idToken).val()
        user['lastname'] = self.db.child('users').child(self.uuid).child('lastname').get(token=self.idToken).val()
        user['role'] = self.db.child('users').child(self.uuid).child('role').get(token=self.idToken).val()
        user['faculty'] = self.db.child('users').child(self.uuid).child('faculty').get(token=self.idToken).val()
        bookmarks = self.db.child('users').child(self.uuid).child('bookmarks').get(token=self.idToken).val()
        user['bookmarks'] = list(bookmarks) if bookmarks else []
        user['theme_mode'] = 'system'

        if user['firstname'] == None:
            return user | {'username':'Анонимный пользователь', 'firstname': '', 'lastname':'', 'role':'','faculty':'', 'email':'',  'bookmarks':[]}
        user['username'] = user['firstname'] + ' ' + user['lastname']
        return user
    
    def is_user_anonymous(self):
        user = self.auth.get_account_info(self.idToken)
        return user['users'][0].__contains__('email')
    
    def kill_all_streams(self):
        try:
            if self.streams:
                for stream in self.streams.values():
                    if stream is not None:  # Проверяем, что поток не равен None
                        stream.close()
                self.streams.clear()  # Очищаем словарь потоков после их закрытия
        except Exception as e:
            print('Error while closing streams:', e)



