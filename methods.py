import requests
from requests.auth import HTTPBasicAuth

class Type():
        GET='get'
	POST='post'

class Method():
	def __init__(self, method_url, method_credentials, method_type, payload=None):
		self.method_url = method_url
		self.method_credentials = method_credentials
		self.method_type = method_type
		self.payload = payload 
		
	def execute(self):
		headers = {'content-type': 'application/xml'}
		return getattr(requests, self.method_type)(self.method_url, auth=HTTPBasicAuth(self.method_credentials['username'],self.method_credentials['password']),data=self.payload, headers=headers)
