import os
import shutil
import json

#path+"/project-files/dynamips"


def correspondance_hostname_nodeid(path_gns3):
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
            hostname = node["name"][1:]
            id = node["node_id"]
            correspondance_dict[hostname] = id
    return correspondance_dict


def new_dynamips(correspondances, program_path, gns3_path):
    config_files_names = os.listdir(program_path+"/config_results")
    if len(correspondances) != len(config_files_names):
        print("WARNING: differences between .gns3 routers and produced routers")
    for filename in config_files_names:
        if ".cfg" in filename:
            hostname = filename[:len(filename)-4]
            router_config_path = gns3_path+"/project-files/dynamips/"
            router_config_path += correspondances[hostname]+"/configs/"

            # find the matching iXX_ number
            files_config_existante = os.listdir(router_config_path)
            new_name_path = ""
            for filename in files_config_existante:
                if "startup-config" in filename:
                    new_name_path = router_config_path + filename
                    os.remove(router_config_path+filename)

            shutil.copy(program_path+"/config_results/" + filename, new_name_path)


