import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import program.config as config
import program.move as move
import os

program_path = os.path.dirname(os.path.abspath(__file__)).replace(os.sep, '/')
json_path = ""
gns3_path = ""
last_button_pressed = "None" #None, Produce, Move or Update
last_config_dict = {}

def open_json():
    filename = filedialog.askopenfilename(initialdir=program_path, title="Select the json file")
    json_path_box.delete("1.0", tk.END)
    json_path_box.insert(tk.END, filename)
    global json_path
    json_path = filename

def open_gns3():
    filename = filedialog.askopenfilename(initialdir=program_path, title="Select the existing .gns3 project")
    gns3_path_box.delete("1.0", tk.END)
    gns3_path_box.insert(tk.END, filename)
    global gns3_path
    gns3_path = filename

def status_update(message):
    now = datetime.now().strftime("%H:%M:%S")
    formatted_message = "\n\n[" + str(now) + "] " + str(message)
    status_box.insert(tk.END, formatted_message)
    status_box.see("end")

def new_json_config():
    if json_path == "":
        status_update("ERROR: Please indicate a .json network intent file")
    else:
        if gns3_path == "":
            status_update("WARNING: No GNS3 project provided. Only config files production will be possible.")
        try:
            config.produce(program_path, json_path)
            status_update("Config successfully produced. Ready to be moved to the GNS3 project.")
            global last_button_pressed
            last_button_pressed = "Produce"
        except Exception as e:
            status_update(str("PYTHON ERROR:",e))

def move_to_gns3():
    if last_button_pressed == "Move" or last_button_pressed == "Update":
        status_update("ERROR: The config files have already been moved.")
    elif last_button_pressed == "":
        status_update("ERROR: Config files must be produced before being moved to the GNS3 project.")
    elif ".gns3" not in gns3_path:
        status_update("ERROR: The GNS3 project file has not been specified, or is not valid.")
    elif last_button_pressed == "Produce":
        correspondances = move.correspondance_hostname_nodeid(gns3_path)
        move.new_dynamips(correspondances, program_path, gns3_path)
        status_update("Config successfully moved to the GNS3 project. Please restart all routers.")
    else:
    	status_update("Erreur variable bouton")


def update():
    status_update("Pas encore implémenté")



root = tk.Tk()
root.title("NAS Project")

# First line : json
json_frame = tk.Frame(root)
json_frame.pack(fill="x", pady=10)

json_label = tk.Label(json_frame, text="Network intent file (.json) :")
json_label.pack(side="top", padx=10)

json_input_frame = tk.Frame(json_frame)
json_input_frame.pack(side="top")

json_button = tk.Button(json_input_frame, text="Open...", command=open_json)
json_button.pack(side="left", padx=10)

json_path_box = tk.Text(json_input_frame, height=1, width=50)
json_path_box.pack(side="left", padx=10)

# Second line : gns3 project
gns3_frame = tk.Frame(root)
gns3_frame.pack(fill="x", pady=(10,30))

gns3_label = tk.Label(gns3_frame, text="Existing .gns3 project :")
gns3_label.pack(side="top", padx=10)

gns3_input_frame = tk.Frame(gns3_frame)
gns3_input_frame.pack(side="top")

gns3_button = tk.Button(gns3_input_frame, text="Open...", command=open_gns3)
gns3_button.pack(side="left", padx=10)

gns3_path_box = tk.Text(gns3_input_frame, height=1, width=50)
gns3_path_box.pack(side="left", padx=10)

# Third line : buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

first_time_button = tk.Button(button_frame, text="Produce config files", command=new_json_config)
first_time_button.pack(side="left", padx=10)

update_button = tk.Button(button_frame, text="Move to GNS3", command=move_to_gns3)
update_button.pack(side="left", padx=10)

real_time_button = tk.Button(button_frame, text="(WIP) Update", command=update)
real_time_button.pack(side="left", padx=10)

# Fourth line : status
status_frame = tk.Frame(root)
status_frame.pack(fill="x", pady=10)

status_label = tk.Label(status_frame, text="Status :")
status_label.pack(side="top", padx=10)

status_box = tk.Text(status_frame, height=8, width=60, wrap=tk.WORD)
status_box.pack(side="top", padx=10)


root.mainloop()

