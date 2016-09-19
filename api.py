import os
import ConfigParser
from logger import Logger
import objects
import methods 
import templates
import xml_parser
import validator
import functools
import midpoint_exceptions


def decorate_get_one(func):
	def inner(*args, **kwargs):
		return get_one(func(*args, **kwargs))
	return inner

def get_one(li):
	if len(li) == 1:
		return li[0]
	elif len(li) == 0:
		return None
	elif len(li) > 1:
		print "ERROR"

class Type():
	CREATE = "create"
	MODIFY = "modify"
	SEARCH = "search"
	DELETE = "delete"
	GET = "get"

class Api():
	def __init__(self, cfg_file='./midpoint.cfg', logFile=None):
		self.logger = Logger()
		self.connection = {}
		self.validate = validator.Validate(self.logger)
		self.read_config(cfg_file)
	
	def read_config(self, cfg_file):
		if os.path.isfile(cfg_file):
			midpointConfig = ConfigParser.ConfigParser()
			midpointConfig.read(cfg_file)
			
			# Define required sections and respective attributes 
			required_sections = ['host', 'credentials']
			required_attrs = {}
			required_attrs['host'] = ['server','port']
			required_attrs['credentials'] = ['username','password']
			
			# Parse Config File
			for section in midpointConfig.sections():
				if section not in required_sections:
					self.logger.write(Logger.FAIL, "Failed reading configuration file: defined section " + section + " is not supported")
				else: 
					self.connection[section] = {}
					for (attr, value) in midpointConfig.items(section):
						if attr not in required_attrs[section]:
							self.logger.write(Logger.FAIL,"Failed reading configuration file: defined attribute: " + attr + " in section: " + section  + " is not supported")
						if not value:
							self.logger.write(Logger.FAIL,"Failed reading configuration file: defined attribute: " + attr + " in section: " + section  + " has an empty value")
						self.connection[section][attr] = value

			# Craft Base Request Url
			self.url = 'http://'+self.connection['host']['server']+':'+self.connection['host']['port']+'/midpoint/ws/rest/'
		else:
			self.logger.write(Logger.FAIL, "Failed reading configuration file: " + cfg_file + " was not found")

	#####################
	### Payload Craft ###
	#####################
	def __craft_search_filter(self, search_filter):
		return templates.Template(templates.Type.SEARCH, search_filter).get_payload()

	def __craft_modification(self, modification):
		return templates.Template(templates.Type.MODIFY, modification).get_payload()

	def __craft_create(self, object_type, metadata):
		return templates.Template(templates.Type.CREATE+object_type, metadata).get_payload()

	######################
	### Object methods ###
	######################
	def __get(self, object_constructor, object_type, *args, **kwargs):
		metadata = self.__get_request(object_type, *args, **kwargs)
		if metadata:
			return object_constructor(self, metadata)
		return None

	def __get_request(self, object_type, object_oid):
		url = self.url + object_type + '/' + object_oid
		request = methods.Method(url,self.connection['credentials'],methods.Type.GET) 
		response = request.execute()

		# Prase response and return
		return xml_parser.Parser(response.content).metadata

	def __search(self, object_constructor, object_type, *args, **kwargs):
		self.validate.check(Type.SEARCH, object_type, *args, **kwargs)
		metadatas = self.__search_request(object_type, *args, **kwargs)
		return [object_constructor(self, m) for m in metadatas]

	def __search_request(self, object_type, search_filter):
		# Make request
		url = self.url + object_type + '/search' 
		request = methods.Method(url,self.connection['credentials'],methods.Type.POST, payload=(self.__craft_search_filter(search_filter))) 
		response = request.execute()
		data = xml_parser.Parser(response.content).metadata
		if data:
                        ## This is particular to midPoint as it returns multiple results with the top-level tag as object 
                        data = data['object']
                elif not len(data):
                        data = []
                if isinstance(data, dict):
                        data = [data]
		# Prase response  and return
		return data 

	def __modify(self, object_type, *args, **kwargs):
		self.validate.check(Type.MODIFY, object_type, *args, **kwargs)
		self.__modify_request(object_type, *args, **kwargs)

	def __modify_request(self, object_type, object_oid, modification):
		url = self.url + object_type + '/' + object_oid
		request = methods.Method(url,self.connection['credentials'],methods.Type.POST, payload=self.__craft_modification(modification)) 
		response = request.execute()
		return response
	
	def __create(self, object_constructor, object_type, *args, **kwargs):
		self.validate.check(Type.CREATE, object_type, *args, **kwargs)
		if getattr(self, "search_" +object_type[:-1])({'search_operator':'and','search_filter':{'name':args[0]}}) == None:
			obj_oid = self.__create_request(object_type, *args, **kwargs)
			return self.__get(object_constructor, object_type, obj_oid)
		else:
			raise midpoint_exceptions.ConflictingObject("Found conflicting object with name: " + args[0])
	
	def __create_request(self, object_type,name, metadata):
		url = self.url + object_type 
		metadata['name'] = name
		request = methods.Method(url,self.connection['credentials'],methods.Type.POST, payload=self.__craft_create(object_type,metadata)) 
		response = request.execute()
		return response.headers['location'].split('/')[-1]

	##################
	##### Public #####
	##################

	### Create ####
	# Input: (name, metadata)##
	def create_user(self, *args, **kwargs):
		user = self.__create(objects.User, objects.Type.USER, *args, **kwargs)
		return user

	def create_role(self, *args, **kwargs):
		return self.__create(objects.Role, objects.Type.ROLE, *args, **kwargs)

	### Get ###
	# Input (oid)#
	def get_role(self,*args, **kwargs):
		return self.__get(objects.Role, objects.Type.ROLE, *args, **kwargs)

	def get_user(self,*args, **kwargs):
		return self.__get(objects.User, objects.Type.USER, *args, **kwargs)

	def get_shadow(self,*args, **kwargs):
		return self.__get(objects.Shadow, objects.Type.SHADOW, *args, **kwargs)

	def get_resource(self,*args, **kwargs):
		return self.__get(objects.Resource, objects.Type.RESOURCE, *args, **kwargs)

	### Modify ###
	# Input ({'modification_type': 'add|delete|replace','modification':{'object_attribute':'attribute_value'}})
	def modify_role(self, *args, **kwargs):
		return self.__modify(objects.Type.ROLE, *args, **kwargs) 
	def modify_user(self, *args, **kwargs):
		return self.__modify(objects.Type.USER, *args, **kwargs) 
	def modify_resource(self, *args, **kwargs):
		return self.__modify(objects.Type.RESOURCE, *args, **kwargs) 
	def modify_shadow(self, *args, **kwargs):
		return self.__modify(objects.Type.SHADOW, *args, **kwargs) 

	### Search ###
	# Input: ({'search_operator':'and|or', 'search_filter':{'object_attribute':'attribute_value', 'another_object_attribute':'attribute_value'}})
	def search_roles(self, *args, **kwargs):
		return self.__search(objects.Role, objects.Type.ROLE, *args, **kwargs)
	def search_users(self, *args, **kwargs):
		return self.__search(objects.User, objects.Type.USER, *args, **kwargs)
	def search_shadows(self, *args, **kwargs):
		return self.__search(objects.Shadow, objects.Type.SHADOW, *args, **kwargs)
	def search_resources(self, *args, **kwargs):
		return self.__search(objects.Resource, objects.Type.RESOURCE, *args, **kwargs)

	search_role = decorate_get_one(search_roles)
	search_user = decorate_get_one(search_users)
	search_shadow = decorate_get_one(search_shadows)
	search_resource = decorate_get_one(search_resources)


