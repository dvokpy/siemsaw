#!/usr/bin/python3

from operator import contains
import os
import platform
import subprocess

#Used to detect OS platform
def os_detector():
    operating_system = platform.system()
    return operating_system

#Builds the windows config file
def config_generator(platform):
    if 'win' in platform:
        config_path = os.getcwd() + '\\config'
        try:
            if os.path.exists(config_path) and os.path.exists(os.getcwd() + '\\output_dir\\'):
                return config_path
            else:
                chainsaw_bin = input("Enter chainsaw binary absolute path:\n> ")
                config_dscr = open(config_path, 'w')
                config_dscr.write('Platform;' + platform + "\n")
                config_dscr.write('ChainsawBin;' + chainsaw_bin + "\n")
                output_dir = os.getcwd() + '\\output_dir\\'
                config_dscr.write('OutputDir;' + output_dir + "\n")
                mapping_file = ('\\'.join((chainsaw_bin.split('\\'))[:-1])) + '\\mapping_files\\sigma-mapping.yml'
                config_dscr.write('MappingFile;' + mapping_file + "\n")
                default_sigma_rules = ('\\'.join((chainsaw_bin.split('\\'))[:-1])) + '\\sigma_rules\\'
                config_dscr.write('DefaultSigmaDirectory;' + default_sigma_rules + "\n")
                os.mkdir(os.getcwd() + '\\output_dir\\')
                evtx_repo = os.getcwd() + '\\evtx_repo\\'
                config_dscr.write('EvtxRepo;' + evtx_repo + '\n')
                os.mkdir(evtx_repo)
                config_dscr.close()
                return config_path
        except KeyboardInterrupt:
            print("\nUser interuptted Program\nExiting...\n")
    elif platform == 'Linux':
        config_path = os.getcwd() + '/config'
        try:
            if os.path.exists(config_path) and os.path.exists(os.getcwd() + '/output_dir/'):
                return config_path
            else:
                chainsaw_bin = input("Enter chainsaw binary absolute path:\n> ")
                config_dscr = open(config_path, 'w')
                config_dscr.write('Platform;' + platform + "\n")
                config_dscr.write('ChainsawBin;' + chainsaw_bin + "\n")
                output_dir = os.getcwd() + '/output_dir/'
                config_dscr.write('OutputDir;' + output_dir + "\n")
                mapping_file = ('/'.join((chainsaw_bin.split('/'))[:-1])) + '/mapping_files/sigma-mapping.yml'
                config_dscr.write('MappingFile;' + mapping_file + "\n")
                default_sigma_rules = ('/'.join((chainsaw_bin.split('/'))[:-1])) + '/sigma_rules/'
                config_dscr.write('DefaultSigmaDirectory;' + default_sigma_rules + "\n")
                os.mkdir(os.getcwd() + '/output_dir/')
                evtx_repo = os.getcwd() + '/evtx_repo/'
                config_dscr.write('EvtxRepo;' + evtx_repo + '\n')
                os.mkdir(evtx_repo)
                config_dscr.close()
                return config_path
        except KeyboardInterrupt:
            print("\nUser interuptted Program\nExiting...\n")
    else:
        print("Unrecognized platform\nExiting...\n")
        exit()
        
#Reads lines from config and assigns that data to variable
def config_var_assign(conf_path):
    file_dsc = open(conf_path, 'r')
    conf_content = file_dsc.readlines()
    operating_system = ((conf_content[0].split(';'))[1])[:-1]
    chainsaw_binary = ((conf_content[1].split(';'))[1])[:-1]
    output_directory = ((conf_content[2].split(';'))[1])[:-1]
    mapping_directory = ((conf_content[3].split(';'))[1])[:-1]
    sigma_directory = ((conf_content[4].split(';'))[1])[:-1]
    evtx_dir = ((conf_content[5].split(';'))[1])[:-1]
    return operating_system, chainsaw_binary, output_directory, mapping_directory, sigma_directory, evtx_dir

#Gathers evtx paths
def evtx_builder(evtx_directory):
    try:
        evtx_paths = []
        answer = input("Would you like to manually load evtx files? Y/N\n")
        while True:
            if answer[0].lower() == 'y':
                evtx_path = input("Enter your evtx path below:\n> ")
                evtx_paths.append(evtx_path)
                cont_answr = input("Would you like to add another path to your query? Y/N\n> ")
                if cont_answr[0].lower() == 'y':
                    continue
                elif cont_answr[0].lower() == 'n':
                    break
            elif answer[0].lower() == 'n':
                print("Loading evtx files from directory\n")
                evtx_files = os.listdir(evtx_directory)
                for file in evtx_files:
                    evtx_paths.append(evtx_directory + file)
                break
    except KeyboardInterrupt:
        exit()
    print("The current loaded evtx files are:\n")
    for file in evtx_paths:
        print(file + "\n")
    return evtx_paths

#Cleans the output_dir for empty files and directories    
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
        

#Main loop
config_path = config_generator(os_detector())

operating_system, saw_bin, output_dir, map_dir, sigma_dir, evtx_directory = config_var_assign(config_path)

evtx_main_paths = evtx_builder(evtx_directory)

menu = '1)Chainsaw Hunt\n2)Chainsaw Search\n3)General Chainsaw Man Page\n4)Exit siemsaw\n'

while True:
    try:
        print(menu)
        user_choice = input('Enter your choice:\n> ')[0]
        if user_choice == '1':
            print("***************\n* TO THE HUNT *\n***************\n")
            default_answer = input("Would you like to use the default sigma rules? Y/N\n> ")
            if default_answer[0].lower() == 'y':
                for evtx_path in evtx_main_paths:
                    if operating_system == 'Linux':
                        chainsaw_hunt = subprocess.run([saw_bin, 'hunt', evtx_path, '--mapping', map_dir, '--rules', sigma_dir, '--csv', output_dir + 'hunt_' + evtx_path.split('/')[-1]], stdout=subprocess.PIPE, text=True)
                        print(chainsaw_hunt.stdout)
                    elif operating_system == 'Windows':
                        chainsaw_hunt = subprocess.run([saw_bin, 'hunt', evtx_path, '--mapping', map_dir, '--rules', sigma_dir, '--csv', output_dir + 'hunt_' + evtx_path.split('\\')[-1]], stdout=subprocess.PIPE, text=True)
                        print(chainsaw_hunt.stdout)
                    else:
                        print("Unknown operating system detected\n")
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
                        if operating_system == 'Linux':
                            custom_chainsaw_hunt = subprocess.run([saw_bin, 'hunt', evtx_path, '--mapping', map_dir, '--rules', rule, '--csv', output_dir + 'hunt_' + evtx_path + (rule.split('/'))[-1]], stdout=subprocess.PIPE, text=True)
                            print(custom_chainsaw_hunt.stdout)
                        elif operating_system == 'Windows':
                            custom_chainsaw_hunt = subprocess.run([saw_bin, 'hunt', evtx_path, '--mapping', map_dir, '--rules', rule, '--csv', output_dir + 'hunt_' + evtx_path + (rule.split('\\'))[-1]], stdout=subprocess.PIPE, text=True)
                            print(custom_chainsaw_hunt.stdout)
                        else:
                            print("Unknown operating system detected\n")
        elif user_choice == '2':
            print("*********************\n*Gonna Search it all*\n*********************\n")
            print("Output will be saved in the output directory with the following scheme: search_<evtx><regex>\n")
            while True:
                try:
                    query = input("Input your regex query below:\n> ")
                    for evtx_path in evtx_main_paths:
                        if operating_system == 'Linux':
                            chainsaw_search = subprocess.run([saw_bin, 'search', evtx_path, '-r', query, '--output', output_dir + 'search_' + (evtx_path.split('/'))[-1] + '_' + query], stdout=subprocess.PIPE, text=True)
                        elif operating_system == 'Windows':
                            chainsaw_search = subprocess.run([saw_bin, 'search', evtx_path, '-r', query, '--output', output_dir + 'search_' + (evtx_path.split('\\'))[-1] + '_' + query], stdout=subprocess.PIPE, text=True)
                        else:
                            print("Unknown operating system detected\n")
                except KeyboardInterrupt:
                    break
        elif user_choice == '3':
            print("Displaying general chainsaw man page\n")
            if operating_system == 'Linux':
                man_page = subprocess.run([saw_bin], stdout=subprocess.PIPE, text=True)
            elif operating_system == 'Windows':
                man_page = subprocess.run([saw_bin], stdout=subprocess.PIPE, text=True)
            else:
                print("Unknown operating system detected\n")
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