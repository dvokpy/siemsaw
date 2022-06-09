#!/usr/bin/python3

from distutils.command.config import config
import os
import platform
import subprocess

def os_detector():
    operating_system = platform.system()
    return operating_system

def windows_config_generator():
    config_path = os.getcwd() + '\config'
    try:
        if os.path.exists(config_path) and os.path.exists(os.getcwd() + '\output_dir\\'):
            return config_path
        else:
            chainsaw_bin = input("Enter chainsaw binary absolute path:\n> ")
            config_dscr = open(config_path, 'w')
            config_dscr.write('ChainsawBin:' + chainsaw_bin + "\n")
            output_dir = os.getcwd() + '\output_dir\\'
            config_dscr.write('OutputDir:' + output_dir + "\n")
            mapping_file = ('/'.join((chainsaw_bin.split('\\'))[:-1])) + '\mapping_files\sigma-mapping.yml'
            config_dscr.write('MappingFile:' + mapping_file + "\n")
            default_sigma_rules = ('\\'.join((chainsaw_bin.split('\\'))[:-1])) + '\sigma_rules\\'
            config_dscr.write('DefaultSigmaDirectory:' + default_sigma_rules + "\n")
            os.mkdir(os.getcwd() + '\output_dir\\')
            evtx_repo = os.getcwd() + '\evtx_repo\\'
            config_dscr.write('EvtxRepo:' + evtx_repo + '\n')
            os.mkdir(evtx_repo)
            config_dscr.close()
            return config_path
    except KeyboardInterrupt:
        print("\nUser interuptted Program\nExiting...\n")


def linux_config_generator():
    config_path = os.getcwd() + '/config'
    try:
        if os.path.exists(config_path) and os.path.exists(os.getcwd() + '/output_dir/'):
            return config_path
        else:
            chainsaw_bin = input("Enter chainsaw binary absolute path:\n> ")
            config_dscr = open(config_path, 'w')
            config_dscr.write('ChainsawBin:' + chainsaw_bin + "\n")
            output_dir = os.getcwd() + '/output_dir/'
            config_dscr.write('OutputDir:' + output_dir + "\n")
            mapping_file = ('/'.join((chainsaw_bin.split('/'))[:-1])) + '/mapping_files/sigma-mapping.yml'
            config_dscr.write('MappingFile:' + mapping_file + "\n")
            default_sigma_rules = ('/'.join((chainsaw_bin.split('/'))[:-1])) + '/sigma_rules/'
            config_dscr.write('DefaultSigmaDirectory:' + default_sigma_rules + "\n")
            os.mkdir(os.getcwd() + '/output_dir/')
            evtx_repo = os.getcwd() + '/evtx_repo/'
            config_dscr.write('EvtxRepo:' + evtx_repo + '\n')
            os.mkdir(evtx_repo)
            config_dscr.close()
            return config_path
    except KeyboardInterrupt:
        print("\nUser interuptted Program\nExiting...\n")
        
menu = '1)Chainsaw Hunt\n2)Chainsaw Search\n3)General Chainsaw Man Page\n4)Exit siemsaw\n'

plat = platform.system()
if plat == 'Linux':
    config_path = linux_config_generator()
elif plat == 'Windows':
    config_path = windows_config_generator()
else:
    print('ALERT!!!Unrecognized platform!!!ALERT\n')

def config_var_assign(conf_path):
    file_dsc = open(conf_path, 'r')
    conf_content = file_dsc.readlines()
    chainsaw_binary = ((conf_content[0].split(':'))[1])[:-1]
    output_directory = ((conf_content[1].split(':'))[1])[:-1]
    mapping_directory = ((conf_content[2].split(':'))[1])[:-1]
    sigma_directory = ((conf_content[3].split(':'))[1])[:-1]
    evtx_dir = ((conf_content[4].split(':'))[1])[:-1]
    return chainsaw_binary, output_directory, mapping_directory, sigma_directory, evtx_dir

def evtx_builder():
    evtx_paths = []
    while True:
        try:
            evtx_path = input("Enter your evtx path below:\n> ")
            evtx_paths.append(evtx_path)
            cont_answr = input("Would you like to add another path to your query? Y/N\n> ")
            if cont_answr[0].lower() == 'y':
                continue
            elif cont_answr[0].lower() == 'n':
                break
        except KeyboardInterrupt:
            break
    return evtx_paths
    


saw_bin, output_dir, map_dir, sigma_dir, evtx_directory = config_var_assign(config_path)

while True:
    evtx_answer = input("Manually load evtx files? Y/N\n> ")
    if evtx_answer[0].lower() == 'y':
        evtx_main_paths = evtx_builder()
        break
    elif evtx_answer[0] == 'n':
        evtx_main_paths = []
        evtx_buffer = os.listdir(evtx_directory)
        for path in evtx_buffer:
            evtx_main_paths.append(evtx_directory + path)
        break
    else:
        print('Invalid input\n')
        
print("The current loaded evtx files are:\n")
for path in evtx_main_paths:
    print(path + "\n")
    
def output_cleaner(out_dir):
    files = os.listdir(out_dir)
    for file in files:
        wrking_filepth = out_dir + file
        try:
            if os.path.isdir(wrking_filepth):
                list = os.listdir(wrking_filepth)
                if list:
                    continue
                else:
                    os.rmdir(wrking_filepth)
            file_dr = open(wrking_filepth, 'r')
            content = file_dr.read()
            if not content:
                file_dr.close()
                os.remove(wrking_filepth)
        except FileNotFoundError:
            continue
while True:
    try:
        print(menu)
        user_choice = input('Enter your choice:\n> ')[0]
        if user_choice == '1':
            print("***************\n* TO THE HUNT *\n***************\n")
            default_answer = input("Would you like to use the default sigma rules? Y/N\n> ")
            if default_answer[0].lower() == 'y':
                for evtx_path in evtx_main_paths:
                    if plat == 'Linux':
                        chainsaw_hunt = subprocess.run([saw_bin, 'hunt', evtx_path, '--mapping', map_dir, '--rules', sigma_dir, '--csv', output_dir + 'hunt_' + evtx_path.split('/')[-1]], stdout=subprocess.PIPE, text=True)
                        print(chainsaw_hunt.stdout)
                    else:
                        chainsaw_hunt = subprocess.run(['python3', saw_bin, 'hunt', evtx_path, '--mapping', map_dir, '--rules', sigma_dir, '--csv', output_dir + 'hunt_' + evtx_path.split('\\')[-1]], stdout=subprocess.PIPE, text=True)
                        print(chainsaw_hunt.stdout)
            elif default_answer[0].lower() == 'n':
                sigma_rules = []
                while True:
                    rule = input("Enter your sigma rule directory in (absolute path):\n> ")
                    sigma_rules.append(rule)
                    answer = input("Add more sigma rules? Y/N\n> ")
                    if answer[0].lower() == 'y':
                        continue
                    elif answer[0].lower() == 'n':
                        break
                    else:
                        print("Invalid choice\n")
                print("Begining Custom Sigma Rule Search...\n")
                for evtx_path in evtx_main_paths:
                    for rule in sigma_rules:
                        if plat == 'Linux':
                            custom_chainsaw_hunt = subprocess.run([saw_bin, 'hunt', evtx_path, '--mapping', map_dir, '--rules', rule, '--csv', output_dir + 'hunt_' + evtx_path + (rule.split('/'))[-1]], stdout=subprocess.PIPE, text=True)
                            print(custom_chainsaw_hunt.stdout)
                        else:
                            custom_chainsaw_hunt = subprocess.run(['python3', saw_bin, 'hunt', evtx_path, '--mapping', map_dir, '--rules', rule, '--csv', output_dir + 'hunt_' + evtx_path + (rule.split('/'))[-1]], stdout=subprocess.PIPE, text=True)
                            print(custom_chainsaw_hunt.stdout)
        elif user_choice == '2':
            print("*********************\n*Gonna Search it all*\n*********************\n")
            print("Output will be saved in the output directory with the following scheme: search_<evtx><regex>\n")
            while True:
                try:
                    query = input("Input your regex query below:\n> ")
                    for evtx_path in evtx_main_paths:
                        cntr = 1
                        if plat == 'Linux':
                            chainsaw_search = subprocess.run([saw_bin, 'search', evtx_path, '-r', query, '--output', output_dir + 'search_' + (evtx_path.split('/'))[-1] + '_' + query], stdout=subprocess.PIPE, text=True)
                        else:
                            chainsaw_search = subprocess.run(['python3', saw_bin, 'search', evtx_path, '-r', query, '--output', output_dir + 'search_' + (evtx_path.split('/'))[-1] + '_' + query], stdout=subprocess.PIPE, text=True)
                        cntr += 1
                except KeyboardInterrupt:
                    break
        elif user_choice == '3':
            print("Displaying general chainsaw man page\n")
            if plat == 'Linux':
                man_page = subprocess.run([saw_bin], stdout=subprocess.PIPE, text=True)
            else:
                man_page = subprocess.run(['python3', saw_bin], stdout=subprocess.PIPE, text=True)
            print("\n" + man_page.stdout + "\n")
        elif user_choice == '4':
            print("Exiting...\n")
            exit()
        else:
            print('Invalid menu option\n')
        output_cleaner(output_dir)
    except KeyboardInterrupt:
        print("User entered keyboard interrupt.\nExiting...\n")
        exit()