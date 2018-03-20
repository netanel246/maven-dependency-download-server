import sys
import os
import subprocess
import shutil
from colorama import init
init()
from colorama import Fore, Back, Style
import uuid

def main(argv):
	initialize_internals()
	
	initialize_users_dependenies_dir(argv[0])
def run():
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

def initialize_internals():
	dirname = os.path.dirname(os.path.realpath(__file__))
	internals_path = os.path.join(dirname, 'internal')
	
	settings_path = create_mvn_settings(internals_path)
	
	subprocess.Popen(r'mvn dependency:go-offline -s {}'.format(settings_path), cwd=internals_path, shell=True)

def initialize_users_dependenies_dir(users_pom_path):
	dirname = os.path.dirname(os.path.realpath(__file__))
	temp_dir = os.path.join(dirname, str(uuid.uuid4()))
	os.makedirs(temp_dir)

	temp_pom_path = os.path.join(temp_dir, 'pom.xml')
	
	temp_settings_path = create_mvn_settings(temp_dir)
	
	with open(users_pom_path, 'r') as users_pom:
		with open(temp_pom_path, 'w') as temp_pom:
			temp_pom.write(users_pom.read())
	
	subprocess.Popen(r'mvn dependency:go-offline -s {}'.format(temp_settings_path), cwd=temp_dir, shell=True)

	



def create_mvn_settings(settings_directory, m2_directory=None):
	if m2_directory is None:
		m2_directory = settings_directory
		
	with open('settings.xml', 'r') as settings_file:
		settings_data = settings_file.read().format(m2_directory)
		new_settings_path = os.path.join(settings_directory, 'settings.xml')
		with open(new_settings_path, 'w') as new_settings:
			new_settings.write(settings_data)
		return new_settings_path
			
		
	
	
if __name__ == '__main__':
	main(sys.argv[1:])
	
