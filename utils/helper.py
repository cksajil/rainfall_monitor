import os
import yaml

# from tensorflow.keras.callbacks import Callback


def time_stamp_fnamer(tstamp):
    """
    A function to generate filenames from timestamps
    """
    cdate, ctime = str(tstamp).split(" ")
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
    CONFIG_PATH = "/home/pi/raingauge/rainfall_monitor/config/"
    with open(os.path.join(CONFIG_PATH, config_name)) as file:
        config = yaml.safe_load(file)

    return config


def create_folder(directory):
    """Function to create a folder in a location if it does not exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_log_file(log_folder, log_file):
    with open(os.path.join(log_folder, log_file), "w") as f:
        f.write("Log file created")


# class EarlyStopper(Callback):
#    """
#    A class for early stopper callback for validation accuracy
#    """
#    def __init__(self, target):
#        super(EarlyStopper, self).__init__()
#        self.target = target
#
#    def on_epoch_end(self, epoch, logs={}):
#        val_loss = logs['val_loss']
#        if val_loss < self.target:
#            self.model.stop_training = True
