from logger import Logger
import midpoint_exceptions
import os 

class Validate():
	def __init__(self, logger):
		self.logger = logger
		self.base = os.path.dirname(os.path.abspath(__file__))

	def check(self, api_type, object_type, input_dict):
		with open(self.base+'/templates/'+object_type+'.attr', 'r') as template_file:
                                user_attrs = template_file.read().split('\n')
		
		input_dict = getattr(self, '_Validate__'+api_type)(input_dict)

		for attr in input_dict:
			if attr not in user_attrs:
				self.logger.write(Logger.FAIL, " Attribute: " + attr + " is not supported for object of type: " + object_type)
	
	def __get(self, input_dict):
		pass
	def __create(self, input_dict):
		if 'name' not in input_dict:
			self.logger.write(Logger.FAIL, "Attribute: name is missing for object of type: User")	
	def __modify(self, input_dict):
		try: 
			with open(self.base+'/templates/modification.types', 'r') as template_file:
					mod_types = template_file.read().split('\n')
			if input_dict['modification_type'] not in mod_types:
				raise midpoint_exceptions.InvalidModificationType("Invalid modification type: " + input_dict['modification_type'])
			return input_dict['modification']
		except KeyError as key:
			raise midpoint_exceptions.MissingModification("Missing modification field: " + str(key))
	def __search(self, input_dict):
		try: 
			with open(self.base+'/templates/search_operator.types', 'r') as template_file:
					search_op_types = template_file.read().split('\n')
			if input_dict['search_operator'] not in search_op_types:
				raise midpoint_exceptions.InvalidSearchOperatorType("Invalid search operator type: " + input_dict['search_operator'])
			return input_dict['search_filter']
		except KeyError as key:
			raise midpoint_exceptions.MissingSearchFilter("Missing search filter entry: " + str(key))
		pass
	def __delete(self, input_dict):
		pass
		 
