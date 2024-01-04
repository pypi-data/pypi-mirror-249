import requests
class Admin:
    def __init__(self, admin):
        self.admin = admin
        self.methods = None
        self.key = None
    @classmethod
    def client(cls, admin):
        return cls(admin)
    def add_key(self, key, methods):
        if not isinstance(key, str) or not isinstance(methods, str) or not isinstance(self.admin, str):
            raise TypeError("key, admin and methods must be a string")
        try:
            add = requests.get(f'https://81082956-3be1-4727-a3bc-80f73b5793df-00-vy262ynkk7xv.worf.replit.dev/addkey?admin={self.admin}&key={key}&loaikey={methods}').json()
            check = add['status']
            if check == 'success':
                return add['message']
            else:
                return add['message']
        except Exception as e:
            raise ValueError(f"Exception: {e}")
    def remove(self, key):
        try:
            add = requests.get(f'https://81082956-3be1-4727-a3bc-80f73b5793df-00-vy262ynkk7xv.worf.replit.dev/remove?admin={self.admin}&key={key}').json()
            check = add['status']
            if check == 'success':
                return add['message']
            else:
                return add['message']
        except Exception as e:
            raise ValueError(f"Exception: {e}")