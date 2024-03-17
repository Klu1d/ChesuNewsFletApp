import sys
import pyrebase

from enum import Enum
from multipledispatch import dispatch
from flet.security import encrypt, decrypt
from firebase.config import config_keys as keys

secret_key = 'sample'

class Status():
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    
class PyrebaseWrapper:
    def __init__(self, page):
        self.page = page
        self.firebase = pyrebase.initialize_app(keys)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        #Переменные, где мы храним временный токен и
        # постоянный идентификатор пользователя во время работы приложения
        self.idToken = None
        self.uuid = None
        #Если приложение было недавно запущено, 
        # мы можем получить токен с устройства пользователя.
        self.check_token()
        

        self.streams = {}

    def save_tokens(self, token, uuid, page):
        encrypted_token = encrypt(token, secret_key)
        page.client_storage.set('firebase_token', encrypted_token)
        page.client_storage.set('firebase_id', uuid)
        self.idToken = token
        self.uuid=uuid
    
    def erase_token(self):
        self.page.client_storage.remove('firebase_token')
        self.page.client_storage.remove('firebase_id')

    def register_user(self, name, lastname, role, email, password, bookmarks=None, tabs=None):
        data={'firstname':name, 'lastname':lastname, 'role':role, 'bookmarks':bookmarks, 'tabs':tabs, 'email':email}
        self.auth.create_user_with_email_and_password(email, password)
        self.sign_in(email, password)
        self.db.child('users').child(self.uuid).update(data=data, token=self.idToken)
        self.auth.send_email_verification(self.idToken)

    def remove_user(self):
        self.db.child('users').child(self.uuid).remove(self.idToken)
        
    def sign_in(self, email, password):
        user = self.auth.sign_in_with_email_and_password(email, password)
        
        if user:
            token = user['idToken']
            uuid = user['localId']
            self.save_tokens(token, uuid, self.page)

    def sign_out(self):
        self.erase_token()
    
    def login_in_anonymous(self):
        user_credential = self.firebase.auth().sign_in_anonymous()
        
        if user_credential:
            token = user_credential['idToken']
            uuid = user_credential['localId']
            self.save_tokens(token, uuid, self.page)

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
        self.db.child('chesu').child('news').child(str(id)).set(data_to_upload)

    def get_username(self):
        firstname = self.db.child('users').child(self.uuid).child('firstname').get(token=self.idToken).val()
        lastname = self.db.child('users').child(self.uuid).child('lastname').get(token=self.idToken).val()
        role = self.db.child('users').child(self.uuid).child('role').get(token=self.idToken).val()
        if firstname == None:
            average = int(len(self.uuid) / 2)
            return self.uuid[:average], self.uuid[average:], 'Аноним' 
        return firstname, lastname, role
    
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
        image=None, 
        status='local'
    ):
        data_to_upload = {
            'status': status,
            'announce_id': announce_id,
            'headline': headline,
            'datetime': datetime,
            'username': username,
            'image': image,
            'place': place,
            'text': text,
            'role': role,
        }
        self.db.child('users').child(self.uuid).child('announcements').child(announce_id).set(data_to_upload, token=self.idToken)
    
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
                'username': username,
                'image': image,
                'place': place,
                'text': text,
                'role': role,
            },
            'status':status,
        }
        self.db.child('moderations').child(self.uuid).child(announce_id).set(data_to_upload, token=self.idToken)
        self.db.child('users').child(self.uuid).child('announcements').child(announce_id).update({'status': Status.PENDING}, token=self.idToken)
    
    def change_status_announce(self, id, new_status, user_id=None):
        try:
            if not user_id:
                self.db.child('users').child(self.uuid).child('announcements').child(id).child('status').set(new_status, token=self.idToken)
            else:
                self.db.child('users').child(user_id).child('announcements').child(id).child('status').set(new_status, token=self.idToken)
        except pyrebase.pyrebase.HTTPError as e:
            print('Нет такого пользователя: ', e)
    
    def cancel_send_announcement(self, announce_id):
        pass
            
    def delete_announcement(self, announce_id):
        self.db.child('users').child(self.uuid).child('announcements').child(announce_id).remove(token=self.idToken)
        
    def publish_announcement(
        self, announce_id, 
        headline, text, 
        place, datetime, 
        role, username, 
        image=None, 
    ):
        data_to_upload = {
            'announce_id': announce_id,
            'headline': headline,
            'datetime': datetime,
            'username': username,
            'image': image,
            'place': place,
            'text': text,
            'role': role,
            'attendees':0,
            'count_attendees':0
        }
        self.db.child('chesu').child('announcements').child(announce_id).set(data_to_upload, token=self.idToken)

    def stream_public_announcements(self, stream_handler):
        stream = self.db.child('chesu').child('announcements').stream(stream_handler=stream_handler, stream_id='public', token=self.idToken)
        self.streams['public'] = stream

        
    def stream_user_draft_announcements(self, stream_handler):
        stream = self.db.child('users').child(self.uuid).child('announcements').stream(stream_handler=stream_handler, stream_id='users', token=self.idToken)
        self.streams['users'] = stream
        

    def stream_moderation_decisions(self):
        status = self.db.child("moderations").stream(stream_handler=self.status_card_update, stream_id='moderator',token=self.idToken)
        self.streams['moderator'] = status

    def status_card_update(self, event):
        if event['data'] != None:
            if event['event'] == 'put':
                if isinstance(event['data'], str):
                    elements = list(filter(None, event['path'].split("/")))
                    self.db.child("users").child(elements[0]).child('announcements').child(elements[1]).update({'status': event['data']}, token=self.idToken)

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
        self.db.child('users').child(self.uuid).child('bookmarks').remove(id_news)

    def account_info(self):
        user = self.auth.get_account_info(self.idToken)
        return user['users'][0]

    def is_user_anonymous(self):
        user = self.auth.get_account_info(self.idToken)
        return user['users'][0].__contains__('email')
    
    def kill_all_streams(self):
        try:
            if self.streams:
                for stream in self.streams.values():
                    stream.close()
                self.streams.clear()  # Очищаем словарь потоков после их закрытия
        except Exception as e:
            print('Error while closing streams:', e)


