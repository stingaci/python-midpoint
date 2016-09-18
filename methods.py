import requests
import midpoint_exceptions
from requests.auth import HTTPBasicAuth

class Type():
        GET='get'
	POST='post'
	DELETE='delete'

class Method():
	def __init__(self, method_url, method_credentials, method_type, payload=None):
		self.method_url = method_url
		self.method_credentials = method_credentials
		self.method_type = method_type
		self.payload = payload 
		
	def execute(self):
		headers = {'content-type': 'application/xml'}
		try: 
			response = getattr(requests, self.method_type)(self.method_url, auth=HTTPBasicAuth(self.method_credentials['username'],self.method_credentials['password']),data=self.payload, headers=headers, timeout=5)
			return response
		except requests.exceptions.ConnectionError as e:
			raise midpoint_exceptions.ConnectionError(e)
		except requests.exceptions.Timeout as e:
			raise midpoint_exceptions.Timeout(e)
		except requests.exceptions.HTTPError as e:
			raise midpoint_exceptions.HTTPError(e)
