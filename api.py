import os
import ConfigParser
from logger import Logger
import objects
import methods 
import templates
import xml_parser


class Api():
	def __init__(self, cfg_file='./midpoint.cfg', logFile=None):
		self.logger = Logger()
		self.connection = {}
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

	def __craft_search_filter(self, search_filter):
		return templates.Template(templates.Type.SEARCH, search_filter).get_payload()

	def __craft_modification(self, modification):
		return templates.Template(templates.Type.MODIFY, modification).get_payload()

	def __get_object(self, object_type, object_oid):
		url = self.url + object_type + '/' + object_oid
		request = methods.Method(url,self.connection['credentials'],methods.Type.GET) 
		response = request.execute()

		# Prase response  and return
		return xml_parser.Parser(response.content).metadata

	def __search_object(self, object_type, search_filter):
		# Make request
		url = self.url + object_type + '/search' 
		request = methods.Method(url,self.connection['credentials'],methods.Type.POST, payload=(self.__craft_search_filter(search_filter))) 
		response = request.execute()

		# Prase response  and return
		data = xml_parser.Parser(response.content).metadata
		if data:
			data = data['object']
			#if isinstance(data, dict):
			#	data = [data]
		elif not len(data):
			data = {}
		return data 
	
	def __modify_object(self, object_type, object_oid, modification):
		url = self.url + object_type + '/' + object_oid
		request = methods.Method(url,self.connection['credentials'],methods.Type.POST, payload=self.__craft_modification(modification)) 
		response = request.execute()
		return response

	def get_user(self,user_oid):
		return objects.User(self, self.__get_object(objects.Type.USER, user_oid))

	def modify_user(self, user_oid, modification):
		return self.__modify_object(objects.Type.USER, user_oid, modification)	

	def search_users(self,search_filter, unique=False):
		if not unique:
			return [objects.User(self, user) for user in self.__search_object(objects.Type.USER, search_filter)]
		else:
			return objects.User(self, self.__search_object(objects.Type.USER, search_filter))

	def get_role(self,role_oid):
		return objects.Role(self, self.__get_object(objects.Type.ROLE, role_oid))

	def modify_role(self, role_oid, modification):
		return self.__modify_object(objects.Type.ROLE, role_oid, modification)	

	def search_roles(self,search_filter, unique=False):
		if not unique:
			return [objects.Role(self, role) for role in self.__search_object(objects.Type.ROLE, search_filter)]
		else:
			return objects.Role(self, self.__search_object(objects.Type.ROLE, search_filter))

	def get_shadow(self,shadow_oid):
		return objects.Shadow(self, self.__get_object(objects.Type.SHADOW, shadow_oid))

	def modify_shadow(self, shadow_oid, modification):
		return self.__modify_object(objects.Type.SHADOW, shadow_oid, modification)	

	def search_shadows(self,search_filter, unqiue=False):
		if not unique: 
			return [objects.Shadow(self, shadow) for shadow in self.__search_object(objects.Type.SHADOW, search_filter)]
		else:
			return objects.Shadow(self, self.__search_object(objects.Type.SHADOW, search_filter))
	
	def get_resource(self,resource_oid):
		return objects.Resource(self, self.__get_object(objects.Type.RESOURCE, resource_oid))

	def modify_resource(self, resource_oid, modification):
		return self.__modify_object(objects.Type.RESOURCE, resource_oid, modification)	

	def search_resources(self,search_filter, unqiue=False):
		if not unqiue:
			return [objects.Resource(self, resource) for resource in self.__search_object(objects.Type.RESOURCE, search_filter)]
		else: 
			return objects.Resource(self, self.__search_object(objects.Type.RESOURCE, search_filter))
