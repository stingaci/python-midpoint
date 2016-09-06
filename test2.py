import api

a = api.Api()
#a.get_user('c2205552-918c-49a4-a6df-1ce09004099c')
#for user in a.search_users({'search_operator': 'and', 'search_filter': {'givenName':'Flower'}}):
#	user.modify({'modification_type': 'replace', 'modification':{'givenName:': 'Florin'}}) 

#for role in a.search_roles({'search_operator': 'and', 'search_filter': {'name':'test_role'}}):
#	role.modify({'modification_type': 'replace', 'modification':{'roleType:': 'BU2'}}) 

resource = a.search_resources({'search_operator': 'and', 'search_filter': {'name':'Corporate Active Directory'}})[0]
user = a.search_users({'search_operator': 'and', 'search_filter': {'name':'box_admin-sd'}})[0]

print user.assign_role(role_name='test_role')

#if 'linkRef' in user.metadata:
#	for shadowRef in user.metadata['linkRef']:
#		shadow = a.get_shadow(shadowRef['oid'])
#		for resourceRef in shadow.metadata['resourceRef']:
#			if resource.metadata['oid'] == resourceRef['oid']:
#				print "User has account on resource"

#print "User has jack shit"
