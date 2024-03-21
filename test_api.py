import os
import yaml
import influxdb_client
from utils.helper import load_config
from influxdb_client.client.write_api import SYNCHRONOUS
from requests.exceptions import ConnectionError


def influxdb(rain: float) -> bool:
    """
    function to write data to influxdb
    """
    try:
        influxdb_config = load_config("influxdb_api.yaml")

        # Configure influxDB credentials
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


api_status = influxdb(0.28)
print(str(api_status))
