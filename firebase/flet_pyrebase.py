import sys
import pyrebase

from firebase.config import config_keys as keys
from flet.security import encrypt, decrypt
from multipledispatch import dispatch

secret_key = "sample"

class PyrebaseWrapper:
    """
    Wraps Pyrebase with flet authentication flow and abstracts crud for my app. 
    """

    def __init__(self, page):
        self.page = page
        self.firebase = pyrebase.initialize_app(keys)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()
        ### Переменные, где мы храним временный токен и постоянный идентификатор пользователя во время работы приложения
        self.idToken = None
        self.uuid = None
        ### Если приложение было недавно запущено, мы можем получить токен с устройства пользователя.
        self.check_token()
        
        self.streams_1 = []


    def save_tokens(self, token, uuid, page):
        encrypted_token = encrypt(token, secret_key)
        page.client_storage.set("firebase_token", encrypted_token)
        page.client_storage.set("firebase_id", uuid)
        self.idToken = token
        self.uuid=uuid
    
    def erase_token(self):
        self.page.client_storage.remove("firebase_token")
        self.page.client_storage.remove("firebase_id")

    def register_user(self, name, lastname, role, email, password, verificated=False):
        self.auth.create_user_with_email_and_password(email, password)
        self.sign_in(email, password)
        
        self.db.child("users").child(self.uuid).update(data={"firstname":name, "lastname":lastname, "role":role, "verificated":verificated}, token=self.idToken)
        self.auth.send_email_verification(self.idToken)
    
    def sign_in(self, email, password):
        user = self.auth.sign_in_with_email_and_password(email, password)
        if user:
            token = user["idToken"]
            uuid = user["localId"]
            self.save_tokens(token, uuid, self.page)

    def sign_out(self):
        self.erase_token()
    
    def login_in_anonymous(self):
        user_credential = self.firebase.auth().sign_in_anonymous()
        
        if user_credential:
            token = user_credential["idToken"]
            uuid = user_credential["localId"]
            self.save_tokens(token, uuid, self.page)

    def check_token(self):
        encrypted_token = self.page.client_storage.get("firebase_token")
        uuid = self.page.client_storage.get("firebase_id")
        if encrypted_token:
            decrypted_token = decrypt(encrypted_token, secret_key)
            self.idToken = decrypted_token
            self.uuid = uuid
            try:
                self.auth.get_account_info(self.idToken)
                return "Success"
            except:
                return None
        return None

    def check_bookmark(self, id_news):
        # if id_news in list[self.db.child("users").child(self.uuid).child("bookmarks").get().val()]:
        #     return True
        # else:
        #     return False
        
        
        return self.db.child("users").child(self.uuid).child("bookmarks").get(token=self.idToken).val()

    def set_bookmark(self, id_news):
        bookmarks = self.db.child("users").child(self.uuid).child("bookmarks").get(token=self.idToken).val()
        
        self.db.child("users").child(self.uuid).child("bookmarks").child().set(token=self.idToken, data=bookmarks)

    def del_bookmark(self, id_news):
        self.db.child("users").child(self.uuid).child("bookmarks").remove(id_news)
    
    def set_news(self, id: int, datetime: str, headline: str, text: str, images: list, tags: list):
        data_to_upload = {
            'id':id,
            'datetime': datetime,
            'headline': headline,
            'text': text,
            'images': images,
            'tags': tags,
        }
        self.db.child("chesu").child("news").child(str(id)).set(data_to_upload)

    def get_username(self):
        return self.db.child("users").child(self.uuid).child("username").get(token=self.idToken).val()

    def get_tabs(self):
        return self.db.child("chesu").child("tabs").get().val()

    @dispatch()  
    def get_news(self):
        return list(self.db.child("chesu").child("news").get().val().values())[::-1]

    @dispatch(int)
    def get_news(self, id: int):
        for item in list(self.db.child("chesu").child("news").get().val().values()):
            if item['id'] == id:
                return self.db.child("chesu").child("news").child(item['id']).get().val()

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
    
    def add_note(self, data):
        if self.uuid == None:
            self.uuid = self.auth.get_account_info(self.idToken)["users"][0]["localId"]
        self.db.child("users").child(self.uuid).child("notes").push(data, self.idToken)

    def get_notes(self):
        return self.db.child("users").child(self.uuid).get(token=self.idToken).val()
    
    def email_verified(self):
        user = self.auth.get_account_info(self.idToken)
        return user['users'][0]['emailVerified']

    def stream_data(self, stream_handler):
        stream = self.db.child("users").child(self.uuid).child("notes").stream(stream_handler=stream_handler, token=self.idToken)
        self.streams_1.append(stream)
    
    def edit_note(self, note_uuid, data):
        self.db.child("users").child(self.uuid).child("notes").child(note_uuid).update(data, token=self.idToken)

    def delete_note(self, note_uuid):
        self.db.child("users").child(self.uuid).child("notes").child(note_uuid).remove(token=self.idToken)

    def kill_all_streams(self):
        for stream in self.streams_1:
            try:
                stream.close()
            except:
                print("no streams")


