import os
import shutil
import json
from difflib import Differ


def difference_significative(path1, path2):
    non_significatif = ["", " ", "!", " !","! "]
    with open(path1) as file1, open(path2) as file2:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

        differ = Differ()
        for line in differ.compare(lines1, lines2):
            if (line[0] == "+") or (line[0] == "-"):
                line = line[2:].rstrip("\n")
                if line not in non_significatif:
                    return True
        return False

def containing_folder(file_path):
    taille = len(file_path)
    if file_path[taille-1] == "/":
        file_path = file_path[:taille-1]
    parent_folder_path_end = file_path.rfind("/")
    return file_path[:parent_folder_path_end]

# retourne : clé = hostname, valeur = [node_id, dynamips_id]
def correspondance_hostname_nodeid(path_gns3):
    path_gns3 = containing_folder(path_gns3)
    liste_fichiers = os.listdir(path_gns3)
    project_file = ""
    correspondance_dict = {}
    for file in liste_fichiers:
        if (".gns3" in file) and not ("backup" in file):
            project_file = path_gns3+"/"+file
    with open(project_file) as file:
        data = json.load(file)
        nodes = data["topology"]["nodes"]
        for node in nodes:
            hostname = node["name"]
            node_id = node["node_id"]
            dyn_id = node["properties"]["dynamips_id"]
            correspondance_dict[hostname] = [node_id, dyn_id]
    return correspondance_dict


def new_dynamips(correspondances, program_path, gns3_path):
    need_restart_routers, total_router_number = [], 0 # sera retourné
    config_files_names = os.listdir(program_path+"/config_results")
    if len(correspondances) != len(config_files_names):
        print("WARNING: differences between .gns3 routers and produced routers")
        print(correspondances)
    for filename in config_files_names:
        if ".cfg" in filename:
            hostname = filename[:len(filename)-4]
            produced_path = program_path+"/config_results/" + hostname+".cfg"
            dyn_folder = containing_folder(gns3_path)+"/project-files/dynamips/"
            dyn_folder += correspondances[hostname][0]+"/configs/"
            dyn_filename = "i"+str(correspondances[hostname][1])+"_startup-config.cfg"
            dyn_path = dyn_folder + dyn_filename

            try:
                #si fichier dyn existant différent de produced
                if difference_significative(produced_path, dyn_path): 
                    shutil.copy(produced_path, dyn_path)
                    need_restart_routers.append(hostname)
                    if hostname == "CE2":
                        print(produced_path,dyn_path)
            except FileNotFoundError: # si le fichier dans dyn n'existe même pas
                pass

            total_router_number += 1
    
    return need_restart_routers, total_router_number

