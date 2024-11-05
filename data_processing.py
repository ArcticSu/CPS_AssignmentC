import pandas as pd
from influxdb import InfluxDBClient

HOST = 'influx.linklab.virginia.edu'
PORT = 443
USERNAME = 'cps1f23'
PASSWORD = 'phah7goohohng5ooL9mae1quohpei1Ahsh1uGing'
DATABASE = 'gateway-generic'

client = InfluxDBClient(HOST, PORT, USERNAME, PASSWORD, DATABASE, ssl=True, verify_ssl=True)

def get_locations():
    query = """
    SELECT "value", "time", "location_specific" FROM "Temperature_°C"
    WHERE time >= '2024-10-07T00:00:00Z' AND time < '2024-10-08T00:00:00Z'
    """
    result = client.query(query)
    
    temperature_data = pd.DataFrame(result.get_points())
    
    if temperature_data.empty:
        print("No data found for the specified query.")
        return []
    
    unique_locations = temperature_data['location_specific'].unique()
    print("Locations available:", unique_locations)
    
    return unique_locations


def get_temperature_data(start_date, location):
    query = f"""
    SELECT mean("value") AS "avg_temperature" FROM "Temperature_°C"
    WHERE time >= '{start_date}T00:00:00Z' AND time < '{start_date}T23:59:59Z'
    AND "location_specific" = '{location}'
    GROUP BY time(1h) fill(none)
    """
    result = client.query(query)
    temperature_data = pd.DataFrame(result.get_points())
    # print("available:", temperature_data)
    return temperature_data

# get_temperature_data("2024-10-07", "20000 Olsson")
