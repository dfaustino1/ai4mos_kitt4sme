from fipy.ngsi.entity import StructuredValueAttr
import joblib
from roughnator.ngsy import Productions, Schedule
import subprocess
import json


NB400_MODEL_PATH_FROM_ROOT = 'data/nb_regressor.pkl'
ASB3_TRITAN_MODEL_PATH_FROM_ROOT = 'data/asb_tritan_regressor.pkl'
ASB3_ECOZEN_MODEL_PATH_FROM_ROOT = 'data/asb_ecozen_regressor.pkl'


# Uses the regressors to estimate the total energy consumption of the created schedule

def estimate_consumption(json_data):
    # Load the JSON string
    data = json.loads(json_data)
    # Load the regressor models
    nb_regressor = joblib.load(NB400_MODEL_PATH_FROM_ROOT)
    asb_tritan_regressor = joblib.load(ASB3_TRITAN_MODEL_PATH_FROM_ROOT)
    asb_ecozen_regressor = joblib.load(ASB3_ECOZEN_MODEL_PATH_FROM_ROOT)
    # Initialize variables for each machine's total consumption
    nb400_consumption = 0
    asb_tritan_consumption = 0
    asb_ecozen_consumption = 0
    # Loop through each production and predict the consumption for each machine
    for production in data['Productions']:
        quantity = production['Quantity']
        machine = production['Machines']
        if machine == '12M 3' or machine == '12M 4':
            if production['Product'] == 'CRISTAL TRITAN':
                asb_tritan_consumption += asb_tritan_regressor.predict([[quantity]])
            elif production['Product'] == 'CRISTAL ECOZEN':
                asb_ecozen_consumption += asb_ecozen_regressor.predict([[quantity]])
        elif machine == 'NB':
            nb400_consumption += nb_regressor.predict([[quantity]])
    # Calculate the total consumption
    total_consumption = nb400_consumption + asb_tritan_consumption + asb_ecozen_consumption
    return str(total_consumption)


# Converts the string output of the genetic algorithm in a json

def convert_to_json(final_output_str,consumption_str):
    # Split the string by the '|' character
    parts = final_output_str.split('|')
    # Remove the first and last elements, which are not part of the data
    parts = parts[1:-1]
    # Split each part by the ',' character
    data = [p.split(',') for p in parts]
    # Convert each part into a dictionary
    output = [{'ProductionId': d[0], 'Machines': d[1], 'start': str(d[2]), 'end': str(d[3])} for d in data]
    schedule = {}
    schedule["Schedule"] = output
    return {'Schedule': output, 'Consumption': consumption_str}


# Calls the genetic algorithm to create a schedule based on the productions input json 

def estimate(productions: Productions) -> Schedule:
    productionId_string = productions.productions.value
    json_input = json.dumps(productionId_string)
    json_algo_input = json_input.replace(", ", ",")
    consumption_str = estimate_consumption(json_input)
    
    # Subprocess was used because the algorithm was developed in java
    a = subprocess.run('java -jar ./roughnator/SchedulingKITT_json/dist/SchedulingKITT.jar', input=json_algo_input.encode(), capture_output=True, shell=True)
    
    final_output_json = convert_to_json(a.stdout.decode("utf-8"),consumption_str)
    schedule = Schedule(id=productions.id, schedule=StructuredValueAttr.new(final_output_json))
    
    return schedule
