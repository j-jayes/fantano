import pandas as pd
import configparser

config = configparser.ConfigParser()

config.read("config.ini")

api_key = config["apiDetails"]["key"]

print(api_key)

