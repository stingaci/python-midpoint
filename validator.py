from logger import Logger
import os 
class Type():
	CREATE="create_"

class Validate():
	def __init__(self, logger):
		self.logger = logger

	def check(self, input_type, input_dict):
		return getattr(self, '_Validate__'+input_type)(input_dict)
		
	
	def __create_users(self, input_dict):	
		base = os.path.dirname(os.path.abspath(__file__))
		with open(base+'/templates/user.attr', 'r') as template_file:
                                user_attrs = template_file.read().split('\n')

		if 'name' not in input_dict:
			self.logger.write(Logger.FAIL, "Failed creating user. Attribute: name is missing")	

		for attr in input_dict:
			if attr not in user_attrs:
				self.logger.write(Logger.FAIL, "Failed creating user. Attribute: " + attr + " is not supported")
		
		return True

	def __create_roles(self, input_dict):	
		base = os.path.dirname(os.path.abspath(__file__))
		with open(base+'/templates/role.attr', 'r') as template_file:
                                user_attrs = template_file.read().split('\n')
		
		if 'name' not in input_dict:
			self.logger.write(Logger.FAIL, "Failed creating role. Attribute: name is missing")	

		for attr in input_dict:
			if attr not in user_attrs:
				self.logger.write(Logger.FAIL, "Failed creating role. Attribute: " + attr + " is not supported")	
		
		return True
