import api

a = api.Api('midpoint.cfg')

print a.search_role({'search_operator':'and', 'search_filter':{'name':'cpe_users'}}).metadata
for role in a.search_roles({'search_operator':'and', 'search_filter':{'roleType':'BU'}}):
	print role.metadata



