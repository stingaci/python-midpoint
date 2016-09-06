import StringIO
import xml.etree.ElementTree as ElementTree
from lxml import etree, objectify

from lxml import etree, objectify

class Parser():
	def __init__(self, raw_xml):
		striped_xml = XmlnsStriper(raw_xml).stripped
		root = ElementTree.XML(striped_xml)
		self.metadata = XmlDictConfig(root)
def formatXML(parent):
	ret = {}
	if parent.items(): ret.update(dict(parent.items()))
	if parent.text: ret['__content__'] = parent.text
	if ('List' in parent.tag):
		ret['__list__'] = []
		for element in parent:
			ret['__list__'].append(formatXML(element))
	else:
		for element in parent:
			ret[element.tag] = formatXML(element)
	return ret


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


class XmlListConfig(list):
	def __init__(self, aList):
		for element in aList:
			if len(element):
			# treat like dict
				if len(element) == 1 or element[0].tag != element[1].tag:
					self.append(XmlDictConfig(element))
			# treat like list
				elif element[0].tag == element[1].tag:
					self.append(XmlListConfig(element))
			elif element.text:
				text = element.text.strip()
				if text:
					self.append(text)

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
	'''
	def __init__(self, parent_element):
		childrenNames = []
		for child in parent_element.getchildren():
			childrenNames.append(child.tag)

		if parent_element.items():
			self.update(dict(parent_element.items()))

		i = 0
		for element in parent_element:
			# Midpoint dose not return uniquely identified objects and thus
			# an xml containting multiple objects will overwrite eachother
			# in the final dict and so we must ensure that we assign unique
			# ids to each element 
			if len(element):
				# treat like dict - we assume that if the first two tags
				# in a series are different, then they are all different.
				if len(element) == 1 or element[0].tag != element[1].tag:
					aDict = XmlDictConfig(element)
				# treat like list - we assume that if the first two tags
				# in a series are the same, then the rest are the same.
				else:
				# here, we put the list in dictionary; the key is the
				# tag name the list elements all share in common, and
				# the value is the list itself 
					aDict = {element[0].tag: XmlListConfig(element)}
				# if the tag has attributes, add those to the dict
				if element.items():
					aDict.update(dict(element.items()))
				if childrenNames.count(element.tag) > 1:
					try:
						currentValue = self[element.tag]
						currentValue.append(aDict)
						self.update({element.tag: currentValue})
					except: #the first of its kind, an empty list must be created
						self.update({element.tag: [aDict]}) #aDict is written in [], i.e. it will be a list
				else:
					self.update({element.tag: aDict})
			# this assumes that if you've got an attribute in a tag,
			# you won't be having any text. This may or may not be a 
			# good idea -- time will tell. It works for the way we are
			# currently doing XML configuration files...
			elif element.items():
				self.update({element.tag: dict(element.items())})
				self[element.tag].update({"__Content__":element.text})
			# finally, if there are no child tags and no attributes, extract
			# the text
			else:
				self.update({element.tag: element.text})

		for elem in self:
			if isinstance(self[elem], dict):
				self[elem] = [self[elem]]

