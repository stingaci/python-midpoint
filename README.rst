===========================================
python-midpoint 
===========================================

Overview
--------
This is a python library for interacting with midpoint. It's actually a wrapper around midPoint's existing RESTfull API and as such performance may suffer. 


Exiting Features
----------------
As of the last commit there is support for the following objects:

* Users
* Roles
* Resources 
* Shadows 

Most of the operations are limited to reading existing objects and modifying them via MidPoint's itemDelta mechanism. Error handling is very poor at the moment and the use of this library assumes that it's used behind a client (yet to be developed) as any encountered errors will result in an error message and a sys.exit() call. This will be addressed in future iterations. 

Search and Modify
-----------------

As of the latest commit there is no validation for the submitted search filters and modifications. This will be improved in the future. 

Search filters for search operations are defined as dicts of the following format:

{'search_operator':'and|or', 'search_filter':{'object_attribute':'attribute_value', 'another_object_attribute':'attribute_value'}}

Modifications are defined as follows (for now only one attribute modification is allowed per API call):

{'modification_type': 'add|delete|replace','modification':{'object_attribute':'attribute_value'}}

User & Role Create
------------------

Support for creation of users and roles is now supported and the allowed initial attributes for creation can be found in templates/role|user.attr. The validator will ensure that any attributes passed in must be contained within those files. Extension attributes must be preceded with extension/. An example call can be as follows:

create_role("my_new_role", {"requestable":"true"})


Future
------

* Support for object deletion 
* Support for resource creation (validation of attributes will be a hassle)
* Proper error handling for both input validation as well as HTTP response handling 
* A command client interface
* Test suites

