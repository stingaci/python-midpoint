import StringIO
import xml.etree.ElementTree as ElementTree
from lxml import etree, objectify


class Parser():
	def __init__(self, raw_xml):
		striped_xml = XmlnsStriper(raw_xml).stripped
		root = ElementTree.XML(striped_xml)
		self.metadata = XmlDictConfig(root)

class XmlnsStriper():
	def __init__(self, xml):
		parser = etree.XMLParser(remove_blank_text=True)
		tree = etree.parse(StringIO.StringIO(xml), parser)
		root = tree.getroot()
		####    
		for elem in root.getiterator():
			if not hasattr(elem.tag, 'find'): continue  # (1)
			i = elem.tag.find('}')
			if i >= 0:
				elem.tag = elem.tag[i+1:]
		objectify.deannotate(root, cleanup_namespaces=True)
		####
		self.stripped = etree.tostring(tree)

class XmlDictConfig(dict):
	'''
	Example usage:

	>>> tree = ElementTree.parse('your_file.xml')
	>>> root = tree.getroot()
	>>> xmldict = XmlDictConfig(root)

	Or, if you want to use an XML string:

	>>> root = ElementTree.XML(xml_string)
	>>> xmldict = XmlDictConfig(root)

	And then use xmldict for what it is... a dict.

	This makes a number of assumptions:
	1. You don't need the top level tag as a key to this dictonary 
	2. That if the current tag has text value, it won't have any attributes 
	3. The previous point can be fixed by adding text value to a dict via the 
	__content__ key. However for the purposes of this use case, this is not required
	4. Multiple tags that have a matching name will be indexed in a dict via the 
	tag name and it's value will be a list of all the objects within that tag
	'''
	def __init__(self, parent_element):
		if parent_element.items():
			self.update(dict(parent_element.items()))
		
		child_count = {}
		for child in parent_element:
			if child.tag in child_count:
				child_count[child.tag] += 1
			else:
				child_count[child.tag] = 0
		
		for child in parent_element:
			if child_count[child.tag] > 0:
				if child.tag not in self:
					if len(child):
						self[child.tag] = [XmlDictConfig(child)]	
					else:
						if child.text == None:
							self[child.tag] = [dict(child.items())]	
						else:
							self[child.tag] = [child.text]	
				else: 
					if len(child):
						self[child.tag].append(XmlDictConfig(child))
					else:
						if child.text == None:
							self[child.tag].append(dict(child.items()))
						else:
							self[child.tag].append(child.text)
			else: 
				if len(child):
					self[child.tag] = XmlDictConfig(child)
				else:
					self[child.tag] = child.text
					if child.text == None:
						self[child.tag] = dict(child.items())
					else:
						self[child.tag] = child.text
