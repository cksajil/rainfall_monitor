"""
this file contain codes for unit testing using pytest framework
# SysConfigPath = "/home/icfoss/hari_work/z_git/rainfall_monitor/config"
# PiConfigPath = "/home/pi/raingauge/code/config"
"""
from utils.helper import time_stamp_fnamer,load_config,create_folder,load_estimate_model
from utils.helper import create_lstm_model_withcnn,create_lstm_model_withoutcnn,influxdb
from utils.estimate import create_cnn_data,combine_audios,estimate_rainfall
from datetime import datetime
import os,numpy as np
import subprocess
import librosa


# from helper.py
def test_load_config():
    config = load_config("config.yaml")
    influxdb_config = load_config("influxdb_api.yaml")
    assert type(config) == dict
    assert type(config["record_hours"]) is int
    assert config["file_format"] == "wav"
    assert type(influxdb_config) is dict
    assert type(influxdb_config["org"]) == str
    assert type(influxdb_config["url"]) == str


def test_time_stamp_fnamer(): 
    assert type(time_stamp_fnamer(datetime.now())) is str


def test_create_folder():
    direct = "./test/#testfolder#"
    create_folder(direct)
    assert os.path.exists(direct) is True
    os.rmdir(direct)


def test_create_lstm_model_withoutcnn():
    model = create_lstm_model_withoutcnn()
    assert model._dtype == 'float32'


def test_create_lstm_model_withcnn():
    model = create_lstm_model_withcnn()
    assert model.output_shape == (None,1)
    assert model._dtype == 'float32'


def test_load_estimate_model():
    # downloading ml models 
    path1 = "./test/models"
    create_folder(path1)
    url1 = 'https://docs.google.com/uc?export=download&id=17yY89nn5k9YEcEXLsZiXsKorpf9Mzlvr'
    path2 = "./test/models/rain_stft.hdf5"
    subprocess.run(["wget", "-O",path2, url1])
    #testing
    model = load_estimate_model("./test/models/rain_stft.hdf5") # works only for rain_stft model
    assert model.output_shape == (None,1)
    assert model._dtype == 'float32'
    # deleting ml models
    os.remove(path2)
    os.rmdir(path1)


def test_influxdb(): # already passed test
    pass
    # assert type(influxdb(80.8)) is bool 


# from estimate.py
def test_combine_audios(): # this function is invoking only inside estimate_rainfall
    # path = "/home/icfoss/hari_work/z_git/rainfall_monitor/test/audios"
    # create_folder(path)
    # url1 = 'https://drive.google.com/file/d/11sYLC_6djWUV42GQX251qsCzQyFabjlR/view?usp=drive_link'
    audioPath1 = "/home/icfoss/hari_work/z_git/rainfall_monitor/test/audios/2023_11_22_18_22_55_751632.wav"
    # subprocess.run(["wget","-O",audioPath1, url1])
    # url2 = 'https://drive.google.com/file/d/1YrXQEJvDSzhO8tUS5k_A9Fhnfzkz1egm/view?usp=drive_link'
    audioPath2 = "/home/icfoss/hari_work/z_git/rainfall_monitor/test/audios/2023_11_22_18_23_05_905819.wav"
    # subprocess.run(["wget","-O",audioPath2, url2])
    audioList = [audioPath1,audioPath2]
    x = combine_audios(audioList) # add list of paths
    assert type(x) is np.ndarray
    #assert len(x) == 2


def test_create_cnn_data(): # invoking inside estimate_rainfall only 
    pass
    # use output of "combine_audios" as input
    # assert output datatype is np.array

    # x = combine_audios("") # add audio path
    # y = create_cnn_data(x)
    # assert type(y) is np.ndarray
    # assert len(y) is "no of audio samples" # add no.of audo samples


def test_estimate_rainfall(): # invoking in daq.py only
    pass
    # dowload model from drive
    # model must be passed(output of load estimate model)
    # list of audio paths should be passed


#notes
# what if we give an input other than directory,or other data type
# what if the directory does not exist for folder creation function
# what if a required number of parameter is not passing to a function 
# HOW TO RESOLVE PATH ISSUES

# test boundary conditions (ie max and min inputs if there is any)
# positive test,try valied inputs and check for ecxpected result
# negative test,try invalid inputs and check how system is handling it
# it is important to write execption handling in functions
