import os
import yaml
import subprocess
from time import sleep


def load_config(config_name: str, CONFIG_PATH="/home/pi/raingauge/code/config") -> dict:
    """
    A function to load and return config file in YAML format
    """
    with open(os.path.join(CONFIG_PATH, config_name)) as file:
        config = yaml.safe_load(file)
    return config


def send_test_data():
    lorawan_config = load_config("lorawan_keys.yaml")
    dev_addr = lorawan_config["rainpi_test"]["dev_addr"]
    nwk_skey = lorawan_config["rainpi_test"]["nwk_skey"]
    app_skey = lorawan_config["rainpi_test"]["app_skey"]
    success = False
    while not success:
        try:
            result = subprocess.call(
                [
                    "ttn-abp-send",
                    dev_addr,
                    nwk_skey,
                    app_skey,
                    str(3.14),
                    str(1),
                ]
            )
            if result == 0:
                success = True
            else:
                print("Subprocess call failed, retrying...")
        except subprocess.CalledProcessError as e:
            print(f"Error during subprocess call: {e}. Retrying...")


if __name__ == "__main__":
    while True:
        send_test_data()
        sleep(10)
