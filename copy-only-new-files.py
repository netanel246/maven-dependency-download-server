import os
import shutil
from colorama import init
init()
from colorama import Fore, Back, Style


dependencies_path = "C:\\Users\\6\\Desktop\\maven-imports\\jersey\\m2"
maven_base_libs_path = "C:\\Users\\6\\Desktop\\Maven-imports\\base-maven-libs"
output_path = "C:\\Users\\6\\Desktop\\maven-imports\\jersey\\dependencies"

dependencies_with_base_libs = []
for root, directories, filenames in os.walk(dependencies_path):
	for filename in filenames: 
		dependencies_with_base_libs.append(os.path.join(root.replace(dependencies_path, ''), filename))
		

maven_base_libs = []
for root, directories, filenames in os.walk(maven_base_libs_path):
	for filename in filenames: 
		maven_base_libs.append(os.path.join(root.replace(maven_base_libs_path, ''), filename))

dependencies = [lib for lib in dependencies_with_base_libs if lib not in maven_base_libs]

if os.path.exists(output_path + '\\tree'):
	shutil.rmtree(output_path + '\\tree')
if os.path.exists(output_path + '\\files'):	
	shutil.rmtree(output_path + '\\files')

for dependency in dependencies:
	dir, filename = os.path.split(dependency)
	
	input_file = dependencies_path + dependency
	output_tree_dir = output_path +'\\tree'+ dir
	output_files_dir = output_path + '\\files'
	
	if not os.path.exists(output_tree_dir):
		os.makedirs(output_tree_dir)	
		
	shutil.copy(input_file, output_tree_dir)
	
	if not os.path.exists(output_files_dir):
		os.makedirs(output_files_dir)
	
 	if os.path.exists(output_files_dir + '\\' + filename):
		print dir + '\\'
		print Fore.RED + filename
		print(Style.RESET_ALL) + ' already exists!'

	shutil.copy(input_file, output_files_dir)

print 'Copied {} files to dependencies directory'.format(len(dependencies))
	
