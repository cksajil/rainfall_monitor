import os
import yaml


def time_stamp_fnamer(tstamp):
    """
    A function to generate filenames from timestamps
    """
    cdate, ctime =  str(tstamp).split(" ")
    current_date = "_".join(cdate.split("-"))
    chour, cmin, csec = ctime.split(":") 
    csec, cmilli = csec.split(".")
    current_time = "_".join([chour, cmin, csec, cmilli])
    current_date_time_name = "_".join([current_date, current_time])
    return current_date_time_name



def load_config(config_name):
    """
    A function to load and return config file in YAML format
    """
    CONFIG_PATH = "./config/"
    with open(os.path.join(CONFIG_PATH, config_name)) as file:
        config = yaml.safe_load(file)

    return config


def create_folder(directory):
    """Function to create a folder in a location if it does not exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)


# with open(path.join(config["data_dir"], dt_fname), "w") as f:
#     f.write("sample data")