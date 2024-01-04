import requests
from .admin import Admin
class Api:
    def __init__(self, name, list_obj):
        self.name = name
        self.list_obj = list_obj
        self.ip = None
    @classmethod
    def client(cls, name, list_obj):
        return cls(name, list_obj)
    def get_key(self, ip):
        if not isinstance(self.list_obj, list):
            raise TypeError("list_obj must be a list")
        if not isinstance(self.name, str) or not isinstance(ip, str):
            raise TypeError("name and ip must be a string")
        if len(self.list_obj) != 2:
            raise ValueError("not enough values to unpack (expected 2, got 1)")
        token, long_url = self.list_obj
        if not isinstance(token, str) or not isinstance(long_url, str):
            raise TypeError("token and long_url must be a string")
        self.ip = ip
        request_key = requests.post('https://81082956-3be1-4727-a3bc-80f73b5793df-00-vy262ynkk7xv.worf.replit.dev/get', json = {'keyword':'Khoidz', 'name': self.name, 'ip': ip, 'token': token, 'long_url': long_url}).json()
        return request_key
    def check_key(self, ip, key):
        request_key = requests.post('https://81082956-3be1-4727-a3bc-80f73b5793df-00-vy262ynkk7xv.worf.replit.dev/check', json = {'keyword':'Khoidz', 'name': self.name, 'ip': ip, 'key': key}).json()
        return request_key
