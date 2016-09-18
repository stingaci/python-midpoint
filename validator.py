from logger import Logger
import midpoint_exceptions
import os 

class Validate():
	def __init__(self, logger):
		self.logger = logger
		self.base = os.path.dirname(os.path.abspath(__file__))

	def check(self, api_type, object_type, *args, **kwargs):
		with open(self.base+'/templates/'+object_type+'.attr', 'r') as template_file:
                                object_attrs = template_file.read().split('\n')
		
		metadata = getattr(self, '_Validate__'+api_type)(*args, **kwargs)

		for attr in metadata:
			if attr not in object_attrs:
				raise midpoint_exceptions.UnsupportedAttribute(" Attribute: " + attr + " is not supported for object of type: " + object_type)
	
	def __get(self, *args, **kwargs):
		pass
	def __create(self, *args, **kwargs):
		try: 
			name = args[0]
			metadata = args[1]
			if not isinstance(name, str):
				raise midpoint_exceptions.UnexpectedAttributeType("Attribute: name is not a string")	
			elif not isinstance(metadata,dict):
				raise midpoint_exceptions.UnexpectedAttributeType("Attribute: metadata is not a dictionary")	
		except IndexError:
			raise midpoint_exceptions.MissingParameters("Create API must be called with the following parameters: (name, metadata)") 
		return metadata 

	def __modify(self, *args, **kwargs):
		try: 
			oid = args[0]
			metadata = args[1]
			if not isinstance(metadata,dict):
				raise midpoint_exceptions.UnexpectedAttributeType("Attribute: metadata is not a dictionary")	
			with open(self.base+'/templates/modification.types', 'r') as template_file:
					mod_types = template_file.read().split('\n')
			if metadata['modification_type'] not in mod_types:
				raise midpoint_exceptions.InvalidModificationType("Invalid modification type: " + metadata['modification_type'])
			return metadata['modification']
		except KeyError as key:
			raise midpoint_exceptions.MissingModification("Missing modification field: " + str(key))
	def __search(self, *args, **kwargs):
		try: 
			metadata = args[0]
			if not isinstance(metadata,dict):
				raise midpoint_exceptions.UnexpectedAttributeType("Attribute: metadata is not a dictionary")	

			with open(self.base+'/templates/search_operator.types', 'r') as template_file:
					search_op_types = template_file.read().split('\n')
			if metadata['search_operator'] not in search_op_types:
				raise midpoint_exceptions.InvalidSearchOperatorType("Invalid search operator type: " + metadata['search_operator'])
			return metadata['search_filter']
		except KeyError as key:
			raise midpoint_exceptions.MissingSearchFilter("Missing search filter entry: " + str(key))
		pass
	def __delete(self, *args):
		pass
		 
