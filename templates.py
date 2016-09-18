import os 
import objects

class Type:
	SEARCH='search'
	MODIFY='modify'
	CREATE='create'

class Template:
	def __init__(self, template_type, template_dict=None):
		base = os.path.dirname(os.path.abspath(__file__))
		if template_type == Type.SEARCH:
			with open(base+'/templates/search_template.xml', 'r') as template_file:
				self.template_content = template_file.read()
		elif template_type == Type.MODIFY:
			with open(base+'/templates/modify_template.xml', 'r') as template_file:
				self.template_content = template_file.read()
		elif template_type == Type.CREATE+objects.Type.USER:
			template_type = Type.CREATE
			with open(base+'/templates/create_user_template.xml', 'r') as template_file:
				self.template_content = template_file.read()
		elif template_type == Type.CREATE+objects.Type.ROLE:
			template_type = Type.CREATE
			with open(base+'/templates/create_role_template.xml', 'r') as template_file:
				self.template_content = template_file.read()
		getattr(self, '_Template__'+template_type)(template_dict)

	def __craft_template(self, payload):
		self.payload = self.template_content.replace('%payload%', payload)

	def __search(self, template_dict):
		payload = ''
		# Empty query, search all
		if template_dict is None:
			return self.__craft_template(payload)
		else:
			payload = '<filter>'
			payload = payload + '<q:' + template_dict['search_operator'] +'>'
			for (path, value) in template_dict['search_filter'].iteritems():
				payload = payload + '<q:equal><q:path>{0}</q:path><q:value>{1}</q:value></q:equal>'.format(path,value)
			payload = payload + '</q:' + template_dict['search_operator'] +'>'
			payload = payload + '</filter>'
			return self.__craft_template(payload)

	#TODO add suport for multiple mods at once
	def __modify(self, template_dict):
		for (path, value) in template_dict['modification'].iteritems(): 
			payload = '<apit:itemDelta><t:modificationType>{0}</t:modificationType><t:path>{1}</t:path><t:value>{2}</t:value></apit:itemDelta>'.format(template_dict['modification_type'], path, value) 
		return self.__craft_template(payload)
	
	def __create(self, template_dict):
		extension = {}
		payload = ''
		for (attr, value) in template_dict.iteritems():
			if 'extension' in attr:
				extension[attr.split('/')[1]] = value
			else:
				payload += '<' + attr + '>' + value + '</' + attr + '>'
		if extension != {}:
			payload += '<extension>'
		for (attr, value) in extension.iteritems():
				payload += '<' + attr + '>' + value + '</' + attr + '>'
		if extension != {}:
			payload += '</extension>'
		return self.__craft_template(payload)	

	def get_payload(self):
		return self.payload
			
			
