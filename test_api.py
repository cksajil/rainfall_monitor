import os
import yaml
import influxdb_client
from utils.helper import load_config
from utils.helper import influxdb
from influxdb_client.client.write_api import SYNCHRONOUS
from requests.exceptions import ConnectionError


api_status = influxdb(0.28)
print(str(api_status))
