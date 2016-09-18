class Type:
        USER='users'
        ROLE='roles'
        SHADOW='shadows'
        RESOURCE='resources'

class GenericObject:
	def __init__(self, api, metadata):
		self.metadata = metadata 
		self.api = api

class User(GenericObject):
	def __init__(self, api, metadata):
		GenericObject.__init__(self, api, metadata)
	
	def modify(self, modification):
		self.api.modify_user(self.metadata['oid'], modification)
	
	def has_account(self, resource_name=None, resource_oid=None, resource_object=None):
		pass
	
	def has_indirect_account(self, resource_name=None, resource_oid=None, resource_object=None):
		if not (resource_name or resource_oid or resource_object):
			return False
		if resource_name:
			resource = self.api.search_resource({'search_operator':'and', 'search_filter':{'name':resourceName}})
		elif resource_oid:
			resource = Resource(self.api, {'oid':resource_oid})
		elif resource_object:
			resource = resource_object

		if resource and 'linkRef' in self.metadata:
			for shadowRef in self.metadata['linkRef']:
				shadow = self.api.get_shadow(shadowRef['oid'])
				for resourceRef in shadow.metadata['resourceRef']:
					if resource.metadata['oid'] == resourceRef['oid']:
						return True
		
		return False
	
	def assign_role(self, role_name=None, role_oid=None, role_object=None):
		if not (role_name or role_oid or role_object):
			return False
		if role_name:
			role = self.api.search_role({'search_operator':'and', 'search_filter':{'name':role_name}})
		elif role_oid:
			role = Role(self.api, {'oid':role_oid})
		elif role_object:
			role = role_object

		if role: 
			self.modify({'modification_type': 'add','modification':{'assignment':'<targetRef oid="'+role.metadata['oid']+ '" type="RoleType"/>'}})
			return True
		return False

class Role(GenericObject):
	def __init__(self, api, metadata):
		GenericObject.__init__(self, api, metadata)
	
	def modify(self, modification):
		self.api.modify_role( self.metadata['oid'], modification)

	def assign_role(self, role_name=None, role_oid=None, role_object=None):
		if not (role_name or role_oid or role_object):
			return False
		if role_name:
			role = self.api.search_role({'search_operator':'and', 'search_filter':{'name':role_name}})
		elif role_oid:
			role = Role(self.api, {'oid':role_oid})
		elif role_object:
			role = role_object

		if role: 
			self.modify({'modification_type': 'add','modification':{'assignment':'<targetRef oid="'+role.metadata['oid']+ '" type="RoleType"/>'}})
			return True
		return False

class Shadow(GenericObject):
	def __init__(self, api, metadata):
		GenericObject.__init__(self, api, metadata)

class Resource(GenericObject):
	def __init__(self, api, metadata):
		GenericObject.__init__(self, api, metadata)
