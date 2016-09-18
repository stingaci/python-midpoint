import requests

class ConnectionError(requests.exceptions.ConnectionError):
	pass

class HTTPError(requests.exceptions.HTTPError):
	pass

class Timeout(requests.exceptions.Timeout):
	pass

class InvalidModificationType(Exception):
	pass

class InvalidSearchOperatorType(Exception):
	pass

class MissingModification(Exception):
	pass

class MissingSearchFilter(Exception):
	pass

class UnsupportedAttribute(Exception):
	pass

class MissingNameAttribute(Exception):
	pass

class MissingParameters(Exception):
	pass

class UnexpectedAttributeType(Exception):
	pass

class ConflictingObject(Exception):
	pass
