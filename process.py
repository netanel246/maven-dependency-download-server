import sys
import os
import subprocess
import shutil
import uuid


def do_run(pom, output_directory):
    internals_path = initialize_internals()
    internals_m2 = os.path.join(internals_path, '.m2')

    temp_path = initialize_users_dependenies_dir(internals_path, pom)
    temp_m2 = os.path.join(temp_path, '.m2')

    run(internals_m2, temp_m2, output_directory)


def run(maven_base_libs_path, dependencies_path, output_path):
    dependencies_with_base_libs = []
    for root, directories, filenames in os.walk(dependencies_path):
        for filename in filenames:
            dependencies_with_base_libs.append(os.path.join(root.replace(dependencies_path + '\\', ''), filename))

    maven_base_libs = []
    for root, directories, filenames in os.walk(maven_base_libs_path):
        for filename in filenames:
            maven_base_libs.append(os.path.join(root.replace(maven_base_libs_path + '\\', ''), filename))

    dependencies = [lib for lib in dependencies_with_base_libs if lib not in maven_base_libs]

    output_tree = os.path.join(output_path, 'tree-' + str(uuid.uuid4())[:8])
    print('writing to ' + output_tree)

    for dependency in dependencies:
        dir, filename = os.path.split(dependency)

        input_file = os.path.join(dependencies_path, dependency)

        output_tree_dir = os.path.join(output_tree, dir)

        if not os.path.exists(output_tree_dir):
            os.makedirs(output_tree_dir)

        shutil.copy2(input_file, output_tree_dir)

    print('Copied {} files to dependencies directory'.format(len(dependencies)))


def initialize_internals():
    dirname = os.path.dirname(os.path.realpath(__file__))
    internals_path = os.path.join(dirname, 'internal')

    settings_path = create_mvn_settings(internals_path)

    print('importing missing base dependencies')
    output = subprocess.check_output(r'mvn dependency:go-offline -s {}'.format(settings_path), cwd=internals_path,
                                     shell=True)
    print(output)

    return internals_path


def initialize_users_dependenies_dir(internals_path, users_pom):
    temp_dir = os.path.join(internals_path, str(uuid.uuid4()))
    os.makedirs(temp_dir)

    temp_pom_path = os.path.join(temp_dir, 'pom.xml')

    temp_settings_path = create_mvn_settings(temp_dir)

    with open(temp_pom_path, 'w') as temp_pom:
        temp_pom.write(users_pom)

    print('copying base depedencies')
    shutil.copytree(os.path.join(internals_path, '.m2'), os.path.join(temp_dir, '.m2'))

    print('downloading new dependencies')
    output = subprocess.check_output(r'mvn dependency:go-offline -s {}'.format(temp_settings_path), cwd=temp_dir,
                                     shell=True)
    print(output)

    return temp_dir


def create_mvn_settings(settings_directory, m2_directory=None):
    if m2_directory is None:
        m2_directory = settings_directory

    with open('settings.xml', 'r') as settings_file:
        settings_data = settings_file.read().format(m2_directory)
        new_settings_path = os.path.join(settings_directory, 'settings.xml')
        with open(new_settings_path, 'w') as new_settings:
            new_settings.write(settings_data)
        return new_settings_path
