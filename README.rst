===========================================
python-midpoint 
===========================================

Overview
========
This is a python library for interacting with midpoint. It's actually a warpper around midPoint's existing RESTfull API and as such perfromance may suffer. 


Exiting Features
========
As of the last commit there is support for the following objects:
	* Users
	* Roles
	* Resources 
	* Shadows 

Most of the operations are limitied to reading existing objects and modifying them via MidPoint's itemDelta mechanism.

Coming Soon 
========
	* Creating New Objects 
	* Deleting Existing Objects 
	* Wrapers for Object functions such as (most of these can be done today with existing schema):
		- Assign To Role 
		- Check User Role Membership
		- etc
