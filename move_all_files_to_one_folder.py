import os

def check_folder_exist(folder_path):
	return os.path.isdir(folder_path)

input_folder = 'wiki_text'
output_folder = 'wiki_text_input_for_concept_graph'

if check_folder_exist(input_folder) is False:
	print(input_folder + 'does not exists')
	exit()

if check_folder_exist(output_folder) is False:
	os.mkdir(output_folder)

A = os.listdir(input_folder)
c = 0
for i in A:
	c += 1
	j = os.path.join(input_folder,i)
	B = os.listdir(j)
	for x in B:
		os.system('cp ' + os.path.join(j,x) + ' ' + os.path.join(output_folder,str(c)+'_'+x))