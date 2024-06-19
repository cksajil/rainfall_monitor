import os
import yaml
import influxdb_client
import tflite_runtime.interpreter as tflite
from requests.exceptions import ConnectionError
from influxdb_client.client.write_api import SYNCHRONOUS


def load_config(config_name: str, CONFIG_PATH="./config") -> dict:
    """
    A function to load and return config file in YAML format
    """
    with open(os.path.join(CONFIG_PATH, config_name)) as file:
        config = yaml.safe_load(file)
    return config


# loading config files
config = load_config("config.yaml")


def time_stamp_fnamer(tstamp) -> str:
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


def create_folder(directory: str) -> None:
    """
    Function to create a folder in a location if it does not exist
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_estimate_model(model_path: str) -> any:
    """
    Loads TFLITE model, build it and loads weights
    """
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter


def influxdb(rain: float) -> bool:
    """
    function to write data to influxdb
    """
    try:
        # Configure influxDB credentials
        influxdb_config = load_config("influxdb_api.yaml")
        bucket = influxdb_config["bucket"]
        org = influxdb_config["org"]
        token = influxdb_config["token"]
        url = influxdb_config["url"]

        # creating an object of influxdb_client
        client = influxdb_client.InfluxDBClient(
            url=url, token=token, org=org, timeout=30_000
        )
        write_api = client.write_api(write_options=SYNCHRONOUS)
        p = (
            influxdb_client.Point("ML-prediction")
            .tag("location", "greenfield tvm")
            .field("rain", rain)
        )

        write_api.write(bucket=bucket, org=org, record=p)
        client.close()
        return True
    except ConnectionError as e:
        print(f"Connection to InfluxDB failed: {e}")
        return False


def load_infer_model_path(board):
    if board == "raspberry_pi_zero_w":
        infer_model_path = os.path.join(
            config["infer_model_dir"], config["tflite_model"]
        )
    elif board == "raspberry_pi_4":
        if config["deployed_model_type"] == "withcnn":
            infer_model_path = os.path.join(
                config["infer_model_dir"], config["infer_model_withcnn"]
            )
        else:
            infer_model_path = os.path.join(
                config["infer_model_dir"], config["infer_model_withoutcnn"]
            )
    return infer_model_path
