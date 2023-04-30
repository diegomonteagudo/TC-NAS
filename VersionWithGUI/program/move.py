import os
import shutil
import json

#path+"/project-files/dynamips"

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
    config_files_names = os.listdir(program_path+"/config_results")
    if len(correspondances) != len(config_files_names):
        print("WARNING: differences between .gns3 routers and produced routers")
        print(correspondances)
    for filename in config_files_names:
        if ".cfg" in filename:
            hostname = filename[:len(filename)-4]
            router_config_path = containing_folder(gns3_path)+"/project-files/dynamips/"
            router_config_path += correspondances[hostname][0]+"/configs/"

            # # find the matching iXX_ number USELESS NOW
            # files_config_existante = os.listdir(router_config_path)
            # new_name_path = ""
            # print("Routeur: ",hostname)
            # print(files_config_existante)
            # print("/\ c'est ce que j'ai trouvé dans :", router_config_path)
            # for filename in files_config_existante:
            #     if "startup-config" in filename:
            #         new_name_path = router_config_path + filename
            #         os.remove(router_config_path+filename)
            new_name_path = router_config_path + "i"+str(correspondances[hostname][1])+"_startup-config.cfg"

            shutil.copy(program_path+"/config_results/" + hostname+".cfg", new_name_path)


