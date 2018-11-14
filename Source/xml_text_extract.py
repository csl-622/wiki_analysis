'''

	Purpose: To clean xml wiki text.
	Date: 13/11/18
	Author: Vaibhav Chopra

'''

from lxml import etree
import os

def check_file_exist(file_path):
	return os.path.exists(file_path)

def check_folder_exist(folder_path):
	return os.path.isdir(folder_path)

path_to_xml_file = 'text.xml'
output_path = 'output'

if check_file_exist(path_to_xml_file) is False:
	print(path_to_xml_file + 'does not exist')
	exit()

if check_folder_exist(output_path) is False:
	os.mkdir(output_path)

count = 0
for event, element in etree.iterparse(path_to_xml_file, tag="text"):
	string = etree.tostring(element)
	string_utf8 = string.decode('utf-8', 'ignore')
	with open(os.path.join(output_path,str(count)+'.txt'), "w") as text_file:
		text_file.write(string_utf8[6:-9])
	element.clear()
	count += 1